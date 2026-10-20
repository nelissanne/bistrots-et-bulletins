# Fonction pour classer les nuances en couleur 
def classer_nuance(df_nuance):
    # Créer la nouvelle variable
    df_nuance["Couleur"] = ""

    # Règles de décision principales
    df_nuance.loc[df_nuance["Nuance"].str.endswith("C", na=False), "Couleur"] = "Centre"
    df_nuance.loc[df_nuance["Nuance"].str.endswith("D", na=False), "Couleur"] = "Droite"
    df_nuance.loc[df_nuance["Nuance"].str.contains("R", na=False), "Couleur"] = "Droite"
    df_nuance.loc[df_nuance["Nuance"].str.endswith("G", na=False), "Couleur"] = "Gauche"
    df_nuance.loc[df_nuance["Nuance"].str.contains("EC", na=False), "Couleur"] = "Gauche"

    # Exceptions : écrasent les règles principales
    df_nuance.loc[df_nuance["Nuance"] == "LREG", "Couleur"] = "Régionaliste"
    df_nuance.loc[df_nuance["Nuance"] == "LDIV", "Couleur"] = "Autre"
    df_nuance.loc[df_nuance["Nuance"].isin(["LHOR", "LUDI"]), "Couleur"] = "Centre"
    df_nuance.loc[df_nuance["Nuance"].isin(["LSOC", "LFI", "LCOM"]), "Couleur"] = "Gauche"
    

    # Contrôle : nuances sans couleur
    sans_couleur = df_nuance.loc[df_nuance["Couleur"].eq(""), "Nuance"].unique()

    if len(sans_couleur) > 0:
        raise ValueError(
            f"STOP : il y a {len(sans_couleur)} nuances sans couleur : "
            f"{list(sans_couleur)}. Impossible de renvoyer la table."
        )

    return df_nuance


def classer_nuance_extd(df_nuance):
    nuances_extd = ['LRN', 'LUXD', 'LEXD', 'LUDR']

    df_nuance["ind3"] = (
        df_nuance["Nuance_maj"].isin(nuances_extd).astype(int)
    )

    sans_ind3 = df_nuance.loc[df_nuance["ind3"].eq(""), "Nuance_maj"].unique()

    if len(sans_ind3) > 0:
        raise ValueError(
            f"STOP : il y a {len(sans_ind3)} nuances sans indicateur : "
            f"{list(sans_ind3)}. Impossible de renvoyer la table."
        )
    return df_nuance