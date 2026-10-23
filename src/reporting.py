"""
Reporting module.

Generates machine-readable JSON outputs for the frontend website.
"""

import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def _get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


class NumpyEncoder(json.JSONEncoder):
    """JSON encoder that handles numpy types."""
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            if np.isnan(obj) or np.isinf(obj):
                return None
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        return super().default(obj)


def _save_json(data, filename: str):
    """Save dict/list to JSON in data/processed/."""
    root = _get_project_root()
    out_dir = root / "data" / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, cls=NumpyEncoder, indent=2)
    logger.info("Saved JSON: %s", path)


# ---------------------------------------------------------------------------
# Chart data JSON
# ---------------------------------------------------------------------------

def generate_chart_data(
    daily_df: pd.DataFrame,
    annual_df: pd.DataFrame,
    monthly_df: pd.DataFrame,
    seasonal_df: pd.DataFrame,
    trend_df: pd.DataFrame,
    clim_df: pd.DataFrame,
    extreme_annual_df: pd.DataFrame,
    quality_df: pd.DataFrame,
    city_stats_df: pd.DataFrame,
) -> dict:
    """Generate comprehensive chart data JSON for the frontend."""

    chart_data = {}

    # --- Cities metadata ---
    root = _get_project_root()
    with open(root / "config" / "cities.json", "r", encoding="utf-8") as f:
        cities_cfg = json.load(f)
    chart_data["cities"] = cities_cfg["cities"]

    # --- Annual time series ---
    annual_records = []
    for _, row in annual_df.iterrows():
        record = {
            "city": row["city"],
            "year": int(row["year"]),
        }
        for col in ["T2M_MIN", "T2M_MAX", "T2M", "DTR", "valid_days"]:
            if col in row.index:
                val = row[col]
                record[col] = float(val) if pd.notna(val) else None
        annual_records.append(record)
    chart_data["annual"] = annual_records

    # --- Monthly climatology ---
    if clim_df is not None and not clim_df.empty:
        clim_records = []
        for _, row in clim_df.iterrows():
            record = {"city": row["city"], "month": int(row["month"])}
            for col in clim_df.columns:
                if col not in ["city", "month", "month_name"]:
                    val = row[col]
                    record[col] = float(val) if pd.notna(val) else None
                elif col == "month_name":
                    record[col] = row[col]
            clim_records.append(record)
        chart_data["monthly_climatology"] = clim_records

    # --- Trends ---
    if trend_df is not None and not trend_df.empty:
        trend_records = []
        for _, row in trend_df.iterrows():
            record = {}
            for col in trend_df.columns:
                val = row[col]
                if isinstance(val, (np.floating, float)):
                    record[col] = float(val) if pd.notna(val) else None
                elif isinstance(val, (np.integer, int)):
                    record[col] = int(val)
                elif isinstance(val, bool):
                    record[col] = bool(val)
                else:
                    record[col] = val
            trend_records.append(record)
        chart_data["trends"] = trend_records

    # --- Data quality ---
    if quality_df is not None and not quality_df.empty:
        chart_data["data_quality"] = quality_df.to_dict(orient="records")

    # --- City statistics ---
    if city_stats_df is not None and not city_stats_df.empty:
        stats_records = []
        for _, row in city_stats_df.iterrows():
            record = {}
            for col in city_stats_df.columns:
                val = row[col]
                if isinstance(val, (np.floating, float)):
                    record[col] = float(val) if pd.notna(val) else None
                elif isinstance(val, (np.integer, int)):
                    record[col] = int(val)
                else:
                    record[col] = val
            stats_records.append(record)
        chart_data["city_statistics"] = stats_records

    # --- Extreme annual frequencies ---
    if extreme_annual_df is not None and not extreme_annual_df.empty:
        extreme_records = []
        for _, row in extreme_annual_df.iterrows():
            record = {}
            for col in extreme_annual_df.columns:
                val = row[col]
                if isinstance(val, (np.floating, float)):
                    record[col] = float(val) if pd.notna(val) else None
                elif isinstance(val, (np.integer, int)):
                    record[col] = int(val)
                elif isinstance(val, (np.bool_, bool)):
                    record[col] = bool(val)
                else:
                    record[col] = val
            extreme_records.append(record)
        chart_data["extreme_frequencies"] = extreme_records

    # --- Seasonal data ---
    if seasonal_df is not None and not seasonal_df.empty:
        seasonal_records = []
        for _, row in seasonal_df.iterrows():
            record = {}
            for col in seasonal_df.columns:
                val = row[col]
                if isinstance(val, (np.floating, float)):
                    record[col] = float(val) if pd.notna(val) else None
                elif isinstance(val, (np.integer, int)):
                    record[col] = int(val)
                else:
                    record[col] = val
            seasonal_records.append(record)
        chart_data["seasonal"] = seasonal_records

    _save_json(chart_data, "chart_data.json")
    return chart_data


# ---------------------------------------------------------------------------
# Findings JSON
# ---------------------------------------------------------------------------

def generate_findings(
    trend_df: pd.DataFrame,
    city_stats_df: pd.DataFrame,
    extreme_annual_df: pd.DataFrame,
    quality_df: pd.DataFrame,
    min_max_comparison: pd.DataFrame = None,
) -> dict:
    """
    Generate findings JSON from computed results.
    Each finding references the actual data — never hardcoded conclusions.
    """
    findings = {
        "study_period": "2001-2025",
        "data_source": "NASA POWER Daily (T2M_MIN, T2M_MAX, T2M)",
        "research_questions": [],
    }

    # --- RQ1: Temperature changes over time ---
    rq1 = {
        "id": "rq1",
        "question": "How have minimum, maximum, and mean temperatures changed over the study period (2001–2025)?",
        "findings": [],
    }

    for var, label in [("T2M_MIN", "Minimum"), ("T2M_MAX", "Maximum"), ("T2M", "Mean")]:
        var_trends = trend_df[trend_df["variable"] == var].copy()
        if var_trends.empty:
            continue

        avg_slope = var_trends["ols_slope_per_decade"].mean()
        n_positive = (var_trends["ols_slope_per_decade"] > 0).sum()
        n_significant = var_trends["ols_significant"].sum() if "ols_significant" in var_trends.columns else 0
        strongest = var_trends.loc[var_trends["ols_slope_per_decade"].abs().idxmax()]

        rq1["findings"].append({
            "variable": var,
            "label": f"{label} Temperature",
            "mean_slope_per_decade": round(float(avg_slope), 4),
            "cities_with_positive_trend": int(n_positive),
            "cities_with_significant_trend": int(n_significant),
            "total_cities": len(var_trends),
            "strongest_trend_city": strongest["city"],
            "strongest_trend_slope": round(float(strongest["ols_slope_per_decade"]), 4),
            "unit": "°C/decade",
        })

    findings["research_questions"].append(rq1)

    # --- RQ2: Min vs Max temperature trends ---
    rq2 = {
        "id": "rq2",
        "question": "Do minimum and maximum temperatures exhibit different long-term trends?",
        "findings": [],
    }

    if min_max_comparison is not None and not min_max_comparison.empty:
        n_min_faster = int(min_max_comparison["min_warming_faster"].sum())
        rq2["findings"].append({
            "cities_where_min_warming_faster": n_min_faster,
            "total_cities": len(min_max_comparison),
            "comparison": min_max_comparison.to_dict(orient="records"),
        })

    findings["research_questions"].append(rq2)

    # --- RQ3: Distribution and seasonal patterns ---
    rq3 = {
        "id": "rq3",
        "question": "How do temperature distributions and seasonal patterns vary across cities?",
        "findings": [],
    }

    if city_stats_df is not None and not city_stats_df.empty:
        t2m_stats = city_stats_df[city_stats_df["variable"] == "T2M"]
        if not t2m_stats.empty:
            warmest = t2m_stats.loc[t2m_stats["mean"].idxmax()]
            coolest = t2m_stats.loc[t2m_stats["mean"].idxmin()]
            most_variable = t2m_stats.loc[t2m_stats["std"].idxmax()]

            rq3["findings"].append({
                "warmest_city": warmest["city"],
                "warmest_mean": round(float(warmest["mean"]), 2),
                "coolest_city": coolest["city"],
                "coolest_mean": round(float(coolest["mean"]), 2),
                "most_variable_city": most_variable["city"],
                "most_variable_std": round(float(most_variable["std"]), 2),
                "unit": "°C",
            })

    findings["research_questions"].append(rq3)

    # --- RQ4: DTR trends ---
    rq4 = {
        "id": "rq4",
        "question": "Is the Daily Temperature Range (DTR) increasing or decreasing?",
        "findings": [],
    }

    dtr_trends = trend_df[trend_df["variable"] == "DTR"]
    if not dtr_trends.empty:
        n_increasing = (dtr_trends["ols_slope_per_decade"] > 0).sum()
        n_decreasing = (dtr_trends["ols_slope_per_decade"] < 0).sum()
        avg_dtr_slope = dtr_trends["ols_slope_per_decade"].mean()

        rq4["findings"].append({
            "mean_dtr_slope_per_decade": round(float(avg_dtr_slope), 4),
            "cities_with_increasing_dtr": int(n_increasing),
            "cities_with_decreasing_dtr": int(n_decreasing),
            "total_cities": len(dtr_trends),
            "unit": "°C/decade",
            "note": "Daily minimum temperature is not equivalent to mean nighttime temperature, and daily maximum temperature is not equivalent to mean daytime temperature.",
        })

    findings["research_questions"].append(rq4)

    # --- RQ5: Extreme events ---
    rq5 = {
        "id": "rq5",
        "question": "How frequently do unusually hot days and warm nights occur, and are their frequencies changing?",
        "findings": [],
    }

    if extreme_annual_df is not None and not extreme_annual_df.empty:
        # Overall averages
        city_avg = extreme_annual_df.groupby("city").agg(
            mean_hot_days=("hot_days", "mean"),
            mean_warm_nights=("warm_nights", "mean"),
        ).reset_index()

        most_hot = city_avg.loc[city_avg["mean_hot_days"].idxmax()]
        most_warm = city_avg.loc[city_avg["mean_warm_nights"].idxmax()]

        rq5["findings"].append({
            "city_with_most_hot_days": most_hot["city"],
            "avg_hot_days_per_year": round(float(most_hot["mean_hot_days"]), 1),
            "city_with_most_warm_nights": most_warm["city"],
            "avg_warm_nights_per_year": round(float(most_warm["mean_warm_nights"]), 1),
            "threshold_method": "City-specific calendar-month 90th percentile of full study period (2001-2025)",
        })

    findings["research_questions"].append(rq5)

    # --- RQ6: Data quality ---
    rq6 = {
        "id": "rq6",
        "question": "How do data quality, missing observations, outliers, and methodological limitations affect interpretation?",
        "findings": [],
    }

    if quality_df is not None and not quality_df.empty:
        total_expected = quality_df["expected_records"].sum()
        total_observed = quality_df["observed_records"].sum()
        completeness = round(100 * total_observed / total_expected, 2) if total_expected > 0 else 0

        rq6["findings"].append({
            "total_expected_records": int(total_expected),
            "total_observed_records": int(total_observed),
            "overall_completeness_pct": completeness,
            "cities_analyzed": len(quality_df),
        })

    findings["research_questions"].append(rq6)

    _save_json(findings, "findings.json")
    return findings


# ---------------------------------------------------------------------------
# Generate all outputs
# ---------------------------------------------------------------------------

def generate_all_outputs(
    daily_df, annual_df, monthly_df, seasonal_df,
    trend_df, clim_df, extreme_annual_df,
    quality_df, city_stats_df, min_max_comparison=None,
):
    """Generate all machine-readable outputs for the frontend."""
    logger.info("Generating frontend data outputs...")

    chart_data = generate_chart_data(
        daily_df, annual_df, monthly_df, seasonal_df,
        trend_df, clim_df, extreme_annual_df,
        quality_df, city_stats_df,
    )

    findings = generate_findings(
        trend_df, city_stats_df, extreme_annual_df,
        quality_df, min_max_comparison,
    )

    logger.info("All frontend data outputs generated.")
    return chart_data, findings
