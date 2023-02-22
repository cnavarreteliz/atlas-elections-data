import numpy as np
import pandas as pd


def get_data(
    country,
    year,
    aggregation,
    election="runoff",
    method="nv"
):
    output_df = pd.read_csv(
        f"../data_output/{country}/{year}_divisiveness_{aggregation}_{method}_{election}.csv.gz")

    output_within = output_df[output_df["type"] == "Within"].copy()
    output_between = output_df[output_df["type"] == "Between"].copy()

    output_between[aggregation] = output_between[aggregation].astype(str)
    output_within[aggregation] = output_within[aggregation].astype(str)

    output_data = pd.merge(output_between, output_within,
                           on=["candidate", aggregation])
    output_data["epi"] = (output_data["value_x"] + output_data["value_y"])

    output_data["epi_between"] = output_data["value_x"]
    output_data["epi_within"] = output_data["value_y"]

    output_data = output_data.groupby(aggregation).agg(
        {"epi": "sum", "epi_between": "sum", "epi_within": "sum"})
    output_data = output_data.reset_index().dropna()
    output_data["year"] = year
    output_data["year"] = output_data["year"].astype(int)

    return output_data
