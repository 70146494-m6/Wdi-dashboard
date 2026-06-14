"""
filters.py — Data loading, cleaning, and filtering functions
World Development Indicators Dashboard
"""

import pandas as pd
import numpy as np
import os


# Known regional/aggregate group keywords to exclude from country lists
AGGREGATES = [
    "World", "income", "Asia", "Europe", "Africa", "America", "Arab",
    "Caribbean", "Pacific", "OECD", "IDA", "IBRD", "dividend", "states",
    "classified", "Euro area", "Fragile", "Heavily", "Least", "Middle East",
    "South Asia", "Sub-Saharan", "North America", "Latin America",
    "Central Europe", "East Asia", "European Union",
]


def _is_aggregate(name: str) -> bool:
    if not isinstance(name, str):
        return True
    for kw in AGGREGATES:
        if kw.lower() in name.lower():
            return True
    return False


def load_data() -> pd.DataFrame:
    """Load and melt WDI data into long format."""
    df = pd.read_csv(DATA_FILE, encoding="latin1")

    # Drop footer rows (Last Updated etc.)
    df = df[df["Country Code"].apply(lambda x: isinstance(x, str) and len(str(x)) <= 5)]
    df = df.dropna(subset=["Series Name", "Country Name"])
    df = df[df["Series Name"].notna()]
    df = df[df["Country Name"].notna()]

    # Identify year columns
    year_cols = [c for c in df.columns if "[YR" in str(c)]

    # Melt to long format
    df_long = df.melt(
        id_vars=["Country Name", "Country Code", "Series Name", "Series Code"],
        value_vars=year_cols,
        var_name="Year_Label",
        value_name="Value",
    )

    # Extract year as int
    df_long["Year"] = df_long["Year_Label"].str.extract(r"(\d{4})").astype(int)

    # Clean Value
    df_long["Value"] = pd.to_numeric(df_long["Value"].replace("..", np.nan), errors="coerce")
    df_long = df_long.dropna(subset=["Value"])

    # Add region flag
    df_long["Is_Country"] = ~df_long["Country Name"].apply(_is_aggregate)

    return df_long.reset_index(drop=True)


def get_countries(df: pd.DataFrame, only_countries: bool = True) -> list:
    if only_countries:
        return sorted(df[df["Is_Country"]]["Country Name"].unique().tolist())
    return sorted(df["Country Name"].unique().tolist())


def get_indicators(df: pd.DataFrame) -> list:
    return sorted(df["Series Name"].unique().tolist())


def apply_filters(
    df: pd.DataFrame,
    year_range: tuple = None,
    countries: list = None,
    indicators: list = None,
    search_text: str = None,
    value_range: tuple = None,
    only_countries: bool = True,
) -> pd.DataFrame:
    """Apply all sidebar filters."""
    filtered = df.copy()

    if only_countries:
        filtered = filtered[filtered["Is_Country"]]

    if year_range:
        filtered = filtered[
            (filtered["Year"] >= year_range[0]) &
            (filtered["Year"] <= year_range[1])
        ]

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
        filtered = filtered[
            (filtered["Value"] >= value_range[0]) &
            (filtered["Value"] <= value_range[1])
        ]

    return filtered.reset_index(drop=True)


def get_kpis(df: pd.DataFrame) -> dict:
    return {
        "total_records": len(df),
        "total_countries": df["Country Name"].nunique(),
        "total_indicators": df["Series Name"].nunique(),
        "year_span": f"{int(df['Year'].min())} – {int(df['Year'].max())}" if len(df) else "—",
        "avg_value": df["Value"].mean(),
        "max_value": df["Value"].max(),
        "max_country": df.loc[df["Value"].idxmax(), "Country Name"] if len(df) else "—",
        "min_value": df["Value"].min(),
    }
