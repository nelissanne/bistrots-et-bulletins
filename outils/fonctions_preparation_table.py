import pandas as pd

def synthese_table_muni(muni):

    """
    Fonction qui transforme les tables sources brutes en tables synthétiques (ie, avec les colonnes nécessaires à l'analyse)

    La fonction prend en entrée la table brute
    La fonction renvoie une table avec les colonnes générales de description du vote, 
    et les colonnes Nuance, et nb de siège aux conseils municipaux, pour toutes les listes candidates au sein de la commune,
    en format long et non large. 

    """
    col_com = muni.columns[~muni.columns.str.contains(r"\d")].tolist()
    col_vote = muni.columns[muni.columns.str.contains(r"Nuance|CM|% Voix/inscrits|% Voix/exprimés", case=False)].tolist()
    muni = muni[col_com + col_vote]

    muni_long = (
        pd.wide_to_long(
            muni,
            stubnames=["Nuance liste", "Sièges au CM", "% Voix/inscrits",  "% Voix/exprimés"],
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


def crea_ind1(df, nomenclature):
    """
    Fonction permettant de créer un indicateur de nuance majoritaire au conseil municipal : 
    - prend 1 si la nuance majoritaire est de droite
    - prend 2 si la nuance majoritaire est sans étiquette
    - prend 0 sinon (gauche ou centre)

    La fonction prend en entrée la table renvoyée par la fonction synthese_table_muni, 
    et la nomenclature de classement des nuances en couleur 
    La fonction renvoie en sortie une table avec l'indicateur 1
    """

    # Sélection de la liste ayant obtenu le plus de sièges au CM
    df_ind1 = (
        df.loc[
            df.groupby('Code commune')['Sièges au CM'].idxmax(),
            ['Code commune', 'Libellé commune', 'Nombre candidats', 'Nuance']
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    # Merge avec la nomenclature des couleurs politiques
    df_ind1 = (df_ind1.merge(nomenclature)
            .rename(columns={'Nuance': 'Nuance_maj'}))

    # Création de l'indicateur 1
    df_ind1['ind1'] = 0

    df_ind1.loc[df_ind1['Couleur'] == 'Droite', 'ind1'] = 1
    df_ind1.loc[df_ind1['Couleur'] == 'Sans étiquette', 'ind1'] = 2

    return df_ind1


def crea_ind2(df, nomenclature):
    """
    Fonction permettant de créer un indicateur de couleur majoritaire au conseil municipal : 
    - prend 1 si la couleur majoritaire est de droite
    - prend 2 si la couleur majoritaire est sans étiquette
    - prend 0 sinon (gauche ou centre)

    La fonction prend en entrée la table renvoyée par la fonction synthese_table_muni, 
    et la nomenclature de classement des nuances en couleur 
    La fonction renvoie en sortie une table avec l'indicateur 2
    """

    # Ajout nomenclature
    df = df.merge(nomenclature)

    # Sommer le nombre de sièges par commune et couleur et conserver la couleur majoritaire
    df_ind = (df.drop(columns='Nuance')
            .groupby(['Code commune', 'Couleur'], as_index=False)
            .agg({'Sièges au CM': 'sum'})
        )

    df_ind = df_ind.loc[
        df_ind.groupby('Code commune')['Sièges au CM'].idxmax()
    ].copy()

    # Création de ind2
    df_ind['ind2'] = 0
    df_ind.loc[df_ind['Couleur'] == 'Droite', 'ind2'] = 1
    df_ind.loc[df_ind['Couleur'] == 'Sans étiquette', 'ind2'] = 2

    return df_ind


def crea_ind3(df_nuance):
    """
    Fonction permettant de créer un indicateur d'extrême droite : 
    - prend 1 si la nuance est d'extrême droite
    - prend 2 si la nuance est sans étiquette
    - prend 0 sinon (gauche ou centre)

    La fonction prend en entrée la table renvoyée par la fonction crea_ind1, de laquelle on drop la colonne ind1
    La fonction renvoie en sortie une table avec l'indicateur 3
    """
    nuances_extd = ['LRN', 'LUXD', 'LEXD', 'LUDR']

    df_nuance["ind3"] = (
        df_nuance["Nuance_maj"].isin(nuances_extd).astype(int)
    )
    df_nuance.loc[df_nuance["Couleur"] == "Sans étiquette", "ind3"] = 2

    return df_nuance


def crea_ind4(df_nuance):
    """
    Fonction permettant de créer un indicateur Horizon : 
    - prend 1 si la nuance est de la liste Horizon
    - prend 2 si la nuance est sans étiquette
    - prend 0 sinon

    La fonction prend en entrée la table renvoyée par la fonction crea_ind1, de laquelle on drop la colonne ind1
    La fonction renvoie en sortie une table avec l'indicateur 4
    """
    nuance_Hor = ['LHOR']

    df_nuance["ind4"] = (
        df_nuance["Nuance_maj"].isin(nuance_Hor).astype(int)
    )
    df_nuance.loc[df_nuance["Couleur"] == "Sans étiquette", "ind4"] = 2

    return df_nuance


def calcul_part_vote_liste_gagnante(df):
    """
    Calcule la part de voix/exprimés de la liste gagnante.
    Entrée : la table renvoyée par la fonction synthese_table_muni.
    Sortie : une table indexée sur le code commune, avec une ligne par commune
    (la liste gagnante) et la colonne part_votes_liste_gagnante.
    """
    # Création de la variable % votes liste gagnante
    df_part = df.copy()

    df_part["part_votes_liste_gagnante"] = (
        pd.to_numeric(
            df_part["% Voix/exprimés"].astype(str)
                .str.replace("%", "", regex=False)
                .str.replace(",", ".", regex=False)
                .str.strip(),
        ) / 100
    )

    df_part = (
        df_part.sort_values("part_votes_liste_gagnante", ascending=False)
               .drop_duplicates(subset="Code commune")
    )

    return df_part