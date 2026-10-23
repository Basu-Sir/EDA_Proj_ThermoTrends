"""
Tests for preprocessing module.
"""

import numpy as np
import pandas as pd
import pytest


def make_sample_df(n=100):
    """Create a sample DataFrame for testing."""
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


class TestFillValues:
    def test_replaces_fill_values(self):
        from src.preprocessing import replace_fill_values
        df = make_sample_df(10)
        df.loc[0, "T2M_MIN"] = -999.0
        df.loc[1, "T2M_MAX"] = -999.0
        result = replace_fill_values(df)
        assert pd.isna(result.loc[0, "T2M_MIN"])
        assert pd.isna(result.loc[1, "T2M_MAX"])

    def test_preserves_valid_values(self):
        from src.preprocessing import replace_fill_values
        df = make_sample_df(10)
        result = replace_fill_values(df)
        assert result["T2M_MIN"].notna().all()


class TestDuplicateDetection:
    def test_removes_duplicates(self):
        from src.preprocessing import remove_duplicates
        df = make_sample_df(10)
        df_dup = pd.concat([df, df.iloc[:3]], ignore_index=True)
        result = remove_duplicates(df_dup)
        assert len(result) == len(df)

    def test_no_duplicates_unchanged(self):
        from src.preprocessing import remove_duplicates
        df = make_sample_df(10)
        result = remove_duplicates(df)
        assert len(result) == len(df)


class TestInconsistencyChecks:
    def test_flags_min_gt_max(self):
        from src.preprocessing import check_inconsistencies
        df = make_sample_df(10)
        df.loc[0, "T2M_MIN"] = 35.0
        df.loc[0, "T2M_MAX"] = 25.0
        result = check_inconsistencies(df)
        assert result.loc[0, "flag_min_gt_max"] == True

    def test_flags_mean_outside_bounds(self):
        from src.preprocessing import check_inconsistencies
        df = make_sample_df(10)
        df.loc[0, "T2M_MIN"] = 20.0
        df.loc[0, "T2M_MAX"] = 30.0
        df.loc[0, "T2M"] = 35.0  # Outside bounds
        result = check_inconsistencies(df, tolerance=0.5)
        assert result.loc[0, "flag_mean_outside"] == True

    def test_no_false_flags_on_clean_data(self):
        from src.preprocessing import check_inconsistencies
        df = make_sample_df(10)
        # Ensure consistent data
        df["T2M_MIN"] = 20.0
        df["T2M_MAX"] = 30.0
        df["T2M"] = 25.0
        result = check_inconsistencies(df)
        assert result["flag_min_gt_max"].sum() == 0
        assert result["flag_mean_outside"].sum() == 0


class TestMissingValues:
    def test_detects_nulls(self):
        from src.preprocessing import analyze_missing
        df = make_sample_df(10)
        df.loc[0:2, "T2M_MIN"] = np.nan
        result = analyze_missing(df)
        row = result[result["city"] == "TestCity"].iloc[0]
        assert row["T2M_MIN_null"] == 3

    def test_correct_percentage(self):
        from src.preprocessing import analyze_missing
        df = make_sample_df(100)
        df.loc[0:9, "T2M_MAX"] = np.nan
        result = analyze_missing(df)
        row = result[result["city"] == "TestCity"].iloc[0]
        assert abs(row["T2M_MAX_null_pct"] - 10.0) < 0.01
