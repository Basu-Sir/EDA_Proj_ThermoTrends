"""
Visualization module.

Generates publication-quality matplotlib/seaborn charts for the EDA analysis.
All figures saved to outputs/figures/ as high-resolution PNGs.
"""

import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Style configuration
# ---------------------------------------------------------------------------

# Warm editorial palette matching the website theme
COLORS = {
    "primary": "#355E48",       # Forest green
    "secondary": "#9CAF88",     # Sage
    "accent": "#C66A4A",        # Terracotta
    "text": "#302F29",          # Charcoal
    "text_secondary": "#77746B",# Warm gray
    "bg": "#F7F4EC",            # Ivory
    "card": "#FFFEFA",          # Warm white
    "border": "#DCD5C8",        # Taupe
}

CITY_PALETTE = [
    "#355E48", "#C66A4A", "#9CAF88", "#6B8E8A", "#D4A574",
    "#7B6B5D", "#A0522D", "#708090", "#BDB76B", "#8FBC8F",
    "#CD853F", "#5F9EA0",
]

SEASON_ORDER = ["Winter", "Pre-monsoon", "Monsoon", "Post-monsoon"]
MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _fig_dir() -> Path:
    d = _get_project_root() / "outputs" / "figures"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _load_settings() -> dict:
    root = _get_project_root()
    with open(root / "config" / "settings.json", "r", encoding="utf-8") as f:
        return json.load(f)


def _setup_style():
    """Set consistent matplotlib style."""
    plt.rcParams.update({
        "figure.facecolor": COLORS["bg"],
        "axes.facecolor": COLORS["card"],
        "axes.edgecolor": COLORS["border"],
        "axes.labelcolor": COLORS["text"],
        "text.color": COLORS["text"],
        "xtick.color": COLORS["text_secondary"],
        "ytick.color": COLORS["text_secondary"],
        "grid.color": COLORS["border"],
        "grid.alpha": 0.5,
        "font.family": "sans-serif",
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "legend.fontsize": 10,
        "figure.dpi": 150,
    })
    sns.set_palette(CITY_PALETTE)


# ---------------------------------------------------------------------------
# 1. Data quality overview
# ---------------------------------------------------------------------------

def plot_data_quality(quality_df: pd.DataFrame):
    """Plot data quality overview — expected vs observed records and issues."""
    _setup_style()
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Records comparison
    ax = axes[0]
    cities = quality_df["city"].values
    x = np.arange(len(cities))
    w = 0.35
    ax.bar(x - w/2, quality_df["expected_records"], w, label="Expected",
           color=COLORS["secondary"], edgecolor=COLORS["border"])
    ax.bar(x + w/2, quality_df["observed_records"], w, label="Observed",
           color=COLORS["primary"], edgecolor=COLORS["border"])
    ax.set_xticks(x)
    ax.set_xticklabels(cities, rotation=45, ha="right", fontsize=9)
    ax.set_ylabel("Number of Records")
    ax.set_title("Expected vs Observed Records by City")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    # Missing dates
    ax = axes[1]
    missing = quality_df["missing_dates"].values if "missing_dates" in quality_df.columns else np.zeros(len(cities))
    bars = ax.barh(cities, missing, color=COLORS["accent"], edgecolor=COLORS["border"])
    ax.set_xlabel("Missing Dates")
    ax.set_title("Missing Date Count by City")
    ax.grid(axis="x", alpha=0.3)
    ax.invert_yaxis()

    plt.tight_layout()
    path = _fig_dir() / "01_data_quality_overview.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved: %s", path)


# ---------------------------------------------------------------------------
# 2. Temperature distributions
# ---------------------------------------------------------------------------

def plot_temperature_distributions(df: pd.DataFrame):
    """Histograms of T2M_MIN, T2M_MAX, T2M for all cities combined."""
    _setup_style()
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    variables = ["T2M_MIN", "T2M_MAX", "T2M"]
    titles = ["Daily Minimum Temperature", "Daily Maximum Temperature", "Daily Mean Temperature"]
    colors = [COLORS["primary"], COLORS["accent"], COLORS["secondary"]]

    for ax, var, title, color in zip(axes, variables, titles, colors):
        data = df[var].dropna()
        ax.hist(data, bins=60, color=color, alpha=0.75, edgecolor="white", linewidth=0.5)
        ax.axvline(data.mean(), color=COLORS["text"], linestyle="--", linewidth=1.5, label=f"Mean: {data.mean():.1f}°C")
        ax.set_xlabel("Temperature (°C)")
        ax.set_ylabel("Frequency")
        ax.set_title(title)
        ax.legend(fontsize=9)
        ax.grid(axis="y", alpha=0.3)

    plt.suptitle("Temperature Distributions — All Cities (2001–2025)", fontsize=15, y=1.02)
    plt.tight_layout()
    path = _fig_dir() / "02_temperature_distributions.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved: %s", path)


# ---------------------------------------------------------------------------
# 3. City-wise boxplots
# ---------------------------------------------------------------------------

def plot_city_boxplots(df: pd.DataFrame):
    """City-wise temperature boxplots for each variable."""
    _setup_style()
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    variables = ["T2M_MIN", "T2M_MAX", "T2M", "DTR"]
    titles = ["Daily Minimum (°C)", "Daily Maximum (°C)", "Daily Mean (°C)", "DTR (°C)"]

    city_order = sorted(df["city"].unique())

    for ax, var, title in zip(axes.flat, variables, titles):
        if var not in df.columns:
            continue
        sns.boxplot(
            data=df, x="city", y=var, order=city_order,
            palette=CITY_PALETTE[:len(city_order)],
            fliersize=1, linewidth=0.8, ax=ax,
        )
        ax.set_xlabel("")
        ax.set_ylabel(title)
        ax.set_title(f"{title} by City")
        ax.tick_params(axis="x", rotation=45)
        ax.grid(axis="y", alpha=0.3)

    plt.suptitle("Temperature Distributions by City (2001–2025)", fontsize=15, y=1.01)
    plt.tight_layout()
    path = _fig_dir() / "03_city_boxplots.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved: %s", path)


# ---------------------------------------------------------------------------
# 4-6. Annual time series
# ---------------------------------------------------------------------------

def plot_annual_time_series(annual_df: pd.DataFrame, variable: str, title: str, filename: str):
    """Plot annual time series for a given variable, one line per city."""
    _setup_style()
    fig, ax = plt.subplots(figsize=(14, 7))

    cities = sorted(annual_df["city"].unique())
    for i, city in enumerate(cities):
        city_data = annual_df[annual_df["city"] == city].sort_values("year")
        ax.plot(city_data["year"], city_data[variable],
                marker="o", markersize=3, linewidth=1.5,
                color=CITY_PALETTE[i % len(CITY_PALETTE)],
                label=city, alpha=0.85)

    ax.set_xlabel("Year")
    ax.set_ylabel(f"{title} (°C)")
    ax.set_title(f"Annual {title} by City (2001–2025)")
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=9)
    ax.grid(alpha=0.3)
    ax.xaxis.set_major_locator(mticker.MultipleLocator(2))

    plt.tight_layout()
    path = _fig_dir() / filename
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved: %s", path)


def plot_all_annual_series(annual_df: pd.DataFrame):
    """Generate annual time series for T2M_MIN, T2M_MAX, T2M."""
    plot_annual_time_series(annual_df, "T2M_MIN", "Minimum Temperature",
                           "04_annual_tmin_series.png")
    plot_annual_time_series(annual_df, "T2M_MAX", "Maximum Temperature",
                           "05_annual_tmax_series.png")
    plot_annual_time_series(annual_df, "T2M", "Mean Temperature",
                           "06_annual_tmean_series.png")


# ---------------------------------------------------------------------------
# 7. Regression trend plots
# ---------------------------------------------------------------------------

def plot_trend_with_regression(annual_df: pd.DataFrame, trend_df: pd.DataFrame):
    """Plot annual values with fitted OLS regression lines for each city-variable."""
    _setup_style()
    variables = ["T2M_MIN", "T2M_MAX", "T2M", "DTR"]
    titles = {"T2M_MIN": "Minimum Temperature", "T2M_MAX": "Maximum Temperature",
              "T2M": "Mean Temperature", "DTR": "Daily Temperature Range"}

    for var in variables:
        var_trends = trend_df[trend_df["variable"] == var]
        cities = sorted(var_trends["city"].unique())
        n_cities = len(cities)
        ncols = 3
        nrows = (n_cities + ncols - 1) // ncols

        fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4 * nrows))
        axes = np.atleast_2d(axes)

        for idx, city in enumerate(cities):
            row, col = idx // ncols, idx % ncols
            ax = axes[row, col]

            city_annual = annual_df[annual_df["city"] == city].sort_values("year")
            city_trend = var_trends[var_trends["city"] == city].iloc[0] if len(var_trends[var_trends["city"] == city]) > 0 else None

            ax.scatter(city_annual["year"], city_annual[var],
                       s=18, color=COLORS["primary"], alpha=0.7, zorder=3)

            if city_trend is not None and np.isfinite(city_trend["ols_slope_per_year"]):
                x = city_annual["year"].values
                y_fit = city_trend["ols_intercept"] + city_trend["ols_slope_per_year"] * x
                ax.plot(x, y_fit, color=COLORS["accent"], linewidth=2, zorder=4)
                slope_label = f"{city_trend['ols_slope_per_decade']:.3f} °C/dec"
                sig = "★" if city_trend.get("ols_significant", False) else ""
                ax.text(0.05, 0.95, f"{slope_label} {sig}",
                        transform=ax.transAxes, fontsize=8, va="top",
                        color=COLORS["accent"])

            ax.set_title(city, fontsize=11)
            ax.grid(alpha=0.2)
            ax.tick_params(labelsize=8)

        # Remove empty axes
        for idx in range(n_cities, nrows * ncols):
            row, col = idx // ncols, idx % ncols
            axes[row, col].set_visible(False)

        fig.suptitle(f"Annual {titles[var]} Trends with OLS Regression", fontsize=14, y=1.01)
        plt.tight_layout()
        path = _fig_dir() / f"07_trend_regression_{var.lower()}.png"
        fig.savefig(path, dpi=300, bbox_inches="tight")
        plt.close(fig)
        logger.info("Saved: %s", path)


# ---------------------------------------------------------------------------
# 8. City-variable trend heatmap
# ---------------------------------------------------------------------------

def plot_trend_heatmap(trend_df: pd.DataFrame):
    """Heatmap of OLS slopes (°C/decade) by city and variable."""
    _setup_style()

    pivot = trend_df.pivot_table(
        index="city", columns="variable", values="ols_slope_per_decade"
    )
    var_order = ["T2M_MIN", "T2M_MAX", "T2M", "DTR"]
    pivot = pivot[[v for v in var_order if v in pivot.columns]]

    fig, ax = plt.subplots(figsize=(8, 10))
    sns.heatmap(
        pivot, annot=True, fmt=".3f", cmap="RdYlGn_r",
        center=0, linewidths=0.5, linecolor=COLORS["border"],
        cbar_kws={"label": "Trend (°C/decade)"}, ax=ax,
    )
    ax.set_title("Temperature Trend Estimates by City and Variable\n(°C per decade, OLS)", fontsize=13)
    ax.set_ylabel("")
    ax.set_xlabel("")

    plt.tight_layout()
    path = _fig_dir() / "08_trend_heatmap.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved: %s", path)


# ---------------------------------------------------------------------------
# 9. Month-by-year heatmaps
# ---------------------------------------------------------------------------

def plot_month_year_heatmaps(df: pd.DataFrame, variable: str = "T2M"):
    """Generate month-by-year heatmaps per city."""
    _setup_style()
    cities = sorted(df["city"].unique())
    n_cities = len(cities)
    ncols = 2
    nrows = (n_cities + ncols - 1) // ncols

    fig, axes = plt.subplots(nrows, ncols, figsize=(14, 4 * nrows))
    axes = np.atleast_2d(axes)

    for idx, city in enumerate(cities):
        row, col = idx // ncols, idx % ncols
        ax = axes[row, col]

        city_data = df[df["city"] == city]
        pivot = city_data.pivot_table(values=variable, index="month", columns="year", aggfunc="mean")

        sns.heatmap(
            pivot, ax=ax, cmap="YlOrRd", linewidths=0.2,
            yticklabels=MONTH_ORDER[:len(pivot)],
            cbar_kws={"shrink": 0.8, "label": "°C"},
        )
        ax.set_title(city, fontsize=11)
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.tick_params(labelsize=8)

    for idx in range(n_cities, nrows * ncols):
        row, col = idx // ncols, idx % ncols
        axes[row, col].set_visible(False)

    fig.suptitle(f"Monthly {variable} Heatmaps by City (2001–2025)", fontsize=14, y=1.01)
    plt.tight_layout()
    path = _fig_dir() / "09_month_year_heatmaps.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved: %s", path)


# ---------------------------------------------------------------------------
# 10. Monthly profiles
# ---------------------------------------------------------------------------

def plot_monthly_profiles(clim_df: pd.DataFrame):
    """City-wise monthly temperature profiles."""
    _setup_style()
    fig, ax = plt.subplots(figsize=(14, 7))

    cities = sorted(clim_df["city"].unique())
    for i, city in enumerate(cities):
        city_data = clim_df[clim_df["city"] == city].sort_values("month")
        ax.plot(city_data["month"], city_data["T2M_mean"],
                marker="o", markersize=4, linewidth=1.8,
                color=CITY_PALETTE[i % len(CITY_PALETTE)],
                label=city, alpha=0.85)

    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(MONTH_ORDER)
    ax.set_xlabel("Month")
    ax.set_ylabel("Mean Temperature (°C)")
    ax.set_title("Monthly Temperature Profiles by City (Long-term Averages)")
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=9)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    path = _fig_dir() / "10_monthly_profiles.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved: %s", path)


# ---------------------------------------------------------------------------
# 11. Seasonal boxplots
# ---------------------------------------------------------------------------

def plot_seasonal_boxplots(df: pd.DataFrame):
    """Seasonal temperature boxplots for all cities."""
    _setup_style()
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    variables = ["T2M_MIN", "T2M_MAX", "T2M", "DTR"]
    titles = ["Minimum Temp (°C)", "Maximum Temp (°C)", "Mean Temp (°C)", "DTR (°C)"]

    for ax, var, title in zip(axes.flat, variables, titles):
        if var not in df.columns:
            continue
        sns.boxplot(
            data=df, x="season", y=var,
            order=SEASON_ORDER,
            palette=[COLORS["primary"], COLORS["accent"], COLORS["secondary"], "#D4A574"],
            fliersize=1, linewidth=0.8, ax=ax,
        )
        ax.set_xlabel("")
        ax.set_ylabel(title)
        ax.set_title(f"{title} by Season")
        ax.grid(axis="y", alpha=0.3)

    plt.suptitle("Seasonal Temperature Distributions — All Cities (2001–2025)", fontsize=14, y=1.01)
    plt.tight_layout()
    path = _fig_dir() / "11_seasonal_boxplots.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved: %s", path)


# ---------------------------------------------------------------------------
# 12. Annual DTR trends
# ---------------------------------------------------------------------------

def plot_dtr_annual_trends(annual_df: pd.DataFrame, trend_df: pd.DataFrame):
    """Plot annual DTR time series with trend lines."""
    plot_annual_time_series(annual_df, "DTR", "Daily Temperature Range",
                           "12_annual_dtr_trends.png")


# ---------------------------------------------------------------------------
# 13. DTR distributions by city
# ---------------------------------------------------------------------------

def plot_dtr_distributions(df: pd.DataFrame):
    """DTR distribution by city — violin/box plots."""
    _setup_style()
    fig, ax = plt.subplots(figsize=(14, 7))

    city_order = sorted(df["city"].unique())
    sns.violinplot(
        data=df, x="city", y="DTR", order=city_order,
        palette=CITY_PALETTE[:len(city_order)],
        inner="box", linewidth=0.8, ax=ax, cut=0,
    )
    ax.set_xlabel("")
    ax.set_ylabel("Daily Temperature Range (°C)")
    ax.set_title("DTR Distributions by City (2001–2025)")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    path = _fig_dir() / "13_dtr_distributions.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved: %s", path)


# ---------------------------------------------------------------------------
# 14-15. Extreme frequency comparisons
# ---------------------------------------------------------------------------

def plot_extreme_frequencies(extreme_annual_df: pd.DataFrame):
    """Plot annual hot-day and warm-night frequencies by city."""
    _setup_style()

    for event, col, title, filename in [
        ("hot_days", "hot_days", "Hot Day Frequency", "14_hot_day_frequency.png"),
        ("warm_nights", "warm_nights", "Warm Night Frequency", "15_warm_night_frequency.png"),
    ]:
        fig, ax = plt.subplots(figsize=(14, 7))
        cities = sorted(extreme_annual_df["city"].unique())

        for i, city in enumerate(cities):
            city_data = extreme_annual_df[extreme_annual_df["city"] == city].sort_values("year")
            ax.plot(city_data["year"], city_data[col],
                    marker="o", markersize=3, linewidth=1.5,
                    color=CITY_PALETTE[i % len(CITY_PALETTE)],
                    label=city, alpha=0.85)

        ax.set_xlabel("Year")
        ax.set_ylabel(f"Number of {title.split()[0]} {title.split()[1]}s")
        ax.set_title(f"Annual {title} by City (2001–2025)")
        ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=9)
        ax.grid(alpha=0.3)
        ax.xaxis.set_major_locator(mticker.MultipleLocator(2))

        plt.tight_layout()
        path = _fig_dir() / filename
        fig.savefig(path, dpi=300, bbox_inches="tight")
        plt.close(fig)
        logger.info("Saved: %s", path)


# ---------------------------------------------------------------------------
# 16. Comparative trend summary
# ---------------------------------------------------------------------------

def plot_comparative_trends(trend_df: pd.DataFrame):
    """Bar chart comparing trend slopes across cities for each variable."""
    _setup_style()
    variables = ["T2M_MIN", "T2M_MAX", "T2M", "DTR"]
    titles = {"T2M_MIN": "Min Temp", "T2M_MAX": "Max Temp", "T2M": "Mean Temp", "DTR": "DTR"}

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    for ax, var in zip(axes.flat, variables):
        var_data = trend_df[trend_df["variable"] == var].sort_values("ols_slope_per_decade")
        colors = [COLORS["accent"] if v > 0 else COLORS["primary"]
                  for v in var_data["ols_slope_per_decade"]]

        ax.barh(var_data["city"], var_data["ols_slope_per_decade"],
                color=colors, edgecolor=COLORS["border"], linewidth=0.5)
        ax.axvline(0, color=COLORS["text"], linewidth=0.8, linestyle="-")
        ax.set_xlabel("Trend (°C/decade)")
        ax.set_title(f"{titles[var]} Trend by City")
        ax.grid(axis="x", alpha=0.3)

    plt.suptitle("Comparative Temperature Trend Estimates (°C/decade)", fontsize=14, y=1.01)
    plt.tight_layout()
    path = _fig_dir() / "16_comparative_trends.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved: %s", path)


# ---------------------------------------------------------------------------
# Generate all figures
# ---------------------------------------------------------------------------

def generate_all_figures(
    daily_df: pd.DataFrame,
    annual_df: pd.DataFrame,
    quality_df: pd.DataFrame,
    trend_df: pd.DataFrame,
    clim_df: pd.DataFrame,
    extreme_annual_df: pd.DataFrame,
):
    """Generate all required visualizations."""
    logger.info("=" * 60)
    logger.info("GENERATING ALL FIGURES")

    plot_data_quality(quality_df)
    plot_temperature_distributions(daily_df)
    plot_city_boxplots(daily_df)
    plot_all_annual_series(annual_df)
    plot_trend_with_regression(annual_df, trend_df)
    plot_trend_heatmap(trend_df)
    plot_month_year_heatmaps(daily_df)
    plot_monthly_profiles(clim_df)
    plot_seasonal_boxplots(daily_df)
    plot_dtr_annual_trends(annual_df, trend_df)
    plot_dtr_distributions(daily_df)
    plot_extreme_frequencies(extreme_annual_df)
    plot_comparative_trends(trend_df)

    logger.info("ALL FIGURES GENERATED")
    logger.info("=" * 60)
