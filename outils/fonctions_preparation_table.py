import pandas 

# Fonction pour synthétiser les tables brutes des municipales (= sélectionner les colonnes pertinentes pour l'analyse et adapter le format)
def synthese_table_muni(muni):
    col_com = muni.columns[~muni.columns.str.contains(r"\d")].tolist()
    col_vote = muni.columns[muni.columns.str.contains(r"Nuance|CM", case=False)].tolist()
    muni = muni[col_com + col_vote]

    muni_long = (
        pandas.wide_to_long(
            muni,
            stubnames=["Nuance liste", "Sièges au CM"],
            i="Code commune",
            j="numero_liste",
            sep=" ",
            suffix=r"\d+"
        )
        .rename(columns={"Nuance liste": "Nuance"})
        .reset_index()
        .drop(columns="numero_liste")
    )

    return muni_long
