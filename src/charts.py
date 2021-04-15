from datetime import timedelta
import pandas as pd
import altair as alt
from src.utils import fetch_timeseries, ts_confirmed, ts_dead, ts_tested


def tested(cummulative, period):
    df = ts_tested()

    if period != 0:
        df = df[(df["Dato"] >= (df["Dato"].max() - timedelta(days=period)))]

    base = alt.Chart(df).encode(
        alt.X("yearmonthdate(Dato):O", axis=alt.Axis(title=None, labelAngle=-40))
    )

    if cummulative == "Nye per dag":
        andel = base.mark_line(color="red", opacity=0.8).encode(
            y=alt.Y("Andel Positive:Q", title="% Positive", axis=alt.Axis(grid=True)),
            tooltip=["Dato", "Andel Positive"],
        )

        bar = (
            base.transform_filter(
                (alt.datum.Kategori == "Nye (Negative)")
                | (alt.datum.Kategori == "Nye (Positive)")
            )
            .mark_bar()
            .encode(
                y=alt.Y(
                    "Antall:Q",
                    title="Antall personer testet for covid-19 per dag",
                ),
                color=alt.Color(
                    "Kategori:N",
                    scale=alt.Scale(
                        domain=["Nye (Positive)", "Nye (Negative)", "% Positive"],
                        range=["#FF9622", "#6DA9FF", "red"],
                    ),
                    legend=alt.Legend(title=None),
                ),
                tooltip=["Dato", "Antall"],
            )
        )

        chart = (
            alt.layer(bar, andel)
            .resolve_scale(y="independent")
            .properties(
                height=400,
            )
            .configure_legend(orient="bottom")
        )
    else:
        chart = (
            base.transform_filter(alt.datum.Kategori == cummulative)
            .mark_bar(color="red")
            .encode(
                y=alt.Y("Antall:Q", axis=alt.Axis(title="Antall", grid=True)),
                tooltip=["Dato", "Antall"],
            )
        )

    return chart


def confirmed(cummulative, period):
    df = ts_confirmed()

    if period != 0:
        df = df[(df["Dato"] >= (df["Dato"].max() - timedelta(days=period)))]

    alt.renderers.set_embed_options(actions=False)
    base = alt.Chart(df).encode(
        alt.X("yearmonthdate(Dato):O", axis=alt.Axis(title=None, labelAngle=-40))
    )

    bar = (
        base.transform_filter(alt.datum.Kategori == cummulative)
        .mark_bar(color="#FFD1D1")
        .encode(
            y=alt.Y("Antall:Q", axis=alt.Axis(title="Antall", grid=True)),
            tooltip=["Dato", "Antall"],
        )
    )

    if cummulative == "Nye per dag":
        ma7 = (
            base.transform_filter(alt.datum.Kategori == "Snitt 7 d.")
            .mark_line(opacity=0.8)
            .encode(
                y=alt.Y("Antall:Q"),
                color=alt.Color(
                    "Kategori:N",
                    scale=alt.Scale(
                        domain=["Nye per dag", "Snitt 7 d."], range=["#FFD1D1", "red"]
                    ),
                    legend=alt.Legend(title=None),
                ),
            )
        )

        chart = (
            alt.layer(bar + ma7)
            .resolve_scale(y="independent")
            .properties(height=400)
            .configure_legend(orient="bottom")
        )
    else:
        chart = (
            base.transform_filter(alt.datum.Kategori == cummulative)
            .mark_bar(color="red")
            .encode(
                y=alt.Y("Antall:Q", axis=alt.Axis(title="Antall", grid=True)),
                tooltip=["Dato", "Antall"],
            )
            .properties(height=400)
            .configure_legend(orient="bottom")
        )

    return chart


def dead(cummulative, period):
    df = ts_dead()

    if period != 0:
        df = df[(df["Dato"] >= (df["Dato"].max() - timedelta(days=period)))]

    alt.renderers.set_embed_options(actions=False)
    base = alt.Chart(df).encode(
        alt.X("yearmonthdate(Dato):O", axis=alt.Axis(title=None, labelAngle=-40))
    )

    if cummulative == "Nye per dag":
        bar = (
            base.transform_filter(alt.datum.Kategori == cummulative)
            .mark_bar(color="#FFD1D1")
            .encode(
                y=alt.Y("Antall:Q", axis=alt.Axis(title="Antall", grid=True)),
                tooltip=["Dato", "Antall"],
            )
        )

        ma7 = (
            base.transform_filter(alt.datum.Kategori == "Snitt 7 d.")
            .mark_line(opacity=0.8)
            .encode(
                y=alt.Y("Antall:Q"),
                color=alt.Color(
                    "Kategori:N",
                    scale=alt.Scale(
                        domain=["Nye per dag", "Snitt 7 d."], range=["#FFD1D1", "red"]
                    ),
                    legend=alt.Legend(title=None),
                ),
            )
        )

        chart = (
            alt.layer(bar + ma7)
            .resolve_scale(y="independent")
            .properties(height=400)
            .configure_legend(orient="bottom")
        )
    else:
        bar = (
            base.transform_filter(alt.datum.Kategori == cummulative)
            .mark_bar(color="red")
            .encode(
                y=alt.Y("Antall:Q", axis=alt.Axis(title="Antall", grid=True)),
                tooltip=["Dato", "Antall"],
            )
        )

        chart = bar.properties(height=400).configure_legend(orient="bottom")

    return chart


def hospitalized(period):
    data = fetch_timeseries("hospitalized")
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])

    if period != 0:
        df = df[(df["date"] >= (df["date"].max() - timedelta(days=period)))]

    df["admissions"] = df["admissions"].fillna(method="ffill").astype(int)
    df["respiratory"] = df["respiratory"].fillna(method="ffill").astype(int)

    df_melt = pd.melt(
        df,
        id_vars=["date"],
        value_vars=["admissions", "respiratory"],
        value_name="value",
    ).replace({"admissions": "Innlagt", "respiratory": "På respirator"})

    chart = (
        alt.Chart(
            df_melt,
        )
        .mark_area(line={}, opacity=0.3)
        .encode(
            x=alt.X("yearmonthdate(date):O", axis=alt.Axis(title=None, labelAngle=-40)),
            y=alt.Y(
                "value:Q",
                stack=None,
                title="Antall innlagte med påvist COVID-19 i Norge",
            ),
            color=alt.Color(
                "variable:N",
                scale=alt.Scale(
                    domain=["Innlagt", "På respirator"], range=["#5A9DFF", "#FF8B1B"]
                ),
                legend=alt.Legend(title=None),
            ),
            tooltip=["date", "variable", "value"],
        )
        .properties(height=400)
        .configure_legend(orient="bottom")
    )

    return chart
