"""
Feature engineering module.

Creates derived features: DTR, temporal columns, seasons.
"""

import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def _get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _load_season_map() -> dict:
    """Load season definitions from settings and create month -> season map."""
    root = _get_project_root()
    with open(root / "config" / "settings.json", "r", encoding="utf-8") as f:
        settings = json.load(f)
    season_defs = settings["seasons"]
    month_to_season = {}
    for season_name, months in season_defs.items():
        for m in months:
            month_to_season[m] = season_name
    return month_to_season


def add_dtr(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate Daily Temperature Range (DTR = T2M_MAX - T2M_MIN)."""
    df = df.copy()
    df["DTR"] = df["T2M_MAX"] - df["T2M_MIN"]
    # DTR should be non-negative for valid records
    n_negative = (df["DTR"] < 0).sum()
    if n_negative > 0:
        logger.warning("%d records have negative DTR (T2M_MIN > T2M_MAX)", n_negative)
    return df


def add_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add year, month, month_name, day_of_year columns."""
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%b")
    df["day_of_year"] = df["date"].dt.dayofyear
    return df


def add_season(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add meteorological season column.

    Seasons (IMD-style):
    - Winter: Dec, Jan, Feb
    - Pre-monsoon: Mar, Apr, May
    - Monsoon: Jun, Jul, Aug, Sep
    - Post-monsoon: Oct, Nov

    December is assigned to the winter of the following year for
    seasonal aggregation (e.g., Dec 2010 belongs to Winter 2011).
    """
    df = df.copy()
    month_to_season = _load_season_map()

    df["season"] = df["month"].map(month_to_season)

    # Season year: December belongs to the following year's winter
    df["season_year"] = df["year"]
    df.loc[df["month"] == 12, "season_year"] = df.loc[df["month"] == 12, "year"] + 1

    # Log season assignment
    season_counts = df["season"].value_counts()
    logger.info("Season assignment:\n%s", season_counts.to_string())

    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full feature engineering pipeline.

    Adds: DTR, year, month, month_name, day_of_year, season, season_year.
    """
    logger.info("Feature engineering start: shape=%s", df.shape)

    df = add_dtr(df)
    df = add_temporal_features(df)
    df = add_season(df)

    # Save the engineered daily dataset
    root = _get_project_root()
    processed_dir = root / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    out_path = processed_dir / "temperature_daily.csv"
    df.to_csv(out_path, index=False)
    logger.info("Saved daily dataset: %s (%d records)", out_path, len(df))

    logger.info("Feature engineering complete: shape=%s", df.shape)
    return df
