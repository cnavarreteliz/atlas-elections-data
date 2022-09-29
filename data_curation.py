import json
import pandas as pd


def flip_df(df_fround, df_runoff, df_location, df_dv, country, year, location_level):
    candidate_a, candidate_b = df_runoff["candidate"].unique()
    endorsements = open("endorsement.json", encoding="utf-8")
    endorsements = json.load(endorsements)
    endorsements = endorsements[f"{country}_{year}"]

    results = open("results.json", encoding="utf-8")
    results = json.load(results)
    results = results[f"{country}_{year}"]

    spectrum = open("political_spectrum.json", encoding="utf-8")
    spectrum = json.load(spectrum)
    spectrum = spectrum[f"{country}_{year}"]

    data = pd.merge(df_fround, df_runoff, on=["polling_id", "candidate"])
    data = data.pivot_table(
        index="polling_id",
        columns=["candidate"],
        values=["rate_x", "rate_y"]
    )
    data = data.reset_index()
    data.columns = [f"{a}{b}" for a, b in data.columns]

    data["winner"] = data.apply(
        lambda x: candidate_a if x[f"rate_x{candidate_a}"] > x[f"rate_x{candidate_b}"] else candidate_b,
        axis=1
    )
    data["loser"] = data.apply(
        lambda x: candidate_a if x[f"rate_x{candidate_a}"] < x[f"rate_x{candidate_b}"] else candidate_b,
        axis=1
    )

    data["rate_winner"] = data.apply(
        lambda x: x[f"rate_x{candidate_a}"] if x[f"rate_x{candidate_a}"] > x[f"rate_x{candidate_b}"] else x[f"rate_x{candidate_b}"],
        axis=1
    )
    data["rate_loser"] = data.apply(
        lambda x: x[f"rate_x{candidate_a}"] if x[f"rate_x{candidate_a}"] < x[f"rate_x{candidate_b}"] else x[f"rate_x{candidate_b}"],
        axis=1
    )

    data = pd.merge(data, df_location, on="polling_id")

    data = pd.merge(
        data,
        df_dv[["value", "candidate", location_level]].rename(
            columns={"value": "dv_winner"}),
        left_on=[location_level, "winner"],
        right_on=[location_level, "candidate"]
    )
    data = pd.merge(
        data,
        df_dv.rename(columns={"value": "dv_loser"}),
        left_on=[location_level, "loser"],
        right_on=[location_level, "candidate"]
    )

    endorse_a = endorsements[candidate_a][0] + endorsements[candidate_a][1]
    endorse_b = endorsements[candidate_b][0] + endorsements[candidate_b][1]
    aa = df_fround[df_fround["candidate"].isin(endorse_a)]\
        .groupby("polling_id").agg({"rate": "sum"})
    aa = aa.reset_index().rename(columns={"rate": candidate_a})
    bb = df_fround[df_fround["candidate"].isin(endorse_b)]\
        .groupby("polling_id").agg({"rate": "sum"})
    bb = bb.reset_index().rename(columns={"rate": candidate_b})

    df_endorsement = pd.merge(aa, bb, on="polling_id", how="outer").fillna(0)
    data = pd.merge(data, df_endorsement, on="polling_id")

    # Calculates Endorsement by Extremes
    candidates = spectrum["scale"]
    idx_a = candidates.index(candidate_a)
    idx_b = candidates.index(candidate_b)

    endorse_a = candidates[:idx_a] if spectrum["candidates"][candidate_a] == - \
        1 else candidates[idx_a+1:]
    endorse_b = candidates[:idx_b] if spectrum["candidates"][candidate_b] == - \
        1 else candidates[idx_b+1:]

    aa = df_fround[df_fround["candidate"].isin(endorse_a)]\
        .groupby("polling_id").agg({"rate": "sum"})
    aa = aa.reset_index().rename(columns={"rate": f"rate_ext_{candidate_a}"})
    bb = df_fround[df_fround["candidate"].isin(endorse_b)]\
        .groupby("polling_id").agg({"rate": "sum"})
    bb = bb.reset_index().rename(columns={"rate": f"rate_ext_{candidate_b}"})

    df_endorsement = pd.merge(aa, bb, on="polling_id", how="outer").fillna(0)
    data = pd.merge(data, df_endorsement, on="polling_id")

    # Calculates Divisiveness of Endorsement
    endorse_a = endorsements[candidate_a][0] + endorsements[candidate_a][1]
    endorse_b = endorsements[candidate_b][0] + endorsements[candidate_b][1]

    aa = df_dv[df_dv["candidate"].isin(endorse_a)]\
        .groupby(location_level).agg({"value": "sum"})
    aa = aa.reset_index().rename(columns={"value": f"dv_en_{candidate_a}"})
    bb = df_dv[df_dv["candidate"].isin(endorse_b)]\
        .groupby(location_level).agg({"value": "sum"})
    bb = bb.reset_index().rename(columns={"value": f"dv_en_{candidate_b}"})

    df_endorsement = pd.merge(aa, bb, on=location_level, how="outer").fillna(0)
    data = pd.merge(data, df_endorsement, on=location_level)

    # Calculates Divisiveness of Extremes
    endorse_a = candidates[:idx_a] if spectrum["candidates"][candidate_a] == - \
        1 else candidates[idx_a+1:]
    endorse_b = candidates[:idx_b] if spectrum["candidates"][candidate_b] == - \
        1 else candidates[idx_b+1:]

    aa = df_dv[df_dv["candidate"].isin(endorse_a)]\
        .groupby(location_level).agg({"value": "sum"})
    aa = aa.reset_index().rename(columns={"value": f"dv_ext_{candidate_a}"})
    bb = df_dv[df_dv["candidate"].isin(endorse_b)]\
        .groupby(location_level).agg({"value": "sum"})
    bb = bb.reset_index().rename(columns={"value": f"dv_ext_{candidate_b}"})

    df_endorsement = pd.merge(aa, bb, on=location_level, how="outer").fillna(0)

    if df_endorsement.shape[0] > 0:
        data = pd.merge(data, df_endorsement, on=location_level, how="outer")

    data["en_winner"] = data.apply(
        lambda x: x[candidate_a] if x[f"rate_x{candidate_a}"] > x[f"rate_x{candidate_b}"] else x[candidate_b],
        axis=1
    )
    data["en_loser"] = data.apply(
        lambda x: x[candidate_a] if x[f"rate_x{candidate_a}"] < x[f"rate_x{candidate_b}"] else x[candidate_b],
        axis=1
    )

    data["en_dv_winner"] = data.apply(
        lambda x: x[f"dv_en_{candidate_a}"] if x[f"rate_x{candidate_a}"] > x[f"rate_x{candidate_b}"] else x[f"dv_en_{candidate_b}"],
        axis=1
    )
    data["en_dv_loser"] = data.apply(
        lambda x: x[f"dv_en_{candidate_a}"] if x[f"rate_x{candidate_a}"] < x[f"rate_x{candidate_b}"] else x[f"dv_en_{candidate_b}"],
        axis=1
    )

    data["en_winner_2"] = data.apply(
        lambda x: x[f"rate_ext_{candidate_a}"] if x[f"rate_x{candidate_a}"] > x[
            f"rate_x{candidate_b}"] else x[f"rate_ext_{candidate_b}"],
        axis=1
    )
    data["en_loser_2"] = data.apply(
        lambda x: x[f"rate_ext_{candidate_a}"] if x[f"rate_x{candidate_a}"] < x[
            f"rate_x{candidate_b}"] else x[f"rate_ext_{candidate_b}"],
        axis=1
    )

    if f"dv_ext_{candidate_a}" in list(data):
        data["en_dv_winner_2"] = data.apply(
            lambda x: x[f"dv_ext_{candidate_a}"] if x[f"rate_x{candidate_a}"] > x[
                f"rate_x{candidate_b}"] else x[f"dv_ext_{candidate_b}"],
            axis=1
        )
        data["en_dv_loser_2"] = data.apply(
            lambda x: x[f"dv_ext_{candidate_a}"] if x[f"rate_x{candidate_a}"] < x[
                f"rate_x{candidate_b}"] else x[f"dv_ext_{candidate_b}"],
            axis=1
        )

    data["polling_winner_fround"] = (data["winner"] == results[0]).astype(int)
    data["polling_winner_election"] = (
        data["winner"] == results[2]).astype(int)

    data["flip"] = ((data[f"rate_x{candidate_a}"] > data[f"rate_x{candidate_b}"]) & (data[f"rate_y{candidate_a}"] < data[f"rate_y{candidate_b}"])) |\
        ((data[f"rate_x{candidate_b}"] > data[f"rate_x{candidate_a}"]) & (
            data[f"rate_y{candidate_b}"] < data[f"rate_y{candidate_a}"]))

    data["flip"] = data["flip"].astype(int)
    data = pd.merge(
        data,
        data.groupby(location_level).agg({"flip": "mean"}).reset_index().rename(
            columns={"flip": "flip_neighbors"}),
        on=location_level
    )

    df_polarization = df_dv.groupby(location_level).agg(
        {"value": "mean"}).rename(columns={"value": "polarization"}).reset_index()
    data = pd.merge(data, df_polarization, on=location_level)

    # data = data.drop(
    #     columns=[
    #         f"rate_x{candidate_a}",
    #         f"rate_x{candidate_b}",
    #         f"rate_ext_{candidate_a}",
    #         f"rate_ext_{candidate_b}",
    #         f"dv_ext_{candidate_a}",
    #         f"dv_ext_{candidate_b}",
    #         candidate_a,
    #         candidate_b
    #     ])

    data.to_csv(
        f"data_regressions/{country}_{year}_flip.csv.gz",
        compression="gzip",
        index=False
    )

    return data
