import pandas as pd
import numpy as np
import os

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "245b6253-2c4c-4eac-a990-ddcef4769577_Data.csv")

AGGREGATES = [
    "World", "income", "Asia", "Europe", "Africa", "America", "Arab",
    "Caribbean", "Pacific", "OECD", "IDA", "IBRD", "dividend", "states",
    "classified", "Euro area", "Fragile", "Heavily", "Least", "Middle East",
    "South Asia", "Sub-Saharan", "North America", "Latin America",
    "Central Europe", "East Asia", "European Union",
]


def _is_aggregate(name):
    if not isinstance(name, str):
        return True
    for kw in AGGREGATES:
        if kw.lower() in name.lower():
            return True
    return False


def load_data():
    df = pd.read_csv(DATA_FILE, encoding="latin1")
    df = df[df["Country Code"].apply(lambda x: isinstance(x, str) and len(str(x)) <= 5)]
    df = df.dropna(subset=["Series Name", "Country Name"])
    df = df[df["Series Name"].notna()]
    df = df[df["Country Name"].notna()]
    year_cols = [c for c in df.columns if "[YR" in str(c)]
    df_long = df.melt(
        id_vars=["Country Name", "Country Code", "Series Name", "Series Code"],
        value_vars=year_cols,
        var_name="Year_Label",
        value_name="Value",
    )
    df_long["Year"] = df_long["Year_Label"].str.extract(r"(\d{4})").astype(int)
    df_long["Value"] = pd.to_numeric(df_long["Value"].replace("..", np.nan), errors="coerce")
    df_long = df_long.dropna(subset=["Value"])
    df_long["Is_Country"] = ~df_long["Country Name"].apply(_is_aggregate)
    return df_long.reset_index(drop=True)


def get_countries(df, only_countries=True):
    if only_countries:
        return sorted(df[df["Is_Country"]]["Country Name"].unique().tolist())
    return sorted(df["Country Name"].unique().tolist())


def get_indicators(df):
    return sorted(df["Series Name"].unique().tolist())


def apply_filters(df, year_range=None, countries=None, indicators=None, search_text=None, value_range=None, only_countries=True):
    filtered = df.copy()
    if only_countries:
        filtered = filtered[filtered["Is_Country"]]
    if year_range:
        filtered = filtered[(filtered["Year"] >= year_range[0]) & (filtered["Year"] <= year_range[1])]
    if countries and len(countries) > 0:
        filtered = filtered[filtered["Country Name"].isin(countries)]
    if indicators and len(indicators) > 0:
        filtered = filtered[filtered["Series Name"].isin(indicators)]
    if search_text and search_text.strip():
        mask = (
            filtered["Country Name"].str.contains(search_text, case=False, na=False) |
            filtered["Series Name"].str.contains(search_text, case=False, na=False)
        )
        filtered = filtered[mask]
    if value_range:
        filtered = filtered[(filtered["Value"] >= value_range[0]) & (filtered["Value"] <= value_range[1])]
    return filtered.reset_index(drop=True)


def get_kpis(df):
    return {
        "total_records": len(df),
        "total_countries": df["Country Name"].nunique(),
        "total_indicators": df["Series Name"].nunique(),
        "year_span": f"{int(df['Year'].min())} - {int(df['Year'].max())}" if len(df) else "-",
        "avg_value": df["Value"].mean(),
        "max_value": df["Value"].max(),
        "max_country": df.loc[df["Value"].idxmax(), "Country Name"] if len(df) else "-",
        "min_value": df["Value"].min(),
    }
