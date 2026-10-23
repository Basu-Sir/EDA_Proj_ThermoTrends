"""
Descriptive statistical analysis module.

Computes summary statistics for each city and temperature variable.
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as scipy_stats

logger = logging.getLogger(__name__)


def _get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def compute_city_statistics(df: pd.DataFrame, save: bool = True) -> pd.DataFrame:
    """
    Compute descriptive statistics per city and variable.

    For each city and each variable (T2M_MIN, T2M_MAX, T2M, DTR):
    - Valid count, mean, median, std, min, max, range
    - Q1, Q3, IQR, skewness, missing %
    """
    variables = ["T2M_MIN", "T2M_MAX", "T2M", "DTR"]
    rows = []

    for city in sorted(df["city"].unique()):
        city_df = df[df["city"] == city]
        for var in variables:
            if var not in city_df.columns:
                continue
            series = city_df[var].dropna()
            total = len(city_df)
            valid = len(series)
            missing = total - valid
            missing_pct = round(100 * missing / total, 3) if total > 0 else 0

            if valid > 0:
                q1 = float(series.quantile(0.25))
                q3 = float(series.quantile(0.75))
                row = {
                    "city": city,
                    "variable": var,
                    "valid_count": valid,
                    "missing_count": missing,
                    "missing_pct": missing_pct,
                    "mean": round(float(series.mean()), 2),
                    "median": round(float(series.median()), 2),
                    "std": round(float(series.std()), 2),
                    "min": round(float(series.min()), 2),
                    "max": round(float(series.max()), 2),
                    "range": round(float(series.max() - series.min()), 2),
                    "q1": round(q1, 2),
                    "q3": round(q3, 2),
                    "iqr": round(q3 - q1, 2),
                    "skewness": round(float(scipy_stats.skew(series, nan_policy="omit")), 3),
                }
            else:
                row = {
                    "city": city,
                    "variable": var,
                    "valid_count": 0,
                    "missing_count": missing,
                    "missing_pct": missing_pct,
                    "mean": np.nan, "median": np.nan, "std": np.nan,
                    "min": np.nan, "max": np.nan, "range": np.nan,
                    "q1": np.nan, "q3": np.nan, "iqr": np.nan,
                    "skewness": np.nan,
                }
            rows.append(row)

    result = pd.DataFrame(rows)

    # Save
    if save:
        root = _get_project_root()
        out_dir = root / "data" / "processed"
        out_dir.mkdir(parents=True, exist_ok=True)
        result.to_csv(out_dir / "city_statistics.csv", index=False)
        logger.info("City statistics saved: %d rows", len(result))

    return result


def compute_annual_averages(df: pd.DataFrame, save: bool = True) -> pd.DataFrame:
    """Compute annual mean of T2M_MIN, T2M_MAX, T2M, DTR per city."""
    variables = ["T2M_MIN", "T2M_MAX", "T2M", "DTR"]
    agg_dict = {var: "mean" for var in variables if var in df.columns}
    agg_dict["date"] = "count"  # valid day count

    annual = (
        df.groupby(["city", "year"])
        .agg(agg_dict)
        .rename(columns={"date": "valid_days"})
        .reset_index()
    )

    # Round temperature values
    for var in variables:
        if var in annual.columns:
            annual[var] = annual[var].round(3)

    # Save
    if save:
        root = _get_project_root()
        out_dir = root / "data" / "processed"
        out_dir.mkdir(parents=True, exist_ok=True)
        annual.to_csv(out_dir / "temperature_annual.csv", index=False)
        logger.info("Annual averages saved: %d rows", len(annual))

    return annual


def compute_monthly_averages(df: pd.DataFrame, save: bool = True) -> pd.DataFrame:
    """Compute monthly mean of temperature variables per city."""
    variables = ["T2M_MIN", "T2M_MAX", "T2M", "DTR"]
    agg_dict = {var: "mean" for var in variables if var in df.columns}
    agg_dict["date"] = "count"

    monthly = (
        df.groupby(["city", "year", "month", "month_name"])
        .agg(agg_dict)
        .rename(columns={"date": "valid_days"})
        .reset_index()
    )

    for var in variables:
        if var in monthly.columns:
            monthly[var] = monthly[var].round(3)

    if save:
        root = _get_project_root()
        out_dir = root / "data" / "processed"
        out_dir.mkdir(parents=True, exist_ok=True)
        monthly.to_csv(out_dir / "temperature_monthly.csv", index=False)
        logger.info("Monthly averages saved: %d rows", len(monthly))

    return monthly


def compute_seasonal_averages(df: pd.DataFrame, save: bool = True) -> pd.DataFrame:
    """Compute seasonal mean of temperature variables per city."""
    variables = ["T2M_MIN", "T2M_MAX", "T2M", "DTR"]
    agg_dict = {var: "mean" for var in variables if var in df.columns}
    agg_dict["date"] = "count"

    seasonal = (
        df.groupby(["city", "season_year", "season"])
        .agg(agg_dict)
        .rename(columns={"date": "valid_days"})
        .reset_index()
        .rename(columns={"season_year": "year"})
    )

    for var in variables:
        if var in seasonal.columns:
            seasonal[var] = seasonal[var].round(3)

    if save:
        root = _get_project_root()
        out_dir = root / "data" / "processed"
        out_dir.mkdir(parents=True, exist_ok=True)
        seasonal.to_csv(out_dir / "temperature_seasonal.csv", index=False)
        logger.info("Seasonal averages saved: %d rows", len(seasonal))

    return seasonal
