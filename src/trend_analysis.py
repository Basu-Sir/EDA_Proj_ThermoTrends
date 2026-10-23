"""
Long-term trend analysis module.

OLS regression, Mann-Kendall test, and Sen's slope for annual temperature trends.
"""

import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as scipy_stats

logger = logging.getLogger(__name__)


def _get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _load_settings() -> dict:
    root = _get_project_root()
    with open(root / "config" / "settings.json", "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# OLS trend for a single city-variable
# ---------------------------------------------------------------------------

def compute_ols_trend(years: np.ndarray, values: np.ndarray, confidence: float = 0.95) -> dict:
    """
    Fit OLS regression: value = slope * year + intercept.

    Returns dict with slope, slope_per_decade, intercept, r_squared,
    p_value, std_err, conf_interval, n_valid.
    """
    mask = np.isfinite(values) & np.isfinite(years)
    y = values[mask]
    x = years[mask]

    if len(x) < 3:
        return {
            "slope_per_year": np.nan, "slope_per_decade": np.nan,
            "intercept": np.nan, "r_squared": np.nan,
            "p_value": np.nan, "std_err": np.nan,
            "ci_lower": np.nan, "ci_upper": np.nan,
            "n_valid": len(x),
        }

    result = scipy_stats.linregress(x, y)
    slope = result.slope
    intercept = result.intercept
    r_squared = result.rvalue ** 2
    p_value = result.pvalue
    std_err = result.stderr

    # Confidence interval for slope
    dof = len(x) - 2
    t_crit = scipy_stats.t.ppf((1 + confidence) / 2, dof)
    ci_lower = slope - t_crit * std_err
    ci_upper = slope + t_crit * std_err

    return {
        "slope_per_year": round(slope, 6),
        "slope_per_decade": round(slope * 10, 4),
        "intercept": round(intercept, 4),
        "r_squared": round(r_squared, 4),
        "p_value": round(p_value, 6),
        "std_err": round(std_err, 6),
        "ci_lower": round(ci_lower, 6),
        "ci_upper": round(ci_upper, 6),
        "n_valid": int(len(x)),
    }


# ---------------------------------------------------------------------------
# Mann-Kendall + Sen's slope
# ---------------------------------------------------------------------------

def compute_mann_kendall(values: np.ndarray) -> dict:
    """
    Compute Mann-Kendall trend test and Sen's slope.
    Uses pymannkendall if available, otherwise returns NaN.
    """
    clean = values[np.isfinite(values)]
    if len(clean) < 5:
        return {
            "mk_trend": "insufficient_data",
            "mk_p_value": np.nan,
            "mk_z_score": np.nan,
            "sens_slope": np.nan,
            "sens_slope_per_decade": np.nan,
        }

    try:
        import pymannkendall as mk
        result = mk.original_test(clean)
        return {
            "mk_trend": result.trend,
            "mk_p_value": round(result.p, 6),
            "mk_z_score": round(result.z, 4),
            "sens_slope": round(result.slope, 6),
            "sens_slope_per_decade": round(result.slope * 10, 4),
        }
    except ImportError:
        logger.warning("pymannkendall not installed. Skipping MK test.")
        return {
            "mk_trend": "not_available",
            "mk_p_value": np.nan,
            "mk_z_score": np.nan,
            "sens_slope": np.nan,
            "sens_slope_per_decade": np.nan,
        }
    except Exception as e:
        logger.warning("Mann-Kendall test failed: %s", e)
        return {
            "mk_trend": "error",
            "mk_p_value": np.nan,
            "mk_z_score": np.nan,
            "sens_slope": np.nan,
            "sens_slope_per_decade": np.nan,
        }


# ---------------------------------------------------------------------------
# Full trend analysis for all cities and variables
# ---------------------------------------------------------------------------

def analyze_trends(annual_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute OLS and Mann-Kendall trends for each city-variable combination.

    Parameters
    ----------
    annual_df : pd.DataFrame
        Output of descriptive_analysis.compute_annual_averages().
        Must have columns: city, year, T2M_MIN, T2M_MAX, T2M, DTR.

    Returns
    -------
    pd.DataFrame
        Trend results with one row per city-variable combination.
    """
    settings = _load_settings()
    confidence = settings["analysis"]["confidence_level"]
    min_years = settings["analysis"]["min_valid_years_for_trend"]
    variables = ["T2M_MIN", "T2M_MAX", "T2M", "DTR"]

    rows = []
    for city in sorted(annual_df["city"].unique()):
        city_df = annual_df[annual_df["city"] == city].sort_values("year")

        for var in variables:
            if var not in city_df.columns:
                continue

            years = city_df["year"].values.astype(float)
            values = city_df[var].values.astype(float)

            n_valid = np.sum(np.isfinite(values))
            if n_valid < min_years:
                logger.warning(
                    "%s/%s: only %d valid years (need %d). Skipping.",
                    city, var, n_valid, min_years,
                )

            # OLS
            ols = compute_ols_trend(years, values, confidence)

            # Mann-Kendall
            mk = compute_mann_kendall(values)

            row = {"city": city, "variable": var}
            row.update({f"ols_{k}": v for k, v in ols.items()})
            row.update(mk)

            # Significance label
            alpha = settings["analysis"]["mann_kendall_significance"]
            if not np.isnan(ols["p_value"]):
                row["ols_significant"] = ols["p_value"] < alpha
            else:
                row["ols_significant"] = None

            rows.append(row)

    result = pd.DataFrame(rows)

    # Save
    root = _get_project_root()
    out_dir = root / "data" / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    result.to_csv(out_dir / "trend_results.csv", index=False)
    logger.info("Trend results saved: %d rows", len(result))

    return result


# ---------------------------------------------------------------------------
# Comparison helpers
# ---------------------------------------------------------------------------

def compare_min_max_slopes(trend_df: pd.DataFrame) -> pd.DataFrame:
    """
    For each city, compare T2M_MIN and T2M_MAX trend slopes.
    Returns DataFrame with per-city slope comparison.
    """
    min_trends = trend_df[trend_df["variable"] == "T2M_MIN"][
        ["city", "ols_slope_per_decade", "sens_slope_per_decade"]
    ].rename(columns={
        "ols_slope_per_decade": "min_ols_slope_decade",
        "sens_slope_per_decade": "min_sens_slope_decade",
    })

    max_trends = trend_df[trend_df["variable"] == "T2M_MAX"][
        ["city", "ols_slope_per_decade", "sens_slope_per_decade"]
    ].rename(columns={
        "ols_slope_per_decade": "max_ols_slope_decade",
        "sens_slope_per_decade": "max_sens_slope_decade",
    })

    merged = pd.merge(min_trends, max_trends, on="city")
    merged["ols_min_minus_max"] = (
        merged["min_ols_slope_decade"] - merged["max_ols_slope_decade"]
    ).round(4)
    merged["min_warming_faster"] = merged["min_ols_slope_decade"] > merged["max_ols_slope_decade"]

    return merged
