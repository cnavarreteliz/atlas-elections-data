import json
import numpy as np
import os
import pandas as pd

from comchoice.preprocessing.to_pairwise import to_pairwise
from comchoice.aggregate import borda, divisiveness, win_rate
from glob import glob


RATE_THRESHOLD = 0.02
DIVISIVENESS_COLUMN = "rate"  # Values accepted are {"rate": "rank"}
_labels = open("acronyms.json", encoding="utf-8")
_labels = json.load(_labels)


for year, country, location_level in [
    (2009, "Romania", "county_name"),
    (2017, "Chile", "province"),
    (2021, "Chile", "province"),
    (2017, "France", "department"),
    (2022, "France", "department"),
    (2018, "Brazil", "region")
]:
    print(year, country)
    labels = _labels[f"{country}_{year}"]

    df = pd.read_csv(
        f"data_output/{country}/{year}_first_round.csv.gz", compression="gzip")
    df.columns = [x.lower() for x in df.columns]

    dd = df.groupby("candidate").agg({"value": "sum"})
    dd["rate"] = dd.apply(lambda x: x/x.sum())
    values = list(dd[dd["rate"] > RATE_THRESHOLD].index.unique())

    df_runoff = pd.read_csv(
        f"data_output/{country}/{year}_runoff.csv.gz", compression="gzip")
    df_runoff.columns = [x.lower() for x in df_runoff.columns]

    df_location = pd.read_csv(
        f"data_output/{country}/{year}_first_round_location.csv.gz", compression="gzip")

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

    path = f"data_output/{country}/{year}_pairwise.csv.gz"

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
        {DIVISIVENESS_COLUMN: "std"}).rename(columns={DIVISIVENESS_COLUMN: "value"}).reset_index()
    path = f"data_output/{country}/{year}_divisiveness_{location_level}.csv.gz"

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
    encoding = "utf-8"
    if country == "Romania":
        encoding = "iso8859_16"
    dd.to_csv(
        f"data_regressions/{country}_{year}_polling_station.csv",
        encoding=encoding,
        index=False
    )
