import streamlit as st
import pandas as pd
import numpy as np

from filters import load_data, apply_filters, get_countries, get_indicators, get_kpis
from charts import (
    chart_pie, chart_histogram, chart_line, chart_bar,
    chart_scatter, chart_box, chart_heatmap, chart_area,
    chart_countplot, chart_violin,
)

st.set_page_config(
    page_title="WDI Analytics Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

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


@st.cache_data(show_spinner="Loading World Development Indicators...")
def get_data():
    return load_data()

df_all = get_data()
all_countries  = get_countries(df_all, only_countries=True)
all_indicators = get_indicators(df_all)

DEFAULT_COUNTRIES = [c for c in ["Pakistan", "India", "China", "United States",
                 "United Kingdom", "Bangladesh", "Australia",
                 "Canada", "Germany", "France"] if c in all_countries]

with st.sidebar:
    st.markdown("## 🌍 Dashboard Filters")
    st.markdown("---")

    selected_indicators = st.multiselect(
        "📊 Select Indicators",
        options=all_indicators,
        default=all_indicators[:3] if len(all_indicators) >= 3 else all_indicators,
    )

    primary_indicator = st.selectbox(
        "🎯 Primary Indicator",
        options=selected_indicators if selected_indicators else all_indicators,
    )

    st.markdown("---")

    yr_min, yr_max = int(df_all["Year"].min()), int(df_all["Year"].max())
    year_range = st.slider("📅 Year Range", min_value=yr_min, max_value=yr_max, value=(2000, yr_max), step=1)

    countries = st.multiselect(
        "🌐 Countries",
        options=all_countries,
        default=DEFAULT_COUNTRIES,
    )

    v_min = float(df_all["Value"].quantile(0.01))
    v_max = float(df_all["Value"].quantile(0.99))
    value_range = st.slider("🔢 Value Range", min_value=v_min, max_value=v_max, value=(v_min, v_max), format="%.2f")

    search_text = st.text_input("🔎 Search", placeholder="e.g. Pakistan, GDP ...")

    st.markdown("---")
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()

    st.caption("📊 Source: World Bank — DataBank WDI")


df = apply_filters(
    df_all,
    year_range=year_range,
    countries=countries if countries else all_countries,
    indicators=selected_indicators if selected_indicators else all_indicators,
    search_text=search_text if search_text else None,
    value_range=value_range,
    only_countries=True,
)

st.markdown("<h1 style='color:#64b5f6; font-size:2rem; margin-bottom:0;'>🌍 World Development Indicators Dashboard</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color:#90caf9; margin-top:4px;'>World Bank DataBank | {year_range[0]}–{year_range[1]} | {len(countries) if countries else len(all_countries)} countries | <b>{len(df):,}</b> filtered records</p>", unsafe_allow_html=True)
st.markdown("---")

kpis = get_kpis(df)
k1, k2, k3, k4, k5 = st.columns(5)

def kpi_card(col, label, value, sub=""):
    col.markdown(f"""<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-sub">{sub
