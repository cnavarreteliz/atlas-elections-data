import numpy as np
import os
import pandas as pd

from comchoice.preprocessing.to_pairwise import to_pairwise
from comchoice.aggregate import borda, divisiveness, win_rate
from glob import glob


RATE_THRESHOLD = 0.02
labels = {
    "Anne HIDALGO": "hidalgo",
    "Emmanuel MACRON": "macron",
    "Fabien ROUSSEL": "roussel",
    "Jean LASSALLE": "lassalle",
    "Jean-Luc MÉLENCHON": "melenchon",
    "Marine LE PEN": "le_pen",
    "Nathalie ARTHAUD": "arthaud",
    "Nicolas DUPONT-AIGNAN": "dupont",
    "Philippe POUTOU": "poutou",
    "Valérie PÉCRESSE": "pecresse",
    "Yannick JADOT": "jadot",
    "Éric ZEMMOUR": "zemmour",
    'Benoît HAMON': "hamon",
    'François FILLON': "fillon",

    "ALVARO FERNANDES DIAS": "alvaro",
    "BENEVENUTO DACIOLO FONSECA DOS SANTOS": "daciolo",
    "CIRO FERREIRA GOMES": "ciro",
    "FERNANDO HADDAD": "haddad",
    "GERALDO JOSÉ RODRIGUES ALCKMIN FILHO": "alckmin",
    "GUILHERME CASTRO BOULOS": "boulos",
    "HENRIQUE DE CAMPOS MEIRELLES": "meirelles",
    "JAIR MESSIAS BOLSONARO": "bolsonaro",
    "JOSE MARIA EYMAEL": "eymael",
    "JOÃO DIONISIO FILGUEIRA BARRETO AMOEDO": "amoedo",
    "JOÃO VICENTE FONTELLA GOULART": "goulart",
    "MARIA OSMARINA MARINA DA SILVA VAZ DE LIMA": "da_silva",
    "VERA LUCIA PEREIRA DA SILVA SALGADO": "vera_lucia",

    "GABRIEL BORIC FONT": "boric",
    "JOSE ANTONIO KAST RIST": "kast",
    "YASNA PROVOSTE CAMPILLAY": "provoste",
    "SEBASTIAN SICHEL RAMIREZ": "sichel",
    "EDUARDO ARTES BRICHETTI": "artes",
    "MARCO ENRIQUEZ-OMINAMI GUMUCIO": "meo",
    "FRANCO PARISI FERNANDEZ": "parisi",

    "CAROLINA GOIC BOROEVIC": "goic",
    "SEBASTIAN PIÑERA ECHENIQUE": "pinera",
    "ALEJANDRO  GUILLIER ALVAREZ": "guillier",
    "MARCO  ENRIQUEZ-OMINAMI GUMUCIO": "meo",
    "BEATRIZ SANCHEZ MUÑOZ": "sanchez",

    "Constantin Ninel Potârcă": "potarca",
    "Constantin Rotaru": "rotaru",
    "Corneliu Vadim Tudor": "tudor",
    "Crin Antonescu": "antonescu",
    "George Becali": "becali",
    "Gheorghe-Eduard Manole": "manole",
    "Hunor Kelemen": "kelemen",
    "Mircea Geoană": "geoana",
    "Ovidiu Cristian Iane": "iane",
    "Remus Cernea": "cernea",
    "Sorin Oprescu": "oprescu",
    "Traian Băsescu": "basescu"
}

for year, country, location_level in [
    (2009, "Romania", "county_name"),
    (2017, "Chile", "commune"),
    (2021, "Chile", "commune"),
    (2017, "France", "department"),
    (2022, "France", "department")
]:
    print(year, country)

    df = pd.read_csv(
        f"data_output/{country}/{year}_first_round.csv.gzip", compression="gzip")
    df.columns = [x.lower() for x in df.columns]

    dd = df.groupby("candidate").agg({"value": "sum"})
    dd["rate"] = dd.apply(lambda x: x/x.sum())
    values = list(dd[dd["rate"] > RATE_THRESHOLD].index.unique())

    df_runoff = pd.read_csv(
        f"data_output/{country}/{year}_runoff.csv.gzip", compression="gzip")
    df_runoff.columns = [x.lower() for x in df_runoff.columns]

    df_location = pd.read_csv(
        f"data_output/{country}/{year}_first_round_location.csv.gzip", compression="gzip")

    df = df[df["candidate"].isin(values)]
    df_runoff = df_runoff[df_runoff["candidate"].isin(values)]

    df1 = pd.merge(df, df_location[["polling_id", location_level]])

    df1 = df1.groupby([location_level, "candidate"]).agg({"value": "sum"})
    df1["rate"] = df1.groupby(level=[0]).apply(lambda x: x/x.sum())
    df1 = df1.reset_index()

    df2 = pd.merge(df_runoff, df_location[["polling_id", location_level]])

    df2 = df2.groupby([location_level, "candidate"]).agg({"value": "sum"})
    df2["rate"] = df2.groupby(level=[0]).apply(lambda x: x/x.sum())
    df2 = df2.reset_index()

    df_rounds = pd.merge(df1, df2, on=[location_level, "candidate"])
    df_rounds["diff"] = df_rounds["rate_y"] - df_rounds["rate_x"]

    path = f"data_output/{country}/{year}_pairwise.csv.gzip"

    if not os.path.isfile(path):

        df_pwc = to_pairwise(
            df,
            alternative="candidate",
            verbose=True,
            voter="polling_id"
        )
        df_pwc.to_csv(path, compression="gzip", index=False)

    else:
        df_pwc = pd.read_csv(path, compression="gzip")

    data = pd.merge(df_location[[location_level, "polling_id"]].drop_duplicates(
    ), df.copy(), on="polling_id").copy()

    df_dv = data.groupby([location_level, "candidate"]).agg(
        {"rate": "std"}).rename(columns={"rate": "value"}).reset_index()
    path = f"data_output/{country}/{year}_divisiveness_{location_level}.csv.gzip"

    df_dv.to_csv(path, compression="gzip", index=False)

    location = "polling_id"

    def get_rate(df, location=["polling_id"], level=[0]):
        df_tmp = df.groupby(location + ["candidate"]).agg({"value": "sum"})
        df_tmp["rate"] = df_tmp.groupby(level=level).apply(lambda x: x/x.sum())
        df_tmp = df_tmp.reset_index()

        return df_tmp

    df = pd.merge(df, df_location, on="polling_id")

    df_a = get_rate(df, location=[location_level, "polling_id"], level=[0, 1])
    df_a = pd.merge(df_a, df_dv.rename(columns={"value": "divisiveness"}), on=[
                    location_level, "candidate"])

    df_b = get_rate(df_runoff)

    dd = df_a.pivot_table(
        index=["polling_id"],
        columns=["candidate"],
        values=["rate", "value", "divisiveness"]
    ).reset_index()

    cols = []
    for column in dd.columns:
        a, b = column
        new_column = None
        if not b:
            new_column = a
        else:
            new_column = f"{a}_{labels[b]}"

        cols.append(new_column)

    dd.columns = cols
    dd = pd.merge(dd, df_b, on="polling_id")
    dd.to_csv(
        f"data_output/regression_{country}_{year}.csv", encoding="utf-8", index=False)
