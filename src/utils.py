from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
import src.c19api as c19api


@st.cache(ttl=30)
def fetch_metadata(category):
    metadata = c19api.metadata(category)

    return metadata


@st.cache(ttl=30)
def fetch_timeseries(category):
    timeseries = c19api.timeseries(category)

    return timeseries


@st.cache(ttl=30)
def ts_confirmed():
    data = fetch_timeseries("confirmed")
    df = pd.DataFrame(data)

    if df.iloc[-1]["new"] == 0:
        df = df[:-1]

    df["date"] = pd.to_datetime(df["date"])
    df["new_sma7"] = df.new.rolling(window=7).mean()
    df = df.rename(columns={"date": "Dato"})

    df = df.melt(
        id_vars=["Dato"],
        value_vars=["new", "new_sma7", "total"],
        var_name="Kategori",
        value_name="Antall",
    ).dropna()

    rename = {"new": "Nye per dag", "new_sma7": "Snitt 7 d.", "total": "Total"}

    df["Kategori"] = df["Kategori"].replace(rename)

    return df


@st.cache(ttl=30)
def ts_dead():
    data = fetch_timeseries("dead")
    df = pd.DataFrame(data)

    idx = pd.date_range("2020-03-07", df["date"].max())
    df.index = pd.DatetimeIndex(df["date"])
    df = df.reindex(idx)
    df["date"] = df.index
    df = df.reset_index(drop=True)

    df["new"] = df["new"].fillna(0).astype(int)
    df["total"] = df["total"].fillna(method="bfill").astype(int)

    df["new_sma7"] = df.new.rolling(window=7).mean()
    df = df.rename(columns={"date": "Dato"})

    df = df.melt(
        id_vars=["Dato"],
        value_vars=["new", "new_sma7", "total"],
        var_name="Kategori",
        value_name="Antall",
    ).dropna()

    rename = {"new": "Nye per dag", "new_sma7": "Snitt 7 d.", "total": "Total"}

    df["Kategori"] = df["Kategori"].replace(rename)

    return df


@st.cache(ttl=30)
def ts_tested():
    data = fetch_timeseries("tested_lab")
    df = pd.DataFrame(data)

    mapping = {
        "date": "Dato",
        "new_neg": "Nye (Negative)",
        "new_pos": "Nye (Positive)",
        "new_total": "Nye",
        "pr100_pos": "Andel Positive",
        "total": "Total",
    }

    df = df.rename(columns=mapping)
    df["Dato"] = pd.to_datetime(df["Dato"])
    df["Andel Negative"] = 100 - df["Andel Positive"]
    df = df.melt(
        id_vars=["Dato", "Andel Positive"], var_name="Kategori", value_name="Antall"
    )

    return df


def thousand_sep(n):
    ret_str = f"{n:,}".replace(",", " ")

    return ret_str


def dateformat(datestr):
    date_time = datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S%z")
    datestr = date_time.strftime(f"{date_time.day}. %b")
    timestr = date_time.strftime("%H:%M")

    ret_str = f"{datestr} kl {timestr}".lower()

    return ret_str


def tested_percent():
    data = fetch_timeseries("tested_lab")

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])

    # last week
    w1_range_max = pd.to_datetime(df["date"].max())
    w1_range_min = w1_range_max - timedelta(days=6)
    df_w1 = df[(df["date"] >= w1_range_min) & (df["date"] <= w1_range_max)]

    w1_mean = round(df_w1["pr100_pos"].mean(), 1)

    # second last week
    w2_range_min = w1_range_min - timedelta(days=7)
    df_w2 = df[(df["date"] >= w2_range_min) & (df["date"] < w1_range_min)]

    w2_mean = round(df_w2["pr100_pos"].mean(), 1)

    date_max = df["date"].max().date()
    datestr = date_max.strftime(f"{date_max.day}. %b")

    return w1_mean, w2_mean, datestr
