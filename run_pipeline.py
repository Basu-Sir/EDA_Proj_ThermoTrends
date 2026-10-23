"""
Main pipeline runner.

Orchestrates the complete ThermoTrends India analysis:
1. Data collection from NASA POWER API
2. Preprocessing and quality assessment
3. Feature engineering
4. Descriptive statistics
5. Trend analysis
6. Seasonal analysis
7. Extreme temperature analysis
8. Visualization generation
9. Frontend data export
"""

import sys
import logging
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_collection import fetch_all_cities, test_api_connection, load_cached_raw_data
from src.preprocessing import preprocess
from src.feature_engineering import engineer_features
from src.descriptive_analysis import (
    compute_city_statistics,
    compute_annual_averages,
    compute_monthly_averages,
    compute_seasonal_averages,
)
from src.trend_analysis import analyze_trends, compare_min_max_slopes
from src.seasonal_analysis import (
    compute_monthly_climatology,
    compute_seasonal_statistics,
    compute_seasonal_variation,
)
from src.extreme_analysis import analyze_extremes
from src.visualizations import generate_all_figures
from src.reporting import generate_all_outputs


def setup_logging():
    """Configure logging for the pipeline."""
    log_dir = PROJECT_ROOT / "outputs" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / "pipeline.log", encoding="utf-8"),
        ],
    )


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("=" * 70)
    logger.info("THERMOTRENDS INDIA — ANALYSIS PIPELINE")
    logger.info("=" * 70)

    # -------------------------------------------------------------------
    # 1. DATA COLLECTION
    # -------------------------------------------------------------------
    logger.info("\n>>> PHASE 1: Data Collection")

    # Test API connectivity first
    api_ok = test_api_connection()
    if not api_ok:
        logger.warning("API test failed. Attempting to load cached data...")
        raw_df = load_cached_raw_data()
        if raw_df is None or raw_df.empty:
            logger.error("No cached data available. Cannot proceed.")
            sys.exit(1)
    else:
        raw_df = fetch_all_cities(force_refresh=False)
        if raw_df.empty:
            logger.warning("Fetch returned empty. Trying cached data...")
            raw_df = load_cached_raw_data()
            if raw_df is None or raw_df.empty:
                logger.error("No data available. Cannot proceed.")
                sys.exit(1)

    # Save raw combined
    raw_dir = PROJECT_ROOT / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_df.to_csv(raw_dir / "temperature_raw_combined.csv", index=False)
    logger.info("Raw data: %d records, %d cities", len(raw_df), raw_df["city"].nunique())

    # -------------------------------------------------------------------
    # 2. PREPROCESSING
    # -------------------------------------------------------------------
    logger.info("\n>>> PHASE 2: Preprocessing & Quality Assessment")
    clean_df, quality_df = preprocess(raw_df)

    # -------------------------------------------------------------------
    # 3. FEATURE ENGINEERING
    # -------------------------------------------------------------------
    logger.info("\n>>> PHASE 3: Feature Engineering")
    daily_df = engineer_features(clean_df)

    # -------------------------------------------------------------------
    # 4. DESCRIPTIVE STATISTICS
    # -------------------------------------------------------------------
    logger.info("\n>>> PHASE 4: Descriptive Statistics")
    city_stats = compute_city_statistics(daily_df)
    annual_df = compute_annual_averages(daily_df)
    monthly_df = compute_monthly_averages(daily_df)
    seasonal_df = compute_seasonal_averages(daily_df)

    # -------------------------------------------------------------------
    # 5. TREND ANALYSIS
    # -------------------------------------------------------------------
    logger.info("\n>>> PHASE 5: Trend Analysis")
    trend_df = analyze_trends(annual_df)
    min_max_comp = compare_min_max_slopes(trend_df)
    logger.info("Min vs Max slope comparison:\n%s", min_max_comp.to_string())

    # -------------------------------------------------------------------
    # 6. SEASONAL ANALYSIS
    # -------------------------------------------------------------------
    logger.info("\n>>> PHASE 6: Seasonal Analysis")
    clim_df = compute_monthly_climatology(daily_df)
    seasonal_stats = compute_seasonal_statistics(daily_df)
    seasonal_var = compute_seasonal_variation(clim_df)

    # -------------------------------------------------------------------
    # 7. EXTREME TEMPERATURE ANALYSIS
    # -------------------------------------------------------------------
    logger.info("\n>>> PHASE 7: Extreme Temperature Analysis")
    extreme_results = analyze_extremes(daily_df)

    # -------------------------------------------------------------------
    # 8. VISUALIZATIONS
    # -------------------------------------------------------------------
    logger.info("\n>>> PHASE 8: Generating Visualizations")
    try:
        generate_all_figures(
            daily_df=daily_df,
            annual_df=annual_df,
            quality_df=quality_df,
            trend_df=trend_df,
            clim_df=clim_df,
            extreme_annual_df=extreme_results["annual"],
        )
    except Exception as e:
        logger.error("Visualization generation failed: %s", e, exc_info=True)

    # -------------------------------------------------------------------
    # 9. FRONTEND DATA EXPORT
    # -------------------------------------------------------------------
    logger.info("\n>>> PHASE 9: Generating Frontend Data")
    generate_all_outputs(
        daily_df=daily_df,
        annual_df=annual_df,
        monthly_df=monthly_df,
        seasonal_df=seasonal_df,
        trend_df=trend_df,
        clim_df=clim_df,
        extreme_annual_df=extreme_results["annual"],
        quality_df=quality_df,
        city_stats_df=city_stats,
        min_max_comparison=min_max_comp,
    )

    # -------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------
    logger.info("\n" + "=" * 70)
    logger.info("PIPELINE COMPLETE")
    logger.info("=" * 70)
    logger.info("Cities analyzed: %d", daily_df["city"].nunique())
    logger.info("Daily records: %d", len(daily_df))
    logger.info("Annual records: %d", len(annual_df))
    logger.info("Trend results: %d", len(trend_df))
    logger.info("Outputs in: %s", PROJECT_ROOT / "data" / "processed")
    logger.info("Figures in: %s", PROJECT_ROOT / "outputs" / "figures")


if __name__ == "__main__":
    main()
