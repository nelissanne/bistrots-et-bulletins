import duckdb
import pandas as pd
import requests

BASE = "https://www.data.gouv.fr/api/1"


# Fonction de récupération des URL par nom de fichier
def get_url(ds, title_part, fmt="parquet"):
    res = next(r for r in ds["resources"]
               if title_part in r["title"] and r["format"].lower() == fmt)
    return res["url"]


# Récupération des données des élections municipales 2026
ds_elections = requests.get(f"{BASE}/datasets/donnees-des-elections-agregees/").json()
url_candidats = get_url(ds_elections, "Résultats par candidat")

t1_muni_26 = duckdb.sql(f"""
    SELECT *
    FROM read_parquet('{url_candidats}')
    WHERE id_election == '2026_muni_t1'
""").df()

t2_muni_26 = duckdb.sql(f"""
    SELECT *
    FROM read_parquet('{url_candidats}')
    WHERE id_election == '2026_muni_t2'
""").df()

# Récupération des données des bistrots (NAF 56.30Z) dans le répertoire Sirene

ds_sirene = requests.get(f"{BASE}/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/").json()
url_etab = get_url(ds_sirene, "StockEtablissement")

bistrots_sirene = duckdb.sql(f"""
    SELECT *
    FROM read_parquet('{url_etab}')
    WHERE activitePrincipaleEtablissement == '56.30Z'
""").df()


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