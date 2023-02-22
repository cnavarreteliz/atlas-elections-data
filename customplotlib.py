def geoplot(
    input_df,
    ax,
    measure_name="epi"
):
    def set_corr(corr, _):
        corr = round(corr, 3)
        if _ < 0.01:
            return f"ρ={corr}***"
        elif _ < 0.05:
            return f"ρ={corr}**"
        elif _ < 0.1:
            return f"ρ={corr}*"
        return f"ρ={corr}"

    input_df.plot(
        column=measure_name,
        edgecolor="black",
        # vmin=input_df[measure_name].min(),
        # vmax=input_df[measure_name].max(),
        lw=0.75,
        ax=ax,
        cmap="Spectral_r",
        legend=True,
        legend_kwds=dict(
            shrink=0.25
        )
    )

    ax.axis("off")
