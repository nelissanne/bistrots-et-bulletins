import duckdb
import pandas as pd
import requests

BASE = "https://www.data.gouv.fr/api/1"




# Récupération des données des élections municipales 2026
url_t1 = "https://tabular-api.data.gouv.fr/api/resources/4feeef01-24f7-4d5a-914f-8aa806f31ec2/data/csv/"
t1_muni_26 = pd.read_csv(url_csv, sep=",")

url_t2 = "https://tabular-api.data.gouv.fr/api/resources/6ff67a28-01bf-459e-beca-dd7aa8132dc1/data/csv/"
t2_muni_26 = pd.read_csv(url_csv, sep=",")

# Récupération des données des bistrots (NAF 56.30Z) dans le répertoire Sirene

url_sirene = "https://static.data.gouv.fr/resources/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/20261001-073823/stock-stocketablissement-parquet.parquet"
tous_bistrots_sirene = duckdb.sql(f"""
    SELECT *
    FROM read_parquet('{url_sirene}')
    WHERE activitePrincipaleEtablissement == '56.30Z'
""").df()

# Récupération des dates de fermeture des bistrots fermés depuis les municipales
url_sirene_historique = "https://static.data.gouv.fr/resources/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/20261001-074108/stock-stocketablissementhistorique-parquet.parquet"
bistrots_sirene_fermetures = duckdb.sql(f"""
    SELECT siret, dateDebut AS date_fermeture
    FROM read_parquet('{url_sirene_historique}')
    WHERE etatAdministratifEtablissement = 'F'
      AND changementEtatAdministratifEtablissement = 'true'
""").df()

# Merge des bistrots avec leur éventuelle date de fermeture
bistrots_sirene_actifs = tous_bistrots_sirene.merge(
  bistrots_sirene_fermetures,
  left_on = ["siret"],
  right_on = ["siret"],
  how = "left"
)

# Filtre des bistrots pour qu'ils soient ouverts pendant les municipales
bistrots_sirene = bistrots_sirene_actifs[((bistrots_sirene_actifs.date_fermeture >= "2026-01-04") | (bistrots_sirene_actifs.date_fermeture.isnull())) & (bistrots_sirene_actifs.dateCreationEtablissement <= "2026-03-01")]

# Récupération des données Filosofi au niveau commune - pas utile immédiatement mais à intégrer plus tard à l'analyse ?

def get_melodi(dataset, dimension, code, value_name, time_period, geo_level="COM"):

  url = f"https://api.insee.fr/melodi/data/{dataset}"

  params = {
    "GEO": geo_level,
    dimension: code,
    "TIME_PERIOD": time_period,
    "maxResult": 40000,
  }

  response = requests.get(url, params=params, timeout=60)
  response.raise_for_status()
  observations = response.json()["observations"]

  return pd.DataFrame(
    {
      "CODGEO": obs["dimensions"]["GEO"].split("-")[-1],
      value_name: obs["measures"]["OBS_VALUE_NIVEAU"].get("value"),
    }
    for obs in observations
  )

niveau_vie = get_melodi("DS_FILOSOFI_CC", "FILOSOFI_MEASURE", "MED_SL", "NIVVIE_MEDIAN", 2023)
taux_pauvrete = get_melodi("DS_FILOSOFI_CC", "FILOSOFI_MEASURE", "PR_MD60", "TAUX_PAUVRETE", 2023)
population = get_melodi("DS_POPULATIONS_HISTORIQUES", "POPREF_MEASURE", "PMUN", "POPULATION", 2023)

url_cog_2023 = "https://www.insee.fr/fr/statistiques/fichier/6800675/v_commune_2023.csv"
url_backup = "https://minio.lab.sspcloud.fr/lgaliana/data/python-ENSAE/cog_2023.csv"

try:
  cog_2023 = pd.read_csv(url_cog_2023)
except requests.exceptions.Timeout:
  cog_2023 = pd.read_csv(url_backup)

noms_communes = (
  cog_2023
  .loc[cog_2023["TYPECOM"] == "COM", ["COM", "LIBELLE"]]
  .rename(columns={"COM": "CODGEO", "LIBELLE": "LIBGEO"})
)

filosofi = (
  niveau_vie
  .merge(taux_pauvrete, on="CODGEO", how="outer")
  .merge(population, on="CODGEO", how="outer")
  .merge(noms_communes, on="CODGEO", how="left")
  [["CODGEO", "LIBGEO", "POPULATION", "NIVVIE_MEDIAN", "TAUX_PAUVRETE"]]
)

filosofi["POPULATION"] = filosofi["POPULATION"].astype(int)
filosofi["dep"] = filosofi["CODGEO"].str[:2]