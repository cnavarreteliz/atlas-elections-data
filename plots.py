from scipy.stats import pearsonr

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def set_plot(dt, ax, xlabel="", ylabel="", labelkey=None):
    dt = dt.copy()
    dt["diff"] = np.absolute(dt["x"] - dt["y"])

    sns.set(font_scale=2, style="ticks")

    g = sns.scatterplot(
        x="x", 
        y="y", 
        hue="type", 
        hue_order=["ec", "ep"], 
        data=dt, 
        legend=False,
        linewidth=0,
        palette=["#385a7c", "#f97171"], 
        s=120,
        style="type", 
        zorder=2,
        ax=ax
    )

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    v = max(np.abs(dt.x.max()), np.abs(dt.x.min()), np.abs(dt.y.max()), np.abs(dt.y.min())) + 0.15

    ax.set_xlim(-v, v)
    ax.set_ylim(-v, v)

    ax.plot([-v, v], [-v, v], color="gray", ls="--", transform=ax.transAxes, zorder=1)

    pos = 0.975
    for i, dd in dt.groupby("type"):
        corr, pvalue = pearsonr(dd["x"], dd["y"])
        def corrfunc(pvalue):
            if pvalue < 0.001:
                return "$P$ < 0.001"
            else:
                return f"$P$ = {round(pvalue, 3)}"

        labels = {"ec": "EC", "ep": "EP"}
        val = corrfunc(pvalue)
        
        ax.text(0.025, pos, f"$ρ_{{{labels[i]}}}$ = {round(corr, 3)} ({val})", transform=ax.transAxes, va="top", fontsize=20)
        pos -= 0.05

    ax.text(0.025, 0.05, "x=y", transform=ax.transAxes, va="top", fontsize=16)

    if labelkey:
        for i, item in dt.sort_values("diff", ascending=False).head().iterrows():
            ax.text(item["x"] + 0.05, item["y"], item[labelkey], va="center", fontsize=16)

    return 