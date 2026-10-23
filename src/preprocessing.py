"""
Data preprocessing and quality assessment module.

Validates, cleans, and assesses quality of NASA POWER temperature data.
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
# NASA POWER fill-value handling
# ---------------------------------------------------------------------------
NASA_POWER_FILL_VALUE = -999.0


def replace_fill_values(df: pd.DataFrame) -> pd.DataFrame:
    """Replace NASA POWER fill values (-999) with NaN."""
    temp_cols = ["T2M_MIN", "T2M_MAX", "T2M"]
    df = df.copy()
    for col in temp_cols:
        if col in df.columns:
            mask = df[col] <= NASA_POWER_FILL_VALUE
            n_fill = mask.sum()
            if n_fill > 0:
                logger.info("Replaced %d fill values in %s", n_fill, col)
            df.loc[mask, col] = np.nan
    return df


# ---------------------------------------------------------------------------
# Date validation
# ---------------------------------------------------------------------------

def validate_dates(df: pd.DataFrame) -> dict:
    """Validate date coverage per city against expected range."""
    settings = _load_settings()
    period = settings["study_period"]
    start = pd.Timestamp(period["start_date"])
    end = pd.Timestamp(period["end_date"])
    expected_dates = pd.date_range(start, end, freq="D")
    expected_count = len(expected_dates)

    report = {}
    for city in df["city"].unique():
        city_df = df[df["city"] == city]
        city_dates = pd.to_datetime(city_df["date"]).dt.normalize()

        present = set(city_dates)
        expected = set(expected_dates)
        missing_dates = sorted(expected - present)
        extra_dates = sorted(present - expected)
        duplicates = city_df.duplicated(subset=["date"], keep=False).sum()

        report[city] = {
            "expected_records": expected_count,
            "observed_records": len(city_df),
            "unique_dates": city_dates.nunique(),
            "missing_dates_count": len(missing_dates),
            "missing_dates_sample": [str(d.date()) for d in missing_dates[:10]],
            "extra_dates_count": len(extra_dates),
            "duplicate_date_records": int(duplicates),
            "date_range_start": str(city_dates.min().date()) if len(city_dates) > 0 else None,
            "date_range_end": str(city_dates.max().date()) if len(city_dates) > 0 else None,
        }
        logger.info(
            "%s: %d/%d records, %d missing dates, %d duplicates",
            city, len(city_df), expected_count, len(missing_dates), duplicates,
        )

    return report


# ---------------------------------------------------------------------------
# Data type and value validation
# ---------------------------------------------------------------------------

def check_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure correct data types."""
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    for col in ["T2M_MIN", "T2M_MAX", "T2M"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    return df


def check_inconsistencies(df: pd.DataFrame, tolerance: float = 0.5) -> pd.DataFrame:
    """
    Flag inconsistent records:
    - T2M_MIN > T2M_MAX
    - T2M outside [T2M_MIN - tolerance, T2M_MAX + tolerance]
    - Non-finite values
    - Implausible temperatures (< -50°C or > 60°C)
    """
    df = df.copy()

    # Min > Max
    df["flag_min_gt_max"] = df["T2M_MIN"] > df["T2M_MAX"]

    # Mean outside bounds (with tolerance)
    df["flag_mean_outside"] = (
        (df["T2M"] < (df["T2M_MIN"] - tolerance)) |
        (df["T2M"] > (df["T2M_MAX"] + tolerance))
    )

    # Non-finite values
    df["flag_nonfinite"] = (
        ~np.isfinite(df["T2M_MIN"].fillna(0)) |
        ~np.isfinite(df["T2M_MAX"].fillna(0)) |
        ~np.isfinite(df["T2M"].fillna(0))
    )

    # Implausible temperatures (India: realistic range roughly -20 to 55°C)
    implausible_low = -20.0
    implausible_high = 55.0
    for col in ["T2M_MIN", "T2M_MAX", "T2M"]:
        df[f"flag_implausible_{col}"] = (
            (df[col] < implausible_low) | (df[col] > implausible_high)
        )

    # Combined flag
    flag_cols = [c for c in df.columns if c.startswith("flag_")]
    df["flag_any"] = df[flag_cols].any(axis=1)

    n_flagged = df["flag_any"].sum()
    logger.info("Flagged %d records (%.2f%%) with inconsistencies",
                n_flagged, 100 * n_flagged / len(df) if len(df) > 0 else 0)

    return df


# ---------------------------------------------------------------------------
# Missing-value analysis
# ---------------------------------------------------------------------------

def analyze_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Generate missing-value summary per city and variable."""
    temp_cols = ["T2M_MIN", "T2M_MAX", "T2M"]
    rows = []
    for city in sorted(df["city"].unique()):
        city_df = df[df["city"] == city]
        row = {"city": city, "total_records": len(city_df)}
        for col in temp_cols:
            n_null = city_df[col].isna().sum()
            row[f"{col}_null"] = int(n_null)
            row[f"{col}_null_pct"] = round(100 * n_null / len(city_df), 3) if len(city_df) > 0 else 0
        rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Quality summary
# ---------------------------------------------------------------------------

def generate_quality_summary(df: pd.DataFrame, date_report: dict) -> pd.DataFrame:
    """Combine date validation, missing values, and inconsistency checks into a summary."""
    temp_cols = ["T2M_MIN", "T2M_MAX", "T2M"]
    rows = []

    for city in sorted(df["city"].unique()):
        city_df = df[df["city"] == city]
        dr = date_report.get(city, {})

        row = {
            "city": city,
            "expected_records": dr.get("expected_records", 0),
            "observed_records": dr.get("observed_records", len(city_df)),
            "unique_dates": dr.get("unique_dates", 0),
            "missing_dates": dr.get("missing_dates_count", 0),
            "duplicate_records": dr.get("duplicate_date_records", 0),
        }

        for col in temp_cols:
            row[f"{col}_nulls"] = int(city_df[col].isna().sum())

        if "flag_min_gt_max" in city_df.columns:
            row["min_gt_max"] = int(city_df["flag_min_gt_max"].sum())
        if "flag_mean_outside" in city_df.columns:
            row["mean_outside_bounds"] = int(city_df["flag_mean_outside"].sum())
        if "flag_any" in city_df.columns:
            row["total_flagged"] = int(city_df["flag_any"].sum())
            row["flagged_excluded"] = 0  # Not excluding — flagging only

        rows.append(row)

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Remove duplicates
# ---------------------------------------------------------------------------

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate city-date records, keeping the first occurrence."""
    before = len(df)
    df = df.drop_duplicates(subset=["city", "date"], keep="first").reset_index(drop=True)
    after = len(df)
    if before != after:
        logger.info("Removed %d duplicate records", before - after)
    return df


# ---------------------------------------------------------------------------
# Main preprocessing pipeline
# ---------------------------------------------------------------------------

def preprocess(df: pd.DataFrame) -> tuple:
    """
    Full preprocessing pipeline.

    Returns
    -------
    tuple of (cleaned_df, quality_summary_df)
    """
    logger.info("=" * 60)
    logger.info("PREPROCESSING PIPELINE START")
    logger.info("Input shape: %s", df.shape)

    # 1. Data types
    df = check_data_types(df)

    # 2. Replace fill values
    df = replace_fill_values(df)

    # 3. Validate dates
    date_report = validate_dates(df)

    # 4. Remove duplicates
    df = remove_duplicates(df)

    # 5. Missing value analysis (before cleaning)
    missing_before = analyze_missing(df)
    logger.info("Missing values before cleaning:\n%s", missing_before.to_string())

    # 6. Flag inconsistencies (do NOT remove — just flag)
    df = check_inconsistencies(df)

    # 7. Quality summary
    quality_summary = generate_quality_summary(df, date_report)

    # 8. Save outputs
    root = _get_project_root()
    processed_dir = root / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    quality_summary.to_csv(processed_dir / "data_quality_summary.csv", index=False)
    missing_before.to_csv(processed_dir / "missing_values_summary.csv", index=False)

    logger.info("Output shape: %s", df.shape)
    logger.info("PREPROCESSING PIPELINE COMPLETE")
    logger.info("=" * 60)

    return df, quality_summary
