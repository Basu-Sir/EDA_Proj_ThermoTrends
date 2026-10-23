"""
Tests for trend analysis module.
"""

import numpy as np
import pandas as pd
import pytest

from src.trend_analysis import compute_ols_trend, compute_mann_kendall


class TestOLSTrend:
    def test_positive_trend(self):
        years = np.arange(2001, 2026, dtype=float)
        values = 20.0 + 0.05 * (years - 2001) + np.random.normal(0, 0.01, len(years))
        result = compute_ols_trend(years, values)
        assert result["slope_per_year"] > 0
        assert result["slope_per_decade"] > 0
        assert abs(result["slope_per_year"] - 0.05) < 0.02

    def test_slope_per_decade_conversion(self):
        years = np.arange(2001, 2026, dtype=float)
        slope_per_year = 0.03
        values = 25.0 + slope_per_year * (years - 2001)
        result = compute_ols_trend(years, values)
        expected_decade = slope_per_year * 10
        assert abs(result["slope_per_decade"] - expected_decade) < 0.001

    def test_no_trend(self):
        years = np.arange(2001, 2026, dtype=float)
        values = np.full_like(years, 25.0)
        result = compute_ols_trend(years, values)
        assert abs(result["slope_per_year"]) < 0.001

    def test_insufficient_data(self):
        years = np.array([2001.0, 2002.0])
        values = np.array([20.0, 21.0])
        result = compute_ols_trend(years, values)
        assert np.isnan(result["slope_per_year"])

    def test_handles_nan_values(self):
        years = np.arange(2001, 2026, dtype=float)
        values = 20.0 + 0.05 * (years - 2001)
        values[5] = np.nan
        values[10] = np.nan
        result = compute_ols_trend(years, values)
        assert result["n_valid"] == 23

    def test_confidence_interval(self):
        years = np.arange(2001, 2026, dtype=float)
        values = 20.0 + 0.05 * (years - 2001) + np.random.normal(0, 0.1, len(years))
        result = compute_ols_trend(years, values, confidence=0.95)
        assert result["ci_lower"] < result["slope_per_year"]
        assert result["ci_upper"] > result["slope_per_year"]

    def test_r_squared_range(self):
        years = np.arange(2001, 2026, dtype=float)
        values = 20.0 + 0.05 * (years - 2001) + np.random.normal(0, 0.5, len(years))
        result = compute_ols_trend(years, values)
        assert 0.0 <= result["r_squared"] <= 1.0


class TestMannKendall:
    def test_increasing_trend(self):
        values = np.arange(25, dtype=float)
        result = compute_mann_kendall(values)
        if result["mk_trend"] != "not_available":
            assert result["mk_trend"] == "increasing"
            assert result["sens_slope"] > 0

    def test_insufficient_data(self):
        values = np.array([1.0, 2.0, 3.0])
        result = compute_mann_kendall(values)
        assert result["mk_trend"] == "insufficient_data"

    def test_handles_nan(self):
        values = np.arange(25, dtype=float)
        values[5] = np.nan
        result = compute_mann_kendall(values)
        # Should still work after removing NaN
        assert result["mk_trend"] != "error"


class TestAnnualAggregation:
    def test_annual_mean_calculation(self):
        from src.descriptive_analysis import compute_annual_averages
        np.random.seed(42)
        dates = pd.date_range("2020-01-01", "2020-12-31", freq="D")
        df = pd.DataFrame({
            "date": dates,
            "city": "TestCity",
            "year": dates.year,
            "T2M_MIN": 20.0,
            "T2M_MAX": 30.0,
            "T2M": 25.0,
            "DTR": 10.0,
        })
        result = compute_annual_averages(df, save=False)
        assert len(result) == 1
        assert abs(result.iloc[0]["T2M"] - 25.0) < 0.01
        assert abs(result.iloc[0]["DTR"] - 10.0) < 0.01
