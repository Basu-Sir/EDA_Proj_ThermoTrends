"""
Tests for feature engineering module.
"""

import numpy as np
import pandas as pd
import pytest


def make_sample_df(n=365):
    """Create a sample DataFrame with realistic temperature data."""
    np.random.seed(42)
    dates = pd.date_range("2020-01-01", periods=n, freq="D")
    return pd.DataFrame({
        "date": dates,
        "city": "TestCity",
        "latitude": 28.6,
        "longitude": 77.2,
        "T2M_MIN": np.random.uniform(10, 25, n),
        "T2M_MAX": np.random.uniform(25, 40, n),
        "T2M": np.random.uniform(18, 32, n),
    })


class TestDTR:
    def test_dtr_calculation(self):
        from src.feature_engineering import add_dtr
        df = make_sample_df(10)
        df["T2M_MIN"] = 20.0
        df["T2M_MAX"] = 35.0
        result = add_dtr(df)
        assert (result["DTR"] == 15.0).all()

    def test_dtr_with_nan(self):
        from src.feature_engineering import add_dtr
        df = make_sample_df(10)
        df.loc[0, "T2M_MIN"] = np.nan
        result = add_dtr(df)
        assert pd.isna(result.loc[0, "DTR"])

    def test_negative_dtr_warning(self):
        from src.feature_engineering import add_dtr
        df = make_sample_df(10)
        df.loc[0, "T2M_MIN"] = 35.0
        df.loc[0, "T2M_MAX"] = 25.0
        result = add_dtr(df)
        assert result.loc[0, "DTR"] < 0


class TestTemporalFeatures:
    def test_year_extraction(self):
        from src.feature_engineering import add_temporal_features
        df = make_sample_df(10)
        result = add_temporal_features(df)
        assert result.loc[0, "year"] == 2020
        assert "month" in result.columns
        assert "month_name" in result.columns
        assert "day_of_year" in result.columns

    def test_leap_year(self):
        from src.feature_engineering import add_temporal_features
        # 2020 is a leap year
        dates = pd.date_range("2020-01-01", "2020-12-31", freq="D")
        df = pd.DataFrame({
            "date": dates,
            "city": "TestCity",
            "latitude": 28.6, "longitude": 77.2,
            "T2M_MIN": 20.0, "T2M_MAX": 30.0, "T2M": 25.0,
        })
        result = add_temporal_features(df)
        assert len(result) == 366  # Leap year
        feb29 = result[result["date"] == "2020-02-29"]
        assert len(feb29) == 1
        assert feb29.iloc[0]["month"] == 2
        assert feb29.iloc[0]["day_of_year"] == 60

    def test_complete_daily_range(self):
        from src.feature_engineering import add_temporal_features
        dates = pd.date_range("2021-01-01", "2021-12-31", freq="D")
        df = pd.DataFrame({
            "date": dates,
            "city": "TestCity",
            "latitude": 28.6, "longitude": 77.2,
            "T2M_MIN": 20.0, "T2M_MAX": 30.0, "T2M": 25.0,
        })
        result = add_temporal_features(df)
        assert len(result) == 365  # Non-leap year


class TestSeasonMapping:
    def test_season_assignment(self):
        from src.feature_engineering import add_temporal_features, add_season
        dates = pd.date_range("2020-01-01", "2020-12-31", freq="D")
        df = pd.DataFrame({
            "date": dates,
            "city": "TestCity",
            "latitude": 28.6, "longitude": 77.2,
            "T2M_MIN": 20.0, "T2M_MAX": 30.0, "T2M": 25.0,
        })
        df = add_temporal_features(df)
        result = add_season(df)

        # January -> Winter
        jan_rows = result[result["month"] == 1]
        assert (jan_rows["season"] == "Winter").all()

        # April -> Pre-monsoon
        apr_rows = result[result["month"] == 4]
        assert (apr_rows["season"] == "Pre-monsoon").all()

        # July -> Monsoon
        jul_rows = result[result["month"] == 7]
        assert (jul_rows["season"] == "Monsoon").all()

        # October -> Post-monsoon
        oct_rows = result[result["month"] == 10]
        assert (oct_rows["season"] == "Post-monsoon").all()

    def test_december_season_year(self):
        from src.feature_engineering import add_temporal_features, add_season
        dates = pd.date_range("2020-12-01", "2020-12-31", freq="D")
        df = pd.DataFrame({
            "date": dates,
            "city": "TestCity",
            "latitude": 28.6, "longitude": 77.2,
            "T2M_MIN": 20.0, "T2M_MAX": 30.0, "T2M": 25.0,
        })
        df = add_temporal_features(df)
        result = add_season(df)

        # December should be Winter
        assert (result["season"] == "Winter").all()
        # December 2020 should have season_year = 2021
        assert (result["season_year"] == 2021).all()
