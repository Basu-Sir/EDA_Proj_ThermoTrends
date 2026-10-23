# ThermoTrends India
### A Comparative Exploratory Data Analysis of Long-Term Temperature Patterns Across Selected Indian Cities (2001–2025)

**Course:** BACSE301 — Exploratory Data Analysis  
**Institution:** Vellore Institute of Technology (VIT), Vellore, Tamil Nadu, India  
**Research Team:** Rishu Kumar, Ananda Basu, Parth Mishra  
**Data Attribution:** NASA POWER (Prediction Of Worldwide Energy Resources) Daily Point Reanalysis  
**Study Span:** 1 January 2001 – 31 December 2025 (25 Years • 109,572 Daily Records)  
**Geographic Coverage:** 12 Indian Cities Spanning 6 Climatological Regimes  

---

## 1. Project Overview & Research Objectives

ThermoTrends India conducts a comparative exploratory data analysis (EDA) of quarter-century daily temperatures across 12 climatically distinct metropolitan centers in India:
1. **Delhi** (Northern Plains — Semi-arid)
2. **Jaipur** (Northwestern — Semi-arid / Subtropical)
3. **Lucknow** (Indo-Gangetic Basin — Humid Subtropical)
4. **Srinagar** (Western Himalayas — Montane Alpine / Humid Continental)
5. **Mumbai** (Konkan Coast — Tropical Wet & Dry)
6. **Ahmedabad** (Western Plains — Hot Semi-arid)
7. **Chennai** (Coromandel Coast — Tropical Wet & Dry)
8. **Bengaluru** (Deccan Plateau — Tropical Savanna)
9. **Hyderabad** (Deccan Plateau — Hot Semi-arid)
10. **Kochi** (Malabar Coast — Tropical Monsoon)
11. **Kolkata** (Lower Gangetic Delta — Tropical Wet & Dry)
12. **Guwahati** (Brahmaputra Valley — Humid Subtropical)

### Core Inquiries:
- **RQ1 (Decadal Trends):** Quantifying rates of change in daily minimum ($T_{\min}$), maximum ($T_{\max}$), and mean ($T_{\text{mean}}$) temperatures.
- **RQ2 (Asymmetric Warming):** Testing whether nocturnal minimums are warming faster than daytime maximums across regions.
- **RQ3 (Climatological Variability):** Characterizing seasonal amplitudes, dispersion, and distributions across peninsular, continental, and Himalayan zones.
- **RQ4 (DTR Contraction):** Determining whether the Diurnal Temperature Range ($\text{DTR} = T_{\max} - T_{\min}$) is expanding or contracting.
- **RQ5 (Percentile Extremes):** Tracking calendar-month 90th percentile ($P_{90}$) exceedance frequencies for hot days and warm nights.
- **RQ6 (Observational Integrity):** Auditing missingness, physical bounds, and documenting the boundaries of gridded reanalysis.

---

## 2. Repository Architecture

```text
thermotrends-india/
├── README.md                      # Complete project documentation & execution guide
├── requirements.txt               # Python package dependencies
├── run_pipeline.py                # Master Python pipeline runner
├── generate_notebook.py           # Automated Jupyter notebook generator
├── config/
│   ├── cities.json                # Geographic coordinates, regions, climate zones
│   └── settings.json              # Study parameters, thresholds, API definitions
├── data/
│   ├── raw/                       # Cached NASA POWER JSONs & temperature_raw_combined.csv
│   └── processed/                 # Clean CSVs, chart_data.json, findings.json
├── notebooks/
│   └── ThermoTrends_EDA.ipynb     # Documented analysis workflow notebook
├── src/
│   ├── __init__.py
│   ├── data_collection.py         # NASA POWER API fetcher with retries & caching
│   ├── preprocessing.py           # Fill value replacement & bounds auditing
│   ├── feature_engineering.py     # DTR calculation & IMD season mapping
│   ├── descriptive_analysis.py    # Summary statistics & annual aggregations
│   ├── trend_analysis.py          # OLS linear regression & Mann-Kendall tests
│   ├── seasonal_analysis.py       # Monthly climatology & seasonal variances
│   ├── extreme_analysis.py        # Calendar-month 90th percentile exceedances
│   ├── visualizations.py          # Matplotlib/Seaborn scientific figures
│   └── reporting.py               # JSON serialization for frontend website
├── frontend/                      # React + TypeScript + Vite + Tailwind CSS site
│   ├── package.json
│   ├── vite.config.ts
│   ├── public/
│   │   └── data/                  # Clean JSON and CSV feeds consumed by frontend
│   └── src/
│       ├── App.tsx                # Main single-page application orchestrator
│       ├── types.ts               # TypeScript data interfaces
│       ├── data.ts                # JSON loaders, formatters, and color tokens
│       ├── index.css              # Warm editorial design system tokens
│       └── components/            # 10 modular React presentation components
├── outputs/
│   ├── figures/                   # 16 high-resolution publication figures (PNG)
│   └── logs/                      # Pipeline execution logs & fetch trace
└── tests/
    ├── test_preprocessing.py      # Unit tests for cleaning and auditing
    ├── test_feature_engineering.py# Unit tests for DTR and leap-year temporal features
    └── test_trend_analysis.py     # Unit tests for OLS slopes and Mann-Kendall
```

---

## 3. Environment Setup & Dependency Installation

### Prerequisites
- Python 3.10+ (Tested on Python 3.11 and 3.13)
- Node.js 18+ and npm 9+ (for the frontend application)

### Python Virtual Environment Setup

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Dependency Versions (Core):
- `pandas >= 2.0.0`
- `numpy >= 1.24.0`
- `scipy >= 1.10.0`
- `statsmodels >= 0.14.0`
- `matplotlib >= 3.7.0`
- `seaborn >= 0.12.0`
- `requests >= 2.31.0`
- `pymannkendall >= 1.4.3`
- `pytest >= 8.0.0`

---

## 4. Running the Data Pipeline & Automated Tests

### 1. Execute the Data Pipeline
To execute the complete end-to-end pipeline (Data Acquisition $\to$ Quality Auditing $\to$ Feature Engineering $\to$ Descriptive Statistics $\to$ Trend Analysis $\to$ Seasonal Analysis $\to$ Extreme Analysis $\to$ Visualizations $\to$ JSON Export):

```bash
python run_pipeline.py
```

*Note on Caching:* Successful API requests are permanently cached in `data/raw/{city}_raw.json`. Re-running `run_pipeline.py` uses the cached raw files and completes in under 30 seconds without generating redundant network calls.

### 2. Run Automated Verification Tests
We maintain 28 unit tests validating DTR computation, leap year handling, duplicate screening, physical bounds, OLS conversion to decadal rates, and Mann-Kendall monotonicity:

```bash
python -m pytest tests/ -v
```
All 28 tests will pass cleanly.

---

## 5. Running the Jupyter Notebook

Open and execute the documented analysis workflow:

```bash
jupyter notebook notebooks/ThermoTrends_EDA.ipynb
```
Or in VS Code / Cursor / Google Colab:
- Open `notebooks/ThermoTrends_EDA.ipynb`
- Select your Python 3 kernel
- Run all cells sequentially

---

## 6. Launching the Research Website (Frontend)

The research presentation website is built with React 19, TypeScript, Vite, Tailwind CSS v4, and Recharts, styled with a warm editorial light theme (`#F7F4EC` ivory and `#EDE6D8` soft beige).

### Install Node Dependencies & Start Dev Server
```bash
cd frontend
npm install
npm run dev
```
Open your browser at `http://127.0.0.1:5173/` (or the URL displayed in the terminal).

### Build for Production Deployment
To generate a compiled, type-checked production bundle:
```bash
cd frontend
npm run build
```
Compiled static assets will be output to `frontend/dist/`.

---

## 7. Key Empirical Findings (Summary)

1. **Persistent Nocturnal Warming (RQ1):** Daily minimum temperatures ($T_{\min}$) warmed at an average rate of **+0.1221 °C/decade** across the 12 cities, with 9 of 12 stations exhibiting positive slopes. Guwahati showed the highest rate (+0.4210 °C/decade).
2. **Universal Warming Asymmetry (RQ2):** In **12 out of 12 cities (100%)**, nighttime minimums warmed faster (or cooled slower) than daytime maximums, creating an average nocturnal warming surplus of **+0.374 °C/decade**.
3. **Subcontinental DTR Contraction (RQ4):** Diurnal Temperature Range ($T_{\max} - T_{\min}$) contracted in **12 out of 12 cities (100%)** at an average rate of **-0.3740 °C/decade**, confirming nationwide diurnal amplitude dampening.
4. **Thermal Extremes (RQ5):** Lucknow recorded the highest frequency of hot days (**36.6 days/year**), while Delhi recorded the highest frequency of warm nights (**36.5 nights/year**) based on calendar-month 90th percentile thresholds.
5. **Observational Completeness (RQ6):** All 109,572 expected daily observations were successfully retrieved with 0 missing dates and 0 duplicate or invalid records.

---

## 8. Scientific Limitations & Boundaries

1. **Gridded Reanalysis Resolution:** NASA POWER operates on a $0.5^\circ \times 0.5^\circ$ grid (~2,500 km²), which naturally averages localized microclimates and attenuates intense asphalt/concrete Urban Heat Island (UHI) peaks found at city centers.
2. **Reanalysis vs. Ground Thermometers:** Data represents satellite-calibrated GEOS numerical weather assimilations rather than direct in-situ mercury thermometers.
3. **Climatological Span:** The 25-year study (2001–2025) provides high-resolution 21st-century temporal fidelity but is shorter than the standard 30-year WMO normal period.
4. **Descriptive Rigor:** This is an exploratory study. In accordance with statistical rigor, we do not assert direct physical causation or construct speculative climate attribution models.

---

## 9. Academic References & Citations

- **Stackhouse, P. W., et al. (2021).** *The NASA POWER Project: Prediction of Worldwide Energy Resources.* NASA Langley Research Center. [https://power.larc.nasa.gov/](https://power.larc.nasa.gov/)
- **IPCC (2021).** *Climate Change 2021: The Physical Science Basis.* Contribution of Working Group I to the Sixth Assessment Report. Cambridge University Press.
- **Karl, T. R., et al. (1993).** *A new perspective on recent global warming: Asymmetric trends of daily maximum and minimum temperature.* Bulletin of the American Meteorological Society, 74(6), 1007–1024.
- **Mann, H. B. (1945).** *Nonparametric tests against trend.* Econometrica, 245–259.
- **Sen, P. K. (1968).** *Estimates of the regression coefficient based on Kendall's tau.* Journal of the American Statistical Association, 63(324), 1379–1389.
- **World Meteorological Organization (2017).** *WMO Guidelines on the Calculation of Climate Normals (WMO-No. 1203).* Geneva.
- **India Meteorological Department (2020).** *Climate of India.* Ministry of Earth Sciences, Pune, India.

---
© 2026 ThermoTrends India • Vellore Institute of Technology (VIT), Vellore.
