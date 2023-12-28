from scipy.stats import pearsonr

import matplotlib.pyplot as plt
import seaborn as sns


def set_plot(dt):
    sns.set(font_scale=2, style="ticks")

    fig, ax = plt.subplots(figsize=(9, 9), dpi=400)

    g = sns.scatterplot(
        x="x",  y="y", hue="type", 
        hue_order=["ec", "ep"], 
        style="type", 
        s=120,
        linewidth=0,
        palette=["#385a7c", "#f97171"], 
        legend=False,
        data=dt, zorder=2
    )
    g.set_xlabel("Value using U.S. Presidential")
    g.set_ylabel("Value using U.S. Senate")

    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)

    ax.plot([0, 1], [0, 1], color="gray", ls="--", transform=ax.transAxes, zorder=1)


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

    ax.text(0.025, 0.03, "x=y", transform=ax.transAxes, va="top", fontsize=16)