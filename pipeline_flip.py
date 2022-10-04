import pandas as pd

from data_curation import flip_df

method = "er"
for year, country, location_level in [
    # (2009, "Romania", "county_name"),
    # (2017, "Chile", "province"),
    (2021, "Chile", "province"),
    # (2017, "France", "department_id"),
    (2022, "France", "department_id"),
    # (2018, "Brazil", "region_id")
]:
    print(country, year)
    df_fround = pd.read_csv(
        f"data_output/{country}/{year}_first_round.csv.gz",
        compression="gzip")
    df_fround.columns = [x.lower() for x in df_fround.columns]
    print(df_fround["candidate"].unique())
    df_runoff = pd.read_csv(
        f"data_output/{country}/{year}_runoff.csv.gz", compression="gzip")
    df_runoff.columns = [x.lower() for x in df_runoff.columns]

    df_location = pd.read_csv(
        f"data_output/{country}/{year}_first_round_location.csv.gz",
        compression="gzip")

    df_dv = pd.read_csv(
        f"data_output/{country}/{year}_divisiveness_{location_level}_{method}.csv.gz", compression="gzip")

    flip_df(
        df_fround,
        df_runoff,
        df_location,
        df_dv,
        country,
        year,
        location_level
    )
