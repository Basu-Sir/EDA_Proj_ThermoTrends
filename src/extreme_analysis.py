"""
Temperature extremes analysis module.

Computes hot-day (T2M_MAX > P90) and warm-night (T2M_MIN > P90) indicators.
"""

import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def _get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _load_settings() -> dict:
    root = _get_project_root()
    with open(root / "config" / "settings.json", "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Threshold calculation
# ---------------------------------------------------------------------------

def compute_monthly_thresholds(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute city-specific monthly percentile thresholds for hot days and warm nights.

    Uses the full study period (2001-2025) as the reference period since a
    conventional 30-year baseline is not available.

    Thresholds are computed per city per calendar month to account for
    seasonal temperature variation.

    Returns DataFrame with columns:
        city, month, hot_day_threshold (T2M_MAX P90), warm_night_threshold (T2M_MIN P90)
    """
    settings = _load_settings()
    hot_pct = settings["extreme_thresholds"]["hot_day_percentile"]
    warm_pct = settings["extreme_thresholds"]["warm_night_percentile"]
    ref_start = settings["extreme_thresholds"]["reference_period"]["start_year"]
    ref_end = settings["extreme_thresholds"]["reference_period"]["end_year"]

    # Filter to reference period
    ref_df = df[(df["year"] >= ref_start) & (df["year"] <= ref_end)]
    logger.info(
        "Computing thresholds from reference period %d-%d (%d records)",
        ref_start, ref_end, len(ref_df),
    )

    rows = []
    for city in sorted(ref_df["city"].unique()):
        city_data = ref_df[ref_df["city"] == city]
        for month in range(1, 13):
            month_data = city_data[city_data["month"] == month]

            tmax_vals = month_data["T2M_MAX"].dropna()
            tmin_vals = month_data["T2M_MIN"].dropna()

            hot_thresh = float(np.percentile(tmax_vals, hot_pct)) if len(tmax_vals) >= 10 else np.nan
            warm_thresh = float(np.percentile(tmin_vals, warm_pct)) if len(tmin_vals) >= 10 else np.nan

            rows.append({
                "city": city,
                "month": month,
                "hot_day_threshold": round(hot_thresh, 2) if np.isfinite(hot_thresh) else np.nan,
                "warm_night_threshold": round(warm_thresh, 2) if np.isfinite(warm_thresh) else np.nan,
                "tmax_count": len(tmax_vals),
                "tmin_count": len(tmin_vals),
                "percentile": hot_pct,
            })

    thresholds_df = pd.DataFrame(rows)

    # Save
    root = _get_project_root()
    out_dir = root / "data" / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    thresholds_df.to_csv(out_dir / "extreme_thresholds.csv", index=False)
    logger.info("Extreme thresholds saved: %d rows", len(thresholds_df))

    return thresholds_df


# ---------------------------------------------------------------------------
# Flag extreme events
# ---------------------------------------------------------------------------

def flag_extreme_events(df: pd.DataFrame, thresholds_df: pd.DataFrame) -> pd.DataFrame:
    """
    Flag hot days and warm nights based on city-month-specific thresholds.

    A hot day: T2M_MAX exceeds the 90th-percentile threshold for that city-month.
    A warm night: T2M_MIN exceeds the 90th-percentile threshold for that city-month.
    """
    df = df.copy()

    # Merge thresholds
    merged = df.merge(
        thresholds_df[["city", "month", "hot_day_threshold", "warm_night_threshold"]],
        on=["city", "month"],
        how="left",
    )

    # Flag events
    merged["is_hot_day"] = merged["T2M_MAX"] > merged["hot_day_threshold"]
    merged["is_warm_night"] = merged["T2M_MIN"] > merged["warm_night_threshold"]

    # Handle NaN thresholds — don't flag
    merged.loc[merged["hot_day_threshold"].isna(), "is_hot_day"] = False
    merged.loc[merged["warm_night_threshold"].isna(), "is_warm_night"] = False

    n_hot = merged["is_hot_day"].sum()
    n_warm = merged["is_warm_night"].sum()
    logger.info("Hot days flagged: %d (%.1f%%)", n_hot, 100 * n_hot / len(merged))
    logger.info("Warm nights flagged: %d (%.1f%%)", n_warm, 100 * n_warm / len(merged))

    return merged


# ---------------------------------------------------------------------------
# Annual extreme frequencies
# ---------------------------------------------------------------------------

def compute_annual_extreme_frequencies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute number and percentage of hot days and warm nights per city per year.
    """
    annual = (
        df.groupby(["city", "year"])
        .agg(
            total_days=("is_hot_day", "count"),
            hot_days=("is_hot_day", "sum"),
            warm_nights=("is_warm_night", "sum"),
        )
        .reset_index()
    )

    annual["hot_day_pct"] = (100 * annual["hot_days"] / annual["total_days"]).round(2)
    annual["warm_night_pct"] = (100 * annual["warm_nights"] / annual["total_days"]).round(2)

    root = _get_project_root()
    out_dir = root / "data" / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    annual.to_csv(out_dir / "extreme_annual_frequencies.csv", index=False)
    logger.info("Annual extreme frequencies saved: %d rows", len(annual))

    return annual


# ---------------------------------------------------------------------------
# Long-term extreme summary per city
# ---------------------------------------------------------------------------

def compute_extreme_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Compute overall extreme event summary per city."""
    summary = (
        df.groupby("city")
        .agg(
            total_days=("is_hot_day", "count"),
            total_hot_days=("is_hot_day", "sum"),
            total_warm_nights=("is_warm_night", "sum"),
        )
        .reset_index()
    )

    summary["hot_day_pct"] = (100 * summary["total_hot_days"] / summary["total_days"]).round(2)
    summary["warm_night_pct"] = (100 * summary["total_warm_nights"] / summary["total_days"]).round(2)

    root = _get_project_root()
    out_dir = root / "data" / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    summary.to_csv(out_dir / "extreme_summary.csv", index=False)
    logger.info("Extreme summary saved: %d rows", len(summary))

    return summary


# ---------------------------------------------------------------------------
# Seasonal distribution of extremes
# ---------------------------------------------------------------------------

def compute_seasonal_extreme_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Count extreme events by city and season."""
    seasonal = (
        df.groupby(["city", "season"])
        .agg(
            total_days=("is_hot_day", "count"),
            hot_days=("is_hot_day", "sum"),
            warm_nights=("is_warm_night", "sum"),
        )
        .reset_index()
    )

    seasonal["hot_day_pct"] = (100 * seasonal["hot_days"] / seasonal["total_days"]).round(2)
    seasonal["warm_night_pct"] = (100 * seasonal["warm_nights"] / seasonal["total_days"]).round(2)

    root = _get_project_root()
    out_dir = root / "data" / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    seasonal.to_csv(out_dir / "extreme_seasonal_distribution.csv", index=False)
    logger.info("Seasonal extreme distribution saved: %d rows", len(seasonal))

    return seasonal


# ---------------------------------------------------------------------------
# Full extreme analysis pipeline
# ---------------------------------------------------------------------------

def analyze_extremes(df: pd.DataFrame) -> dict:
    """
    Run the complete extreme temperature analysis.

    Returns dict with keys: thresholds, flagged_df, annual, summary, seasonal.
    """
    logger.info("=" * 60)
    logger.info("EXTREME TEMPERATURE ANALYSIS START")

    # 1. Compute thresholds
    thresholds = compute_monthly_thresholds(df)

    # 2. Flag events
    flagged = flag_extreme_events(df, thresholds)

    # 3. Annual frequencies
    annual = compute_annual_extreme_frequencies(flagged)

    # 4. Summary
    summary = compute_extreme_summary(flagged)

    # 5. Seasonal distribution
    seasonal = compute_seasonal_extreme_distribution(flagged)

    logger.info("EXTREME TEMPERATURE ANALYSIS COMPLETE")
    logger.info("=" * 60)

    return {
        "thresholds": thresholds,
        "flagged_df": flagged,
        "annual": annual,
        "summary": summary,
        "seasonal": seasonal,
    }
