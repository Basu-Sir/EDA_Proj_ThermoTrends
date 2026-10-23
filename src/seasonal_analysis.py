"""
Seasonal analysis module.

Analyses monthly and seasonal temperature behaviour across cities.
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def _get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Long-term monthly climatology
# ---------------------------------------------------------------------------

def compute_monthly_climatology(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute long-term average temperature for each calendar month and city.

    Returns DataFrame with city, month, month_name, and mean/std of each variable.
    """
    variables = ["T2M_MIN", "T2M_MAX", "T2M", "DTR"]
    agg_dict = {}
    for var in variables:
        if var in df.columns:
            agg_dict[var] = ["mean", "std", "count"]

    clim = (
        df.groupby(["city", "month", "month_name"])
        .agg(agg_dict)
    )
    # Flatten multi-level columns
    clim.columns = ["_".join(col).strip() for col in clim.columns.values]
    clim = clim.reset_index()

    # Round
    for col in clim.columns:
        if clim[col].dtype in [np.float64, np.float32]:
            clim[col] = clim[col].round(3)

    root = _get_project_root()
    out_dir = root / "data" / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    clim.to_csv(out_dir / "monthly_climatology.csv", index=False)
    logger.info("Monthly climatology saved: %d rows", len(clim))

    return clim


# ---------------------------------------------------------------------------
# Seasonal statistics
# ---------------------------------------------------------------------------

def compute_seasonal_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Compute seasonal means and standard deviations per city."""
    variables = ["T2M_MIN", "T2M_MAX", "T2M", "DTR"]
    agg_dict = {}
    for var in variables:
        if var in df.columns:
            agg_dict[var] = ["mean", "std", "count"]

    seasonal = (
        df.groupby(["city", "season"])
        .agg(agg_dict)
    )
    seasonal.columns = ["_".join(col).strip() for col in seasonal.columns.values]
    seasonal = seasonal.reset_index()

    for col in seasonal.columns:
        if seasonal[col].dtype in [np.float64, np.float32]:
            seasonal[col] = seasonal[col].round(3)

    root = _get_project_root()
    out_dir = root / "data" / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    seasonal.to_csv(out_dir / "seasonal_statistics.csv", index=False)
    logger.info("Seasonal statistics saved: %d rows", len(seasonal))

    return seasonal


# ---------------------------------------------------------------------------
# Seasonal variation metric
# ---------------------------------------------------------------------------

def compute_seasonal_variation(monthly_clim: pd.DataFrame) -> pd.DataFrame:
    """
    Compute seasonal variation per city.

    Metric: difference between highest and lowest long-term monthly mean T2M.
    """
    if "T2M_mean" not in monthly_clim.columns:
        logger.warning("T2M_mean not found in monthly climatology.")
        return pd.DataFrame()

    variation = (
        monthly_clim.groupby("city")["T2M_mean"]
        .agg(["max", "min"])
        .reset_index()
    )
    variation["seasonal_range"] = (variation["max"] - variation["min"]).round(2)
    variation = variation.rename(columns={"max": "warmest_month_mean", "min": "coolest_month_mean"})
    variation = variation.sort_values("seasonal_range", ascending=False).reset_index(drop=True)

    root = _get_project_root()
    out_dir = root / "data" / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    variation.to_csv(out_dir / "seasonal_variation.csv", index=False)
    logger.info("Seasonal variation saved: %d rows", len(variation))

    return variation


# ---------------------------------------------------------------------------
# Month × Year heatmap data
# ---------------------------------------------------------------------------

def compute_month_year_heatmap_data(df: pd.DataFrame, variable: str = "T2M") -> dict:
    """
    Create month-by-year pivot tables per city for heatmap visualization.

    Returns dict of {city: DataFrame with months as rows, years as columns}.
    """
    result = {}
    for city in sorted(df["city"].unique()):
        city_df = df[df["city"] == city]
        if variable not in city_df.columns:
            continue
        pivot = city_df.pivot_table(
            values=variable,
            index="month",
            columns="year",
            aggfunc="mean",
        ).round(2)
        result[city] = pivot

    return result
