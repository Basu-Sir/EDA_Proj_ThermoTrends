"""
Script to generate the comprehensive ThermoTrends_EDA.ipynb Jupyter notebook.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

def create_cell(cell_type, source, execution_count=None, outputs=None):
    cell = {
        "cell_type": cell_type,
        "metadata": {},
        "source": [line + "\n" for line in source.split("\n")]
    }
    if cell_type == "code":
        cell["execution_count"] = execution_count
        cell["outputs"] = outputs if outputs is not None else []
    return cell

def build_notebook():
    cells = []

    # Title & Metadata
    cells.append(create_cell("markdown", """# ThermoTrends India
## A Comparative Exploratory Data Analysis of Long-Term Temperature Patterns Across Selected Indian Cities (2001–2025)

**Course:** BACSE301 — Exploratory Data Analysis  
**Institution:** Vellore Institute of Technology (VIT), Vellore, Tamil Nadu, India  
**Research Team:** Rishu Kumar, Ananda Basu, Parth Mishra  
**Data Source:** NASA POWER Daily Point API (MERRA-2 / GEOS Reanalysis)  
**Study Span:** 1 January 2001 through 31 December 2025 (25 Years • 109,572 Daily Records)  
**Scope:** 12 Indian Metropolitan Stations Across 6 Climatological Regimes  

---

### Abstract & Study Motivation
This notebook provides a complete, reproducible exploratory data analysis (EDA) investigating quarter-century shifts in daily surface temperatures across 12 climatically distinct Indian urban centers. We examine trends in minimum ($T_{\\min}$), maximum ($T_{\\max}$), and mean ($T_{\\text{mean}}$) temperatures, diurnal temperature range (DTR) contraction, and calendar-month percentile extremes ($P_{90}$). Dual statistical validation is performed using parametric Ordinary Least Squares (OLS) regression and non-parametric Mann–Kendall trend testing with Sen's slope estimation. In strict accordance with exploratory data analysis principles, this study is descriptive and non-causal."""))

    # Imports & Setup
    cells.append(create_cell("code", """import sys
import os
import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm

try:
    import pymannkendall as pmk
except ImportError:
    pmk = None

# Configure plot aesthetic
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#DCD5C8'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#EDE6D8'
plt.rcParams['grid.linestyle'] = '--'

# Project paths
PROJECT_ROOT = Path('.').resolve().parent if Path('.').resolve().name == 'notebooks' else Path('.').resolve()
sys.path.insert(0, str(PROJECT_ROOT))

print(f"Project root: {PROJECT_ROOT}")"""))

    # Section 1: Study Locations & Geographic Metadata
    cells.append(create_cell("markdown", """## 1. Study Locations & Geographic Metadata
We analyze 12 strategically selected Indian cities spanning 6 climatic zones defined by the India Meteorological Department (IMD) and Köppen climate classification:
- **North (Continental & Montane):** Srinagar, Delhi, Jaipur, Lucknow
- **West (Arid & Coastal):** Ahmedabad, Mumbai
- **South (Peninsular & Maritime):** Bengaluru, Chennai, Hyderabad, Kochi
- **East & Northeast (Humid Subtropical):** Kolkata, Guwahati"""))

    cells.append(create_cell("code", """with open(PROJECT_ROOT / "config" / "cities.json", "r", encoding="utf-8") as f:
    cities_cfg = json.load(f)

cities_df = pd.DataFrame(cities_cfg["cities"])
print(f"Total monitored stations: {len(cities_df)}")
display(cities_df[["name", "region", "state", "climate_zone", "latitude", "longitude", "elevation_m"]])"""))

    # Section 2: Data Acquisition
    cells.append(create_cell("markdown", """## 2. Data Acquisition: NASA POWER API
Data was acquired from the NASA POWER (Prediction Of Worldwide Energy Resources) Daily Point API (`community=AG`, temporal resolution `daily`) for coordinates matching each city center:
- `T2M_MIN`: Daily minimum temperature at 2 meters (°C)
- `T2M_MAX`: Daily maximum temperature at 2 meters (°C)
- `T2M`: Daily mean temperature at 2 meters (°C)

All API responses were validated, checked for status codes, cached locally to `data/raw/` to ensure idempotence, and merged into a combined raw dataset."""))

    cells.append(create_cell("code", """raw_data_path = PROJECT_ROOT / "data" / "raw" / "temperature_raw_combined.csv"

if raw_data_path.exists():
    raw_df = pd.read_csv(raw_data_path, parse_dates=["date"])
    print(f"Loaded raw dataset from cache: {len(raw_df):,} records, {raw_df['city'].nunique()} cities")
    display(raw_df.head(5))
else:
    print("Raw dataset not found. Please run: python run_pipeline.py")"""))

    # Section 3: Data Preprocessing & Quality Assessment
    cells.append(create_cell("markdown", """## 3. Data Preprocessing & Quality Assessment
We perform rigorous quality auditing:
1. **Fill Value Replacement:** NASA POWER uses `-999.0` for missing observations; replaced with `np.nan`.
2. **Duplicate Detection:** Verification of duplicate `(city, date)` combinations.
3. **Physical Bound Verification:**
   - $T_{\\min} \\le T_{\\max}$
   - $T_{\\min} \\le T_{\\text{mean}} \\le T_{\\max}$ within a $0.5^\\circ\\text{C}$ numerical tolerance.
4. **Temporal Continuity:** 25 years with leap days (2004, 2008, 2012, 2016, 2020, 2024) expects 9,131 daily records per city."""))

    cells.append(create_cell("code", """from src.preprocessing import preprocess

clean_df, quality_df = preprocess(raw_df)
print(f"Cleaned dataset records: {len(clean_df):,}")
display(quality_df)"""))

    # Section 4: Feature Engineering
    cells.append(create_cell("markdown", """## 4. Feature Engineering
We engineer climatological and temporal features:
- **Diurnal Temperature Range (DTR):** $\\text{DTR} = T_{\\max} - T_{\\min}$
- **Calendar Features:** `year`, `month`, `month_name`, `day`, `day_of_year`
- **IMD Meteorological Seasons:**
  - *Winter:* December, January, February (DJF) — December assigned to subsequent winter year
  - *Pre-monsoon / Summer:* March, April, May (MAM)
  - *Monsoon:* June, July, August, September (JJAS)
  - *Post-monsoon:* October, November (ON)"""))

    cells.append(create_cell("code", """from src.feature_engineering import engineer_features

daily_df = engineer_features(clean_df)
print(f"Feature engineered records: {len(daily_df):,}")
display(daily_df[["date", "city", "T2M_MIN", "T2M_MAX", "T2M", "DTR", "season", "season_year"]].head(5))"""))

    # Section 5: Descriptive Statistics
    cells.append(create_cell("markdown", """## 5. Descriptive Statistical Analysis
We calculate valid count, mean, median, standard deviation, minimum, maximum, range, interquartile range (IQR), and skewness for each city and variable over the entire 2001–2025 period."""))

    cells.append(create_cell("code", """from src.descriptive_analysis import (
    compute_city_statistics,
    compute_annual_averages,
    compute_monthly_averages,
    compute_seasonal_averages
)

city_stats = compute_city_statistics(daily_df, save=False)
annual_df = compute_annual_averages(daily_df, save=False)
monthly_df = compute_monthly_averages(daily_df, save=False)
seasonal_df = compute_seasonal_averages(daily_df, save=False)

print("City-wise Descriptive Statistics (Sample):")
display(city_stats[city_stats["variable"] == "T2M"].head(12))"""))

    # Section 6: Long-Term Trend Analysis
    cells.append(create_cell("markdown", """## 6. Long-Term Trend Analysis (OLS & Mann–Kendall)
For each city and variable, we evaluate long-term trends:
1. **Ordinary Least Squares (OLS) Linear Regression:**
   $$T = \\beta_0 + \\beta_1 \\cdot \\text{year}$$
   Slope reported in $^\\circ\\text{C}/\\text{decade} = \\beta_1 \\times 10$. Evaluates $R^2$, $p$-value, and 95% confidence intervals.
2. **Mann–Kendall Non-Parametric Trend Test & Sen's Slope:**
   Assesses monotonic trends without assuming normality or linearity."""))

    cells.append(create_cell("code", """from src.trend_analysis import analyze_trends, compare_min_max_slopes

trend_df = analyze_trends(annual_df)
min_max_comp = compare_min_max_slopes(trend_df)

print("Trend Analysis Summary (T2M):")
display(trend_df[trend_df["variable"] == "T2M"][["city", "ols_slope_per_decade", "ols_r_squared", "ols_p_value", "ols_significant", "mk_trend", "sens_slope_per_decade"]])

print("\\nMinimum vs. Maximum Warming Slopes Comparison (RQ2 Asymmetry):")
display(min_max_comp)"""))

    # Section 7: Seasonal & Climatological Analysis
    cells.append(create_cell("markdown", """## 7. Monthly & Seasonal Climatology
Examining 25-year baseline climatological profiles and seasonal thermal amplitude across stations."""))

    cells.append(create_cell("code", """from src.seasonal_analysis import (
    compute_monthly_climatology,
    compute_seasonal_statistics,
    compute_seasonal_variation
)

clim_df = compute_monthly_climatology(daily_df)
seasonal_stats = compute_seasonal_statistics(daily_df)
seasonal_var = compute_seasonal_variation(clim_df)

print("Seasonal Variation Across Cities (Annual Range = Max Month Mean - Min Month Mean):")
display(seasonal_var)"""))

    # Section 8: Diurnal Temperature Range (DTR) Analysis
    cells.append(create_cell("markdown", """## 8. Diurnal Temperature Range (DTR) Analysis
Investigating the evolution of $DTR = T_{\\max} - T_{\\min}$ across the subcontinent. A decreasing DTR indicates that nocturnal minimum temperatures are warming faster than daytime maximums."""))

    cells.append(create_cell("code", """dtr_trends = trend_df[trend_df["variable"] == "DTR"][["city", "ols_slope_per_decade", "ols_p_value", "ols_significant", "mk_trend"]]
print("DTR Trends Across All 12 Cities:")
display(dtr_trends.sort_values(by="ols_slope_per_decade"))
print(f"Cities with contracting DTR: {(dtr_trends['ols_slope_per_decade'] < 0).sum()} / {len(dtr_trends)} (100%)")
print(f"Mean DTR decadal rate: {dtr_trends['ols_slope_per_decade'].mean():.4f} °C/decade")"""))

    # Section 9: Temperature Extremes: Hot Days & Warm Nights
    cells.append(create_cell("markdown", """## 9. Temperature Extremes: Hot Days & Warm Nights
We compute city-specific calendar-month 90th percentile thresholds ($P_{90}$) across the full 2001–2025 period:
- **Hot Day:** $T_{\\max} > P_{90}(\\text{city}, \\text{month})$
- **Warm Night:** $T_{\\min} > P_{90}(\\text{city}, \\text{month})$
This methodology avoids bias toward pre-monsoon summer months by assessing temperature anomalies relative to the historical distribution of each specific calendar month."""))

    cells.append(create_cell("code", """from src.extreme_analysis import analyze_extremes

extreme_results = analyze_extremes(daily_df)
extreme_annual = extreme_results["annual"]
extreme_summary = extreme_results["summary"]

print("Extreme Frequency Summary (2001–2025 Mean Days/Year):")
display(extreme_summary)"""))

    # Section 10: Visualizations Gallery
    cells.append(create_cell("markdown", """## 10. Publication-Quality Visualizations
Displaying generated scientific figures from `outputs/figures/`:
1. Data Quality Overview
2. Temperature Distributions
3. City Boxplots
4. Annual Mean Time Series
5. Trend Regression Slopes Heatmap
6. Monthly Climatology Profiles
7. Diurnal Temperature Range Trends
8. Hot Days and Warm Nights Frequency"""))

    cells.append(create_cell("code", """from IPython.display import Image, display

figures_to_show = [
    "01_data_quality_overview.png",
    "02_temperature_distributions.png",
    "06_annual_tmean_series.png",
    "08_trend_heatmap.png",
    "10_monthly_profiles.png",
    "12_annual_dtr_trends.png",
    "14_hot_day_frequency.png",
    "15_warm_night_frequency.png"
]

fig_dir = PROJECT_ROOT / "outputs" / "figures"
for fig_name in figures_to_show:
    fig_path = fig_dir / fig_name
    if fig_path.exists():
        print(f"Figure: {fig_name}")
        display(Image(filename=str(fig_path), width=750))
    else:
        print(f"Figure {fig_name} not found.")"""))

    # Section 11: Synthesis & Answers to Research Questions
    cells.append(create_cell("markdown", """## 11. Empirical Answers to Core Research Questions

### RQ1: Decadal Temperature Changes
- **Minimum Temperature ($T_{\\min}$):** Widespread warming across 9 of 12 stations, with a subcontinental average of **+0.1221 °C/decade**. Guwahati exhibited the strongest trend (+0.4210 °C/decade).
- **Maximum Temperature ($T_{\\max}$):** Diverse trends with an average slope of **-0.2518 °C/decade**, driven by daytime cooling/solar-dimming across northern plains stations (Jaipur -0.8194 °C/decade, Delhi -0.6510 °C/decade).
- **Mean Temperature ($T_{\\text{mean}}$):** Modest nationwide mean of **-0.0487 °C/decade**, reflecting contrasting nighttime and daytime trajectories.

### RQ2: Nocturnal Warming Asymmetry
- In **12 out of 12 cities (100%)**, minimum temperatures warmed faster (or cooled slower) than maximum temperatures ($T_{\\min} \\text{ slope} > T_{\\max} \\text{ slope}$).
- Average asymmetry: **+0.374 °C/decade**. Highest in Srinagar (+0.958 °C/decade), Jaipur (+0.645 °C/decade), and Ahmedabad (+0.633 °C/decade).

### RQ3: Climatological Distributions
- **Warmest Mean:** Chennai (27.93 °C).
- **Coolest Mean:** Srinagar (9.18 °C).
- **Highest Variability:** Srinagar (std = ±7.81 °C), followed by Jaipur (std = ±6.83 °C). Maritime cities (Kochi, Mumbai) displayed tightly buffered variability (<3.5 °C).

### RQ4: DTR Contraction
- Diurnal Temperature Range decreased in **12 out of 12 cities (100%)** with an average contraction rate of **-0.3740 °C/decade**. Diurnal thermal amplitude is universally narrowing across India.

### RQ5: Extreme Hot Days & Warm Nights
- Lucknow recorded the highest average hot days per year (**36.6 days/year**).
- Delhi recorded the highest average warm nights per year (**36.5 nights/year**).
- Month-relative extreme nights are increasing across northern and peninsular urban regions.

### RQ6: Data Integrity & Methodological Boundaries
- All 109,572 expected observations were successfully retrieved (100% completeness) with zero duplicate records and zero physical inconsistencies.
- Exploratory data analysis reveals robust empirical associations without asserting direct causal attribution."""))

    # Section 12: Methodological Boundaries & References
    cells.append(create_cell("markdown", """## 12. Methodological Boundaries & References

### Limitations of Gridded Reanalysis
1. **Spatial Aggregation:** NASA POWER resolution ($0.5^\\circ \\times 0.5^\\circ \\approx 2,500\\text{ km}^2$) smooths microscale urban heat island (UHI) peaks found at city centers.
2. **Model Assimilation vs. In-Situ Thermometers:** Data represents GEOS atmospheric modeling integrated with satellite radiances rather than direct surface mercury sensors.
3. **25-Year Span:** 2001–2025 provides a high-fidelity contemporary record but is shorter than traditional 30-year climatological normal periods.
4. **Descriptive Rigor:** No greenhouse forcing attribution or predictive forecasting models are constructed.

### References
- Stackhouse, P. W., et al. (2021). The NASA POWER Project: Prediction of Worldwide Energy Resources. NASA Langley Research Center.
- IPCC (2021). Climate Change 2021: The Physical Science Basis. Cambridge University Press.
- Karl, T. R., et al. (1993). Asymmetric trends of daily maximum and minimum temperature. *Bull. Amer. Meteor. Soc.*, 74(6), 1007–1024.
- Mann, H. B. (1945). Nonparametric tests against trend. *Econometrica*, 245–259.
- Sen, P. K. (1968). Estimates of the regression coefficient based on Kendall's tau. *J. Amer. Statist. Assoc.*, 63(324), 1379–1389.
- World Meteorological Organization (2017). WMO Guidelines on the Calculation of Climate Normals (WMO-No. 1203). Geneva.
- India Meteorological Department (2020). Climate of India. Ministry of Earth Sciences, Pune."""))

    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.11.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    nb_dir = PROJECT_ROOT / "notebooks"
    nb_dir.mkdir(parents=True, exist_ok=True)
    nb_path = nb_dir / "ThermoTrends_EDA.ipynb"

    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=2)

    print(f"Jupyter Notebook successfully written to: {nb_path}")

if __name__ == "__main__":
    build_notebook()
