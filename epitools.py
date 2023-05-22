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
        f"data_output/{country}/{year}_divisiveness_{aggregation}_{method}_{election}.csv.gz")

    if method in ["nv", "nv_all"]:
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

    else:
        return output_df


def between_p(
    input_df
):
    values = input_df.pivot(
        index="candidate",
        columns="polling_id",
        values="value"
    )
    rates = input_df.pivot(
        index="candidate",
        columns="polling_id",
        values="rate"
    )

    output = []
    total = values.sum().sum()

    for candidate in rates.index:
        N_candidates = rates.shape[0]
        rates_c = rates[rates.index == candidate]
        values_c = values[values.index == candidate]

        xx = np.tile(rates_c, reps=(N_candidates, 1))
        yy = np.tile(values_c, reps=(N_candidates, 1))

        between = np.multiply(yy, (1 - np.absolute(xx - rates)))  # 1 -
        between = between[between.index != candidate]

        dv_between = 0 if np.sum(values_c).sum() == 0 else np.sum(
            between).sum() / (N_candidates * (N_candidates - 1) * np.sum(values_c).sum())
        output.append({
            "candidate": candidate,
            "value": dv_between,
            "weight": values_c.sum().sum()/total
        })

    df_between = pd.DataFrame(output)
    df_between["type"] = "Between"

    return df_between


def within_p(input_df):
    values = input_df.pivot(
        index="candidate",
        columns="polling_id",
        values="value"
    )

    total = values.sum().sum()

    def get_average(x, total=1):
        return x["value"].sum() / total

    # total = dt["value"].sum()
    df_mean = input_df.groupby("candidate").apply(lambda x: get_average(
        x, total=total)).reset_index().rename(columns={0: "weight"})

    xx = np.sum(values).reset_index().rename(columns={0: "total"})

    df_within = pd.merge(input_df, df_mean, on="candidate")
    df_within = pd.merge(df_within, xx, on="polling_id")
    df_within["diff_abs"] = np.absolute(
        df_within["rate"] - df_within["weight"])
    df_within["total"] = df_within["value"] * df_within["diff_abs"]

    N_candidates = len(input_df["candidate"].unique())
    df_within = df_within.groupby("candidate").agg(
        {"total": "sum"}) / (N_candidates - 1)

    df_sum = input_df.groupby("candidate").agg(
        {"value": "sum"}).reset_index().rename(columns={"value": "total_votes"})

    df_within = pd.merge(df_within, df_sum, on="candidate")
    df_within = df_within.rename(
        columns={"total": "value", "value": "weight"}
    )
    df_within["value"] = df_within.apply(
        lambda x: x["value"] / x["total_votes"] if x["total_votes"] > 0 else 0, axis=1)
    df_within = df_within.drop(columns=["total_votes"])
    df_within = pd.merge(df_within, df_mean, on="candidate")

    df_within["type"] = "Within"

    return df_within


def within_ps(input_df, alpha=2):
    input_df = input_df.copy()
    values = input_df.pivot(
        index="candidate",
        columns="polling_id",
        values="value"
    )

    total = values.sum().sum()

    def get_average(x, total=1):
        return x["value"].sum() / total

    # total = dt["value"].sum()
    df_mean = input_df.groupby("candidate").apply(lambda x: get_average(
        x, total=total)).reset_index().rename(columns={0: "weight"})

    xx = np.sum(values).reset_index().rename(columns={0: "ww"})

    df_within = pd.merge(input_df, df_mean, on="candidate")
    df_within = pd.merge(df_within, xx, on="polling_id")
    # yy = df_within.groupby("polling_id").agg({"value": "sum"}).reset_index()

    df_within["diff_abs"] = (df_within["rate"] - df_within["weight"]) ** 2
    df_within["total"] = df_within["ww"] * df_within["diff_abs"]

    N_candidates = len(input_df["candidate"].unique())
    N_units = len(input_df["polling_id"].unique())

    df_within = N_candidates * df_within.groupby("candidate").agg(
        {"total": "sum"}) / (N_candidates - 1)

    df_sum = input_df.groupby("candidate").agg(
        {"value": "sum"}).reset_index().rename(columns={"value": "total_votes"})

    df_within = pd.merge(df_within, df_sum, on="candidate")
    df_within = df_within.rename(
        columns={"total": "value", "value": "weight"}
    )
    df_within["value"] = df_within.apply(
        lambda x: x["value"] / total if x["total_votes"] > 0 else 0, axis=1)
    df_within = df_within.drop(columns=["total_votes"])
    df_within = pd.merge(df_within, df_mean, on="candidate")

    df_within["type"] = "Within"

    return df_within
