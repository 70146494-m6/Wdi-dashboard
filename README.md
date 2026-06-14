# 🌍 World Development Indicators Dashboard
---
## 📁 Project Structure

```
wdi_dashboard/
├── data/
│   ├── 245b6253-2c4c-4eac-a990-ddcef4769577_Data.csv
│   └── 245b6253-2c4c-4eac-a990-ddcef4769577_Series_-_Metadata.csv
├── app.py          ← Main Streamlit dashboard
├── charts.py       ← All 10 chart functions
├── filters.py      ← Data loading & filtering logic
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Running

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the dashboard
```bash
streamlit run app.py
```

Opens at **http://localhost:8501**

---

## 📊 Charts Included (all 10 required)

| # | Chart | Insight |
|---|-------|---------|
| 1 | Pie Chart | Top 8 countries share for selected indicator |
| 2 | Histogram | Value distribution for selected indicator |
| 3 | Line Chart | Trends over time for top countries |
| 4 | Bar Chart | Top 15 countries average value |
| 5 | Scatter Plot | Indicator vs Indicator relationship |
| 6 | Box Plot | Value spread by indicator |
| 7 | Heatmap | Country × Year value intensity |
| 8 | Area Chart | Stacked cumulative trends over time |
| 9 | Count Plot | Record count by indicator |
|10 | Violin Plot | Value density distribution by indicator |

---

## 🎛️ Filters (all linked to charts)

- **Indicator Multi-select** — Choose which WDI indicators to analyze
- **Primary Indicator** — Drives Pie, Line, Bar, Area charts
- **Year Range Slider** — Filter by year (1960–2025)
- **Country Multi-select** — Select specific countries
- **Value Range Slider** — Filter by data value magnitude
- **Text Search** — Search by country or indicator name
- **Reset Button** — Reset all filters to default

---

## 💡 Key Insights

- **GDP (current US$):** USA, China, and Germany dominate global GDP figures consistently.
- **GDP Growth (annual %):** South Asian countries (Pakistan, Bangladesh, India) show volatile but high growth rates across decades.
- **Poverty ($3/day):** Sub-Saharan Africa and South Asia show highest poverty headcount ratios, with gradual improvement post-2000.
- **Education Expenditure:** Developed nations consistently spend more on education as % of GNI.
- **Births with Skilled Staff:** Strong upward trend globally post-1990, reflecting healthcare improvements.

---

## 📚 Data Source

World Bank Group — World Development Indicators (WDI)  
https://databank.worldbank.org/source/world-development-indicators
