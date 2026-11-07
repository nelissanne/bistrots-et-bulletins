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

# Fonction pour créer l'indicateur 1 
def crea_ind1(df, nomenclature_couleur_nuance):

    # Sélection de la liste ayant obtenu le plus de sièges au CM
    df_ind1 = (
        df.loc[
            df.groupby('Code commune')['Sièges au CM'].idxmax(),
            ['Code commune', 'Libellé commune', 'Nuance']]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    # Merge avec la nomenclature des couleurs politiques
    df_ind1 = (df_ind1.merge(nomenclature_couleur_nuance)
        .rename(columns={'Nuance': 'Nuance_maj'}))

    # Création de l'indicateur 1
    df_ind1['ind1'] = 0

    df_ind1.loc[df_ind1['Couleur'] == 'Droite', 'ind1'] = 1
    df_ind1.loc[df_ind1['Couleur'] == 'Sans étiquette', 'ind1'] = 2

    return df_ind1