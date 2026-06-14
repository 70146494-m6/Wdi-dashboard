"""
app.py — World Development Indicators Dashboard
Course: Exploratory Data Analysis | Instructor: Ali Hassan Sherazi
Data Source: World Bank — DataBank WDI
"""

import streamlit as st
import pandas as pd
import numpy as np

from filters import load_data, apply_filters, get_countries, get_indicators, get_kpis
from charts import (
    chart_pie, chart_histogram, chart_line, chart_bar,
    chart_scatter, chart_box, chart_heatmap, chart_area,
    chart_countplot, chart_violin,
)

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="World Development Indicators Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #e6edf3; }
    .stSidebar { background-color: #161b22; }
    .stSidebar * { color: #e6edf3 !important; }

    .kpi-card {
        background: linear-gradient(135deg, #1f2937 0%, #1a3a5c 100%);
        border: 1px solid #2196F3;
        border-radius: 10px;
        padding: 16px 20px;
        text-align: center;
        margin: 4px 0;
    }
    .kpi-label { font-size: 11px; color: #90caf9; text-transform: uppercase; letter-spacing: 0.5px; }
    .kpi-value { font-size: 22px; font-weight: 700; color: #FF9800; margin-top: 4px; }
    .kpi-sub   { font-size: 10px; color: #90caf9; margin-top: 2px; }

    .section-header {
        font-size: 16px; font-weight: 700; color: #64b5f6;
        border-left: 4px solid #2196F3; padding-left: 10px;
        margin: 20px 0 10px 0;
    }
    label { color: #e6edf3 !important; }
    hr { border-color: #21262d; }
</style>
""", unsafe_allow_html=True)


# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading World Development Indicators...")
def get_data():
    return load_data()

df_all = get_data()
all_countries  = get_countries(df_all, only_countries=True)
all_indicators = get_indicators(df_all)


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🌍 Dashboard Filters")
    st.markdown("---")

    # Indicator selector
    selected_indicators = st.multiselect(
        "📊 Select Indicators",
        options=all_indicators,
        default=all_indicators,
        help="Choose one or more WDI indicators to analyze",
    )

    # Primary indicator for single-indicator charts
    primary_indicator = st.selectbox(
        "🎯 Primary Indicator (for Pie/Line/Bar/Area)",
        options=selected_indicators if selected_indicators else all_indicators,
    )

    st.markdown("---")

    # Year range
    yr_min, yr_max = int(df_all["Year"].min()), int(df_all["Year"].max())
    year_range = st.slider(
        "📅 Year Range",
        min_value=yr_min, max_value=yr_max,
        value=(2000, yr_max), step=1,
    )

    # Country multi-select
    countries = st.multiselect(
        "🌐 Countries",
        options=all_countries,
        default=["Pakistan", "India", "China", "United States",
                 "United Kingdom", "Bangladesh", "Australia",
                 "Canada", "Germany", "France"],
        help="Select countries to include in analysis",
    )

    # Value range slider
    v_min = float(df_all["Value"].quantile(0.01))
    v_max = float(df_all["Value"].quantile(0.99))
    value_range = st.slider(
        "🔢 Value Range",
        min_value=v_min, max_value=v_max,
        value=(v_min, v_max), format="%.2f",
    )

    # Text search
    search_text = st.text_input(
        "🔎 Search (Country / Indicator)",
        placeholder="e.g. Pakistan, GDP, Poverty …",
    )

    st.markdown("---")

    # Reset
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()

    st.markdown("---")
    st.caption("📊 Source: World Bank — DataBank WDI")
    st.caption("🧑‍🎓 EDA Project | Ali Hassan Sherazi")


# ══════════════════════════════════════════════════════════════════════════════
# APPLY FILTERS
# ══════════════════════════════════════════════════════════════════════════════
df = apply_filters(
    df_all,
    year_range=year_range,
    countries=countries if countries else all_countries,
    indicators=selected_indicators if selected_indicators else all_indicators,
    search_text=search_text if search_text else None,
    value_range=value_range,
    only_countries=True,
)


# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    "<h1 style='color:#64b5f6; font-size:2rem; margin-bottom:0;'>🌍 World Development Indicators Dashboard</h1>",
    unsafe_allow_html=True
)
st.markdown(
    f"<p style='color:#90caf9; margin-top:4px;'>"
    f"World Bank DataBank | {year_range[0]}–{year_range[1]} | "
    f"{len(countries) if countries else len(all_countries)} countries | "
    f"<b>{len(df):,}</b> filtered records</p>",
    unsafe_allow_html=True
)
st.markdown("---")


# ══════════════════════════════════════════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════════════════════════════════════════
kpis = get_kpis(df)
k1, k2, k3, k4, k5 = st.columns(5)

def kpi_card(col, label, value, sub=""):
    col.markdown(
        f"""<div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>""",
        unsafe_allow_html=True,
    )

kpi_card(k1, "Total Records",   f"{kpis['total_records']:,}")
kpi_card(k2, "Countries",       f"{kpis['total_countries']}")
kpi_card(k3, "Indicators",      f"{kpis['total_indicators']}")
kpi_card(k4, "Year Span",       kpis["year_span"])
kpi_card(k5, "Highest Country", kpis["max_country"], f"{kpis['max_value']:,.2f}")

st.markdown("<br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1: DISTRIBUTION & PROPORTIONS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">📊 Distribution & Proportions</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.pyplot(chart_pie(df, primary_indicator))
with c2:
    st.pyplot(chart_countplot(df))

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2: TRENDS OVER TIME
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">📈 Trends Over Time</div>', unsafe_allow_html=True)
st.pyplot(chart_line(df, primary_indicator))
st.pyplot(chart_area(df, primary_indicator))

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3: COMPARATIVE ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">🔢 Comparative Analysis</div>', unsafe_allow_html=True)
c3, c4 = st.columns(2)
with c3:
    st.pyplot(chart_bar(df, primary_indicator))
with c4:
    st.pyplot(chart_scatter(df))

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4: STATISTICAL DISTRIBUTION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">📉 Statistical Distribution</div>', unsafe_allow_html=True)
c5, c6 = st.columns(2)
with c5:
    st.pyplot(chart_histogram(df, primary_indicator))
with c6:
    st.pyplot(chart_box(df))

c7, c8 = st.columns(2)
with c7:
    st.pyplot(chart_violin(df))
with c8:
    st.pyplot(chart_heatmap(df))

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# DATA TABLE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">📋 Filtered Data Preview</div>', unsafe_allow_html=True)
show_cols = ["Country Name", "Country Code", "Series Name", "Year", "Value"]
st.dataframe(
    df[show_cols].head(500).reset_index(drop=True),
    use_container_width=True,
    height=300,
)
st.caption(f"Showing first 500 of {len(df):,} filtered records.")

st.markdown("---")
st.markdown(
    "<center><small style='color:#555'>World Development Indicators Dashboard · "
    "World Bank Data · EDA Course Project</small></center>",
    unsafe_allow_html=True,
)
