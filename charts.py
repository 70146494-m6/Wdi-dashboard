"""
charts.py — All 10 required chart types
World Development Indicators Dashboard
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# ── Global Style ──────────────────────────────────────────────────────────────
PALETTE = [
    "#2196F3", "#4CAF50", "#FF9800", "#E91E63",
    "#9C27B0", "#00BCD4", "#FF5722", "#8BC34A",
    "#FFC107", "#3F51B5",
]
BG    = "#0d1117"
FG    = "#e6edf3"
GRID  = "#21262d"
ACC   = "#2196F3"


def _style(fig, axes):
    fig.patch.set_facecolor(BG)
    axlist = axes if hasattr(axes, "__iter__") else [axes]
    for ax in axlist:
        ax.set_facecolor(BG)
        ax.tick_params(colors=FG, labelsize=9)
        ax.xaxis.label.set_color(FG)
        ax.yaxis.label.set_color(FG)
        ax.title.set_color(FG)
        for sp in ax.spines.values():
            sp.set_edgecolor(GRID)
        ax.grid(color=GRID, linewidth=0.5, linestyle="--", alpha=0.6)


def _fig(w=9, h=5):
    return plt.subplots(figsize=(w, h))


# ── 1. PIE CHART ─────────────────────────────────────────────────────────────
def chart_pie(df: pd.DataFrame, indicator: str = None) -> plt.Figure:
    if indicator:
        data = df[df["Series Name"] == indicator]
    else:
        data = df

    top = (
        data.groupby("Country Name")["Value"].mean()
        .nlargest(8)
    )
    ind_label = indicator if indicator else "Selected Indicator"
    fig, ax = _fig(8, 6)
    wedges, texts, autotexts = ax.pie(
        top.values,
        labels=top.index,
        autopct="%1.1f%%",
        colors=PALETTE[:len(top)],
        startangle=140,
        wedgeprops=dict(edgecolor=BG, linewidth=1.5),
    )
    for t in texts:
        t.set_color(FG); t.set_fontsize(9)
    for at in autotexts:
        at.set_color(FG); at.set_fontsize(8)
    ax.set_title(f"Top 8 Countries — {ind_label}", color=FG, fontsize=12, fontweight="bold", pad=12)
    _style(fig, ax)
    ax.grid(False)
    fig.tight_layout()
    return fig


# ── 2. HISTOGRAM ─────────────────────────────────────────────────────────────
def chart_histogram(df: pd.DataFrame, indicator: str = None) -> plt.Figure:
    data = df[df["Series Name"] == indicator]["Value"].dropna() if indicator else df["Value"].dropna()
    ind_label = indicator if indicator else "All Indicators"
    fig, ax = _fig()
    ax.hist(data, bins=40, color=ACC, edgecolor=BG, alpha=0.85)
    ax.set_xlabel("Value", color=FG)
    ax.set_ylabel("Frequency", color=FG)
    ax.set_title(f"Value Distribution — {ind_label}", color=FG, fontsize=12, fontweight="bold")
    _style(fig, ax)
    fig.tight_layout()
    return fig


# ── 3. LINE CHART ─────────────────────────────────────────────────────────────
def chart_line(df: pd.DataFrame, indicator: str = None, top_n: int = 8) -> plt.Figure:
    data = df[df["Series Name"] == indicator] if indicator else df
    ind_label = indicator if indicator else "Selected Indicators"
    top_countries = data.groupby("Country Name")["Value"].mean().nlargest(top_n).index
    data = data[data["Country Name"].isin(top_countries)]
    trend = data.groupby(["Year", "Country Name"])["Value"].mean().reset_index()

    fig, ax = _fig(10, 5)
    for i, country in enumerate(top_countries):
        sub = trend[trend["Country Name"] == country].sort_values("Year")
        ax.plot(sub["Year"], sub["Value"], marker="o", markersize=3,
                linewidth=2, label=country, color=PALETTE[i % len(PALETTE)])
    ax.set_xlabel("Year", color=FG)
    ax.set_ylabel("Value", color=FG)
    ax.set_title(f"Trends Over Time — {ind_label}", color=FG, fontsize=12, fontweight="bold")
    ax.legend(fontsize=8, framealpha=0.2, labelcolor=FG, facecolor=BG)
    _style(fig, ax)
    fig.tight_layout()
    return fig


# ── 4. BAR CHART ─────────────────────────────────────────────────────────────
def chart_bar(df: pd.DataFrame, indicator: str = None) -> plt.Figure:
    data = df[df["Series Name"] == indicator] if indicator else df
    ind_label = indicator if indicator else "All"
    top = data.groupby("Country Name")["Value"].mean().nlargest(15).sort_values()

    fig, ax = _fig(9, 6)
    ax.barh(top.index, top.values, color=PALETTE[:len(top)], edgecolor=BG, height=0.7)
    ax.set_xlabel("Average Value", color=FG)
    ax.set_title(f"Top 15 Countries — {ind_label}", color=FG, fontsize=12, fontweight="bold")
    _style(fig, ax)
    fig.tight_layout()
    return fig


# ── 5. SCATTER PLOT ──────────────────────────────────────────────────────────
def chart_scatter(df: pd.DataFrame) -> plt.Figure:
    indicators = df["Series Name"].unique()
    if len(indicators) >= 2:
        ind1, ind2 = indicators[0], indicators[1]
        d1 = df[df["Series Name"] == ind1].groupby("Country Name")["Value"].mean()
        d2 = df[df["Series Name"] == ind2].groupby("Country Name")["Value"].mean()
        merged = pd.concat([d1, d2], axis=1).dropna()
        merged.columns = [ind1, ind2]
        xlabel, ylabel = ind1[:40], ind2[:40]
    else:
        merged = df.groupby(["Country Name", "Year"])["Value"].mean().unstack().T
        xlabel, ylabel = "Year", "Value"
        fig, ax = _fig()
        ax.scatter(df["Year"], df["Value"], color=ACC, alpha=0.5, s=20)
        ax.set_xlabel("Year", color=FG)
        ax.set_ylabel("Value", color=FG)
        ax.set_title("Year vs Value (Scatter)", color=FG, fontsize=12, fontweight="bold")
        _style(fig, ax)
        fig.tight_layout()
        return fig

    fig, ax = _fig(9, 5)
    ax.scatter(merged.iloc[:, 0], merged.iloc[:, 1], color=ACC, alpha=0.7, s=50, edgecolors=BG)
    ax.set_xlabel(xlabel, color=FG, fontsize=9)
    ax.set_ylabel(ylabel, color=FG, fontsize=9)
    ax.set_title("Scatter: Indicator vs Indicator", color=FG, fontsize=12, fontweight="bold")
    _style(fig, ax)
    fig.tight_layout()
    return fig


# ── 6. BOX PLOT ──────────────────────────────────────────────────────────────
def chart_box(df: pd.DataFrame) -> plt.Figure:
    indicators = df["Series Name"].unique().tolist()
    fig, ax = _fig(9, 5)
    bp_data = [df[df["Series Name"] == ind]["Value"].dropna().values for ind in indicators]
    bp_data = [d for d in bp_data if len(d) > 0]
    short_labels = [ind[:25] + "…" if len(ind) > 25 else ind for ind in indicators[:len(bp_data)]]

    bp = ax.boxplot(bp_data, labels=short_labels, patch_artist=True,
                    medianprops=dict(color="#FF9800", linewidth=2))
    for patch, color in zip(bp["boxes"], PALETTE):
        patch.set_facecolor(color)
        patch.set_alpha(0.8)
    ax.set_xlabel("Indicator", color=FG)
    ax.set_ylabel("Value", color=FG)
    ax.set_title("Value Distribution by Indicator (Box Plot)", color=FG, fontsize=12, fontweight="bold")
    plt.xticks(rotation=15, ha="right", fontsize=8)
    _style(fig, ax)
    fig.tight_layout()
    return fig


# ── 7. HEATMAP ───────────────────────────────────────────────────────────────
def chart_heatmap(df: pd.DataFrame, top_n: int = 12) -> plt.Figure:
    top_countries = df.groupby("Country Name")["Value"].mean().nlargest(top_n).index
    data = df[df["Country Name"].isin(top_countries)]
    data = data[data["Year"] >= 2000]
    pivot = data.groupby(["Country Name", "Year"])["Value"].mean().unstack(fill_value=np.nan)

    fig, ax = _fig(11, 6)
    sns.heatmap(pivot, ax=ax, cmap="YlOrRd", linewidths=0.3,
                linecolor=BG, cbar_kws={"shrink": 0.8}, yticklabels=True)
    ax.set_title(f"Heatmap: Top {top_n} Countries × Year (2000+)", color=FG, fontsize=12, fontweight="bold")
    ax.set_xlabel("Year", color=FG)
    ax.set_ylabel("Country", color=FG)
    ax.tick_params(colors=FG, labelsize=8)
    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(colors=FG)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    fig.tight_layout()
    return fig


# ── 8. AREA CHART ────────────────────────────────────────────────────────────
def chart_area(df: pd.DataFrame, indicator: str = None, top_n: int = 6) -> plt.Figure:
    data = df[df["Series Name"] == indicator] if indicator else df
    ind_label = indicator if indicator else "All"
    top_countries = data.groupby("Country Name")["Value"].mean().nlargest(top_n).index
    area_data = (
        data[data["Country Name"].isin(top_countries)]
        .groupby(["Year", "Country Name"])["Value"].mean()
        .unstack(fill_value=0)
        .sort_index()
    )
    fig, ax = _fig(10, 5)
    ax.stackplot(area_data.index, area_data.T.values,
                 labels=area_data.columns,
                 colors=PALETTE[:len(area_data.columns)], alpha=0.8)
    ax.set_xlabel("Year", color=FG)
    ax.set_ylabel("Value", color=FG)
    ax.set_title(f"Cumulative Trends — {ind_label}", color=FG, fontsize=12, fontweight="bold")
    ax.legend(fontsize=8, loc="upper left", framealpha=0.2, labelcolor=FG, facecolor=BG)
    _style(fig, ax)
    fig.tight_layout()
    return fig


# ── 9. COUNT PLOT ─────────────────────────────────────────────────────────────
def chart_countplot(df: pd.DataFrame) -> plt.Figure:
    counts = df["Series Name"].value_counts()
    short_labels = [lbl[:30] + "…" if len(lbl) > 30 else lbl for lbl in counts.index]

    fig, ax = _fig(9, 5)
    ax.bar(short_labels, counts.values, color=PALETTE[:len(counts)], edgecolor=BG, width=0.6)
    ax.set_xlabel("Indicator", color=FG)
    ax.set_ylabel("Record Count", color=FG)
    ax.set_title("Records Count by Indicator", color=FG, fontsize=12, fontweight="bold")
    plt.xticks(rotation=20, ha="right", fontsize=8)
    _style(fig, ax)
    fig.tight_layout()
    return fig


# ── 10. VIOLIN PLOT ──────────────────────────────────────────────────────────
def chart_violin(df: pd.DataFrame) -> plt.Figure:
    indicators = df["Series Name"].unique().tolist()
    vdata = [df[df["Series Name"] == ind]["Value"].dropna().values for ind in indicators]
    vdata = [d for d in vdata if len(d) > 1]
    short_labels = [ind[:25] + "…" if len(ind) > 25 else ind for ind in indicators[:len(vdata)]]

    fig, ax = _fig(9, 5)
    parts = ax.violinplot(vdata, positions=range(len(vdata)),
                          showmedians=True, showmeans=False)
    for i, pc in enumerate(parts["bodies"]):
        pc.set_facecolor(PALETTE[i % len(PALETTE)])
        pc.set_alpha(0.8)
    parts["cmedians"].set_color("#FF9800")
    parts["cmaxes"].set_color(FG)
    parts["cmins"].set_color(FG)
    parts["cbars"].set_color(FG)
    ax.set_xticks(range(len(short_labels)))
    ax.set_xticklabels(short_labels, rotation=15, ha="right", fontsize=8)
    ax.set_xlabel("Indicator", color=FG)
    ax.set_ylabel("Value", color=FG)
    ax.set_title("Value Density by Indicator (Violin Plot)", color=FG, fontsize=12, fontweight="bold")
    _style(fig, ax)
    fig.tight_layout()
    return fig
