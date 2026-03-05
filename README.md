# 📈 NSE Market Intelligence Dashboard

> **Risk · Return · Valuation Analysis across Market Cap Categories**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-00CC96?style=flat-square&logo=plotly&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=flat-square&logo=mysql&logoColor=white)
![FY](https://img.shields.io/badge/Data-FY2024--25-FFD700?style=flat-square)

---

## 📋 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Objectives](#2-objectives)
3. [Project Structure](#3-project-structure)
4. [Dataset Description](#4-dataset-description)
5. [Tech Stack](#5-tech-stack)
6. [Installation & Setup](#6-installation--setup)
7. [Dashboard Features](#7-dashboard-features)
8. [SQL Analytics](#8-sql-analytics)
9. [Key Insights](#9-key-insights)
10. [Screenshots](#10-screenshots)
11. [Future Enhancements](#11-future-enhancements)
12. [License](#12-license)

---

## 1. Project Overview

The **NSE Market Intelligence Dashboard** is a comprehensive financial analytics tool built to analyze, visualize, and interpret the performance of major National Stock Exchange (NSE) indices across different market capitalization categories.

Modeled after a professional **trading terminal UI**, the dashboard presents real-time-style analytics using FY2024-25 data, enabling investors, researchers, and finance students to make informed comparisons across **risk**, **return**, and **valuation** dimensions — all from a single interactive interface.

The project spans the complete data lifecycle:

```
Raw Data  →  ETL Pipeline  →  Feature Engineering  →  MySQL Storage  →  Streamlit Dashboard
```

---

## 2. Objectives

- 📊 Analyze multi-period **CAGR performance** (1Y, 3Y, 5Y) across 10 NSE indices
- ⚠️ Quantify and compare **risk levels** using volatility and composite risk scores
- 💰 Evaluate **valuation metrics** including P/E, P/B, and a composite valuation score
- 🎯 Compute **risk-adjusted returns** to identify the most efficient indices
- 🗂️ Provide **sector and market-cap category comparisons** via heatmaps and radar charts
- 🔍 Enable **single-index deep-dive** analysis with universe benchmarking
- 🗄️ Store and query index data using a normalized **MySQL schema**

---

## 3. Project Structure

```
NSE_Index_Analytics/
│
├── data/
│   ├── raw/
│   │   └── nse_index_raw.csv               # Original uncleaned data
│   └── processed/
│       ├── nse_index_clean.csv             # After cleaning & type fixing
│       └── nse_index_final.csv             # After feature engineering
│
├── scripts/
│   ├── 01_data_loading.py                  # Load and inspect raw data
│   ├── 02_data_cleaning.py                 # Standardize columns, handle nulls
│   └── 03_feature_engineering.py          # Derived features & category labels
│
├── sql/
│   └── sqlnse_index_queries.sql            # MySQL schema & analytics queries
│
├── streamlit_dashboard.py                  # Interactive dashboard (main app)
└── README.md                               # Project documentation
```

---

## 4. Dataset Description

The dataset covers **10 major NSE indices** for FY2024-25.

| Column | Type | Description |
|--------|------|-------------|
| `index_name` | String | Full name of the NSE index |
| `market_cap_category` | String | Large / Mid / Small / Micro / Sectoral |
| `cagr_1y` | Float | 1-Year Compound Annual Growth Rate (%) |
| `cagr_3y` | Float | 3-Year Compound Annual Growth Rate (%) |
| `cagr_5y` | Float | 5-Year Compound Annual Growth Rate (%) |
| `volatility` | Float | Annualized volatility as risk proxy (%) |
| `avg_pe` | Float | Average Price-to-Earnings ratio |
| `avg_pb` | Float | Average Price-to-Book ratio |
| `index_level` | Integer | Current index value |
| `risk_level` | String | Low / Medium / High / Very High / Extreme |
| `risk_score` | Integer | Numeric mapping of risk_level (1–5) |
| `return_category` | String | Moderate / High / Very High / Excellent |
| `risk_adjusted_return` | Float | 5Y CAGR ÷ Volatility |
| `valuation_score` | Float | Composite overvaluation score: avg_pe × avg_pb |

### Index Universe

| Index | Segment | Risk Level |
|-------|---------|------------|
| NIFTY 50 | Large Cap | High |
| NIFTY NEXT 50 | Large Cap | High |
| NIFTY MIDCAP 100 | Mid Cap | High |
| NIFTY MIDCAP 150 | Mid Cap | High |
| NIFTY SMALLCAP 100 | Small Cap | Very High |
| NIFTY SMALLCAP 250 | Small Cap | Very High |
| NIFTY MICROCAP 250 | Micro Cap | Extreme |
| NIFTY BANK | Sectoral Large Cap | Medium |
| NIFTY FMCG | Defensive Large Cap | Low |
| NIFTY PHARMA | Large Cap Pharma | Medium |

---

## 5. Tech Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| **Data Processing** | Python 3.10+ / Pandas | ETL pipeline: loading, cleaning, feature engineering |
| **Visualization** | Plotly | Interactive charts, scatter plots, radar, heatmaps |
| **Dashboard UI** | Streamlit | Web-based UI with sidebar filters, tabs, KPI cards |
| **Database** | MySQL 8.0+ | Relational schema with analytics-ready SQL queries |
| **Styling** | Custom CSS | Trading terminal dark theme with Space Mono font |
| **Export** | Pandas CSV | One-click filtered dataset download from sidebar |

---

## 6. Installation & Setup

### Prerequisites

- Python 3.10 or higher
- pip package manager
- MySQL 8.0+ *(optional — for SQL analytics only)*

### Step 1 — Clone the Repository

```bash
git clone https://github.com/yourusername/nse-index-analytics.git
cd nse-index-analytics
```

### Step 2 — Install Dependencies

```bash
pip install streamlit pandas plotly numpy
```

### Step 3 — Run the ETL Pipeline

```bash
python scripts/01_data_loading.py
python scripts/02_data_cleaning.py
python scripts/03_feature_engineering.py
```

### Step 4 — Launch the Dashboard

```bash
streamlit run streamlit_dashboard.py
```

Then open your browser at: **http://localhost:8501**

### Step 5 — MySQL Setup *(Optional)*

```bash
mysql -u root -p < sql/sqlnse_index_queries.sql
```

---

## 7. Dashboard Features

### Navigation Tabs

| Tab | Section | Contents |
|-----|---------|----------|
| 📈 **Returns** | CAGR Analysis | Multi-period grouped bar, ranking bar, momentum scatter, segment heatmap |
| ⚠️ **Risk** | Risk Metrics | Risk distribution donut, volatility bars, risk-return scatter, radar chart |
| 💰 **Valuation** | PE / PB Analysis | Dual-axis P/E+P/B chart, valuation score bars, PE vs PB quadrant, AI insights |
| 🎯 **Efficiency** | Risk-Adj Returns | RAR ranking bar, top-5 indicator tiles, efficiency frontier, return categories |
| 🔍 **Deep Dive** | Single Index | Per-index KPIs, CAGR bars, metric strength, universe comparison, AI analysis |
| 📋 **Data Table** | Full Dataset | Sortable styled table with color-coded risk, summary statistics |

### KPI Metrics (Header Row)

- **Avg 5Y CAGR** — portfolio-wide average with best performer callout
- **Best Risk-Adj Return** — top efficiency ratio with index name
- **Avg P/E Ratio** — universe average with min–max range
- **Indices Tracked** — count of indices in filtered view
- **Best 1Y Return** — highest short-term performer
- **Avg Volatility** — universe average volatility

### Sidebar Controls

- **Market Cap Category** — multi-select filter (Large / Mid / Small / Micro / Sectoral)
- **Risk Level** — multi-select filter (Low → Extreme)
- **CAGR Horizon** — radio selector for 1Y / 3Y / 5Y used in ranking chart
- **Download CSV** — one-click export of the filtered dataset

---

## 8. SQL Analytics

The project includes a complete **MySQL schema** with six pre-written analytics queries:

```sql
-- Database: nse_index_analytics
-- Table: nse_indices (14 columns, 10 rows)
```

| # | Query | Output |
|---|-------|--------|
| Q1 | Top 5 indices by 5Y CAGR | Ranked list of highest-returning indices |
| Q2 | Risk vs Return overview | Volatility and CAGR side-by-side |
| Q3 | Best risk-adjusted returns | Efficiency ranking across all indices |
| Q4 | Overvalued indices by PE×PB score | Valuation risk ranking |
| Q5 | Avg CAGR & volatility by market segment | Grouped aggregation by category |
| Q6 | Low vs Extreme risk comparison | Filtered comparison of risk extremes |

### Sample Query

```sql
-- Best risk-adjusted returns
SELECT index_name, risk_adjusted_return
FROM nse_indices
ORDER BY risk_adjusted_return DESC;

-- Market segment performance
SELECT market_cap_category,
       ROUND(AVG(cagr_5y), 2)     AS avg_5y_return,
       ROUND(AVG(volatility), 2)  AS avg_volatility
FROM nse_indices
GROUP BY market_cap_category;
```

---

## 9. Key Insights

- 🥇 **NIFTY FMCG** delivers the best risk-adjusted return (**1.585**) thanks to low volatility (9.4%) despite a modest 5Y CAGR of 14.9%
- 🚀 **NIFTY MICROCAP 250** offers the highest 5Y CAGR (**23.7%**) but carries the most risk (volatility 27.6%, rated *Extreme*)
- 📉 **NIFTY BANK** has the lowest risk-adjusted return (**0.831**) — investors are not being adequately compensated for its volatility
- 💸 **NIFTY FMCG** has the highest valuation score (**461**) — investors are paying a heavy premium, reflecting defensive sector demand
- ⚖️ **Large Cap indices** (NIFTY 50, NIFTY NEXT 50) offer the best balance of risk and return for conservative investors
- 📊 **Mid Cap indices** outperform Large Caps on raw CAGR with only moderately higher volatility — a compelling risk-return trade-off

---

## 10. Screenshots

The dashboard renders in a **dark trading-terminal theme** with:

- Header with live-data badge and 6 KPI metric cards
- **Returns tab** — grouped CAGR bars, momentum scatter, segment heatmap
- **Risk tab** — donut chart, volatility bars, risk-return scatter, radar chart
- **Valuation tab** — dual-axis P/E + P/B, valuation score bars, quadrant chart
- **Efficiency tab** — RAR ranking bar, top-5 indicator tiles, efficiency frontier
- **Deep Dive tab** — per-index deep analysis with universe benchmarking

> 📸 *Refer to the screenshot provided during project submission for a full preview.*

---

## 11. Future Enhancements

- [ ] Integrate **NSE Live API** for real-time index data feed
- [ ] Add **portfolio simulator** — pick indices, allocate weights, simulate returns
- [ ] Expand to **30+ indices** with 5+ years of monthly historical data
- [ ] Add **Monte Carlo simulation** for forward-looking risk analysis
- [ ] **Deploy** on Streamlit Cloud / Hugging Face Spaces for public access
- [ ] Add **authentication** layer for personalized watchlists
- [ ] Enable **PDF report export** directly from the dashboard

---

## 12. License

This project is built for **educational and portfolio demonstration purposes only**.  
All data is simulated/indicative based on publicly available NSE India market information for FY2024-25.

> ⚠️ **Disclaimer:** This is NOT investment advice. Always consult a SEBI-registered financial advisor before making investment decisions.

---

<div align="center">

**Built with ❤️ by a Financial Analytics Enthusiast**

*NSE Market Intelligence Dashboard · FY2024-25 · Python · Streamlit · Plotly · MySQL*

</div>
