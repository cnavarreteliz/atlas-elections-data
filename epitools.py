import numpy as np
import pandas as pd


def get_data(
    country,
    year,
    aggregation,
    candidate="candidate",
    election="runoff"
):
    output_df = pd.read_csv(
        f"data_curated/{country}/antagonism_{year}_{aggregation}_{election}.csv.gz")

    output_within = output_df[output_df["type"] == "EP"].copy()
    output_between = output_df[output_df["type"] == "EC"].copy()

    output_between[aggregation] = output_between[aggregation].astype(str)
    output_within[aggregation] = output_within[aggregation].astype(str)

    output_data = pd.merge(output_between, output_within,
                            on=[candidate, aggregation])
    
    output_data["ec"] = output_data["antagonism_x"]
    output_data["ep"] = output_data["antagonism_y"]

    output_data = output_data.groupby(aggregation).agg({"ec": "sum", "ep": "sum"})
    output_data = output_data.reset_index().dropna()
    output_data["year"] = year
    output_data["year"] = output_data["year"].astype(int)

    return output_data

