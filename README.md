# Funnel Analysis — Olist Marketing Pipeline

End-to-end marketing funnel analysis project built with Python and Power BI.
Analyzes 7,999 leads from the Olist dataset to identify conversion drop-offs,
channel performance gaps, and actionable growth recommendations.

---

## Project Structure
```
FUTURE_DS_03/
├── data/
│   ├── raw/                         # Original dataset (not tracked by Git)
│   └── processed/                   # Cleaned CSVs exported for Power BI
│
├── notebooks/
│   └── 01_data_exploration.ipynb    # Exploratory data analysis
│
├── src/
│   ├── load_clean.py                # Load and clean raw data
│   ├── funnel_metrics.py            # Calculate CVR at each funnel stage
│   ├── channel_analysis.py          # Channel performance and quality scores
│   └── export_for_powerbi.py        # Run full pipeline and export all CSVs
│
├── powerbi/
│   └── funnel_analysis.pbix         # Power BI dashboard (4 pages)
│
├── reports/
│   └── summary.md                   # Key findings and recommendations
│
├── requirements.txt                 # Python dependencies
├── template.py                      # Project scaffolding script
└── README.md                        # This file
```

---

## Dataset

**Source**: Olist Marketing Funnel Dataset
**Link**: https://www.kaggle.com/datasets/olistbr/marketing-funnel-olist

Two CSV files:
- `olist_marketing_qualified_leads_dataset.csv` — 8,000 leads
- `olist_closed_deals_dataset.csv` — 842 closed deals

Download and place both files in `data/raw/` before running the pipeline.

---

## Quickstart

**1. Clone the repo**
```bash
git clone https://github.com/bennedictbett/FUTURE_DS_03
cd FUTURE_DS_03
```

**2. Create and activate virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add the dataset**
```
Download from Kaggle and place both CSVs in:
data/raw/
```

**5. Run the full pipeline**
```bash
python src/export_for_powerbi.py
```

This generates 10 clean CSV files in `data/processed/`.

**6. Open Power BI**
```
Open powerbi/funnel_analysis.pbix
→ Refresh data
→ Point to data/processed/ folder
```

---

## Pipeline Overview
```
Raw Data (Kaggle)
      ↓
load_clean.py          → removes nulls, fixes dates, adds features
      ↓
funnel_metrics.py      → calculates CVR, drop-off, monthly trends
      ↓
channel_analysis.py    → channel quality scores, days to close
      ↓
export_for_powerbi.py  → runs all scripts, exports 10 CSVs
      ↓
Power BI Dashboard     → 4-page interactive report
```

---

## Dashboard Pages

| Page | Description |
|------|-------------|
| Funnel Overview | KPI cards, funnel chart, monthly CVR trend |
| Channel Performance | Lead volume, CVR by channel, quality ranking |
| Monthly Trends | Month-by-month CVR and lead volume breakdown |
| Sales Cycle | Days to close by channel, win/loss summary |

---

## Key Findings

- **10.51% overall CVR** — 841 of 7,999 leads converted
- **89.49% drop-off** — 7,158 leads never converted
- **Jan 2018 inflection** — CVR jumped from 5.5% to 13.32% in one month
- **UTM tracking gap** — 1,159 leads untracked, converting at 16.65%
- **Email underperforming** — 493 leads, only 3.04% CVR
- **Organic search** is the highest quality tracked channel (11.76% CVR)
- **Median close time** is 14 days — mean of 48.5 days is skewed by outliers

---

## Recommendations

1. Fix UTM tracking — best channel is currently invisible
2. Audit email strategy — 3.04% CVR is critically low
3. Scale organic and paid search — proven high CVR channels
4. Optimize social targeting — high volume, low quality
5. Investigate Jan 2018 inflection — replicate what worked
6. Monitor May 2018 CVR drop — prevent further decline

Full recommendations in `reports/summary.md`

---

## Requirements
```
pandas
numpy
openpyxl
matplotlib
seaborn
jupyter
pyyaml
```

---

## Tools Used

| Tool | Purpose |
|------|---------|
| Python (VS Code) | Data cleaning and analysis |
| pandas | Data manipulation |
| Jupyter Notebook | Exploratory analysis |
| Power BI Desktop | Interactive dashboard |
| GitHub | Version control |

---

## Author

Built as part of a data analytics portfolio project.
Dataset credit: Olist — Brazilian E-Commerce (Kaggle)