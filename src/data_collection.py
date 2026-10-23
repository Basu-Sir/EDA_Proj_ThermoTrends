"""
NASA POWER API data collection module.

Fetches daily T2M_MIN, T2M_MAX, T2M for selected Indian cities (2001-2025).
Implements retries with exponential backoff, caching, and error handling.
"""

import json
import os
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
import requests

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
logger = logging.getLogger(__name__)


def _get_project_root() -> Path:
    """Return the project root (thermotrends-india/)."""
    return Path(__file__).resolve().parent.parent


def load_config():
    """Load cities and settings JSON from config/."""
    root = _get_project_root()
    with open(root / "config" / "cities.json", "r", encoding="utf-8") as f:
        cities_cfg = json.load(f)
    with open(root / "config" / "settings.json", "r", encoding="utf-8") as f:
        settings = json.load(f)
    return cities_cfg["cities"], settings


# ---------------------------------------------------------------------------
# Single-city fetch
# ---------------------------------------------------------------------------

def fetch_city_data(
    city: dict,
    settings: dict,
    *,
    cache_dir: Optional[Path] = None,
    force_refresh: bool = False,
) -> Optional[pd.DataFrame]:
    """
    Fetch daily temperature data for one city from NASA POWER API.

    Parameters
    ----------
    city : dict
        City metadata with keys: name, latitude, longitude.
    settings : dict
        Project settings with nasa_power_api and study_period sections.
    cache_dir : Path, optional
        Directory to store cached raw JSON responses.
    force_refresh : bool
        If True, ignore cached data and re-download.

    Returns
    -------
    pd.DataFrame or None
        DataFrame with columns [date, city, latitude, longitude, T2M_MIN, T2M_MAX, T2M]
        or None if the request fails after all retries.
    """
    api_cfg = settings["nasa_power_api"]
    period = settings["study_period"]

    city_name = city["name"]
    lat = city["latitude"]
    lon = city["longitude"]

    # Cache setup
    if cache_dir is None:
        cache_dir = _get_project_root() / "data" / "raw"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"{city_name.lower().replace(' ', '_')}_raw.json"

    # Use cache if available
    if cache_file.exists() and not force_refresh:
        logger.info("Loading cached data for %s from %s", city_name, cache_file)
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                raw_json = json.load(f)
            return _parse_power_response(raw_json, city)
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning("Cache file corrupted for %s: %s. Re-downloading.", city_name, e)

    # Build API request
    start_date = period["start_date"].replace("-", "")
    end_date = period["end_date"].replace("-", "")
    params = {
        "parameters": ",".join(api_cfg["parameters"]),
        "community": api_cfg["community"],
        "longitude": lon,
        "latitude": lat,
        "start": start_date,
        "end": end_date,
        "format": api_cfg["output_format"],
    }

    url = api_cfg["base_url"]
    timeout = api_cfg["timeout_seconds"]
    max_retries = api_cfg["max_retries"]
    backoff = api_cfg["initial_backoff_seconds"]
    rate_delay = api_cfg["rate_limit_delay_seconds"]

    # Fetch with retries
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(
                "Fetching %s (attempt %d/%d) — lat=%.4f, lon=%.4f, %s to %s",
                city_name, attempt, max_retries, lat, lon, start_date, end_date,
            )
            t0 = time.time()
            resp = requests.get(url, params=params, timeout=timeout)
            elapsed = time.time() - t0
            logger.info("Response for %s: HTTP %d in %.1fs", city_name, resp.status_code, elapsed)

            if resp.status_code == 429:
                wait = backoff * (2 ** (attempt - 1))
                logger.warning("Rate-limited for %s. Waiting %.1fs before retry.", city_name, wait)
                time.sleep(wait)
                continue

            resp.raise_for_status()
            raw_json = resp.json()

            # Cache the raw response
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(raw_json, f)
            logger.info("Cached raw data for %s to %s", city_name, cache_file)

            time.sleep(rate_delay)  # Respect rate limits
            return _parse_power_response(raw_json, city)

        except requests.exceptions.Timeout:
            logger.warning("Timeout fetching %s (attempt %d/%d).", city_name, attempt, max_retries)
        except requests.exceptions.ConnectionError as e:
            logger.warning("Connection error for %s (attempt %d): %s", city_name, attempt, e)
        except requests.exceptions.HTTPError as e:
            logger.error("HTTP error for %s (attempt %d): %s", city_name, attempt, e)
        except (json.JSONDecodeError, KeyError) as e:
            logger.error("Response parse error for %s: %s", city_name, e)
            break  # Don't retry on parse errors

        if attempt < max_retries:
            wait = backoff * (2 ** (attempt - 1))
            logger.info("Retrying %s in %.1fs ...", city_name, wait)
            time.sleep(wait)

    logger.error("Failed to fetch data for %s after %d attempts.", city_name, max_retries)
    return None


def _parse_power_response(raw_json: dict, city: dict) -> pd.DataFrame:
    """Parse NASA POWER JSON response into a tidy DataFrame."""
    properties = raw_json.get("properties", {})
    parameters = properties.get("parameter", {})

    if not parameters:
        raise KeyError("No 'parameter' key found in NASA POWER response properties.")

    records = []
    # Each parameter is a dict of {YYYYMMDD: value}
    t2m_min = parameters.get("T2M_MIN", {})
    t2m_max = parameters.get("T2M_MAX", {})
    t2m = parameters.get("T2M", {})

    all_dates = sorted(set(t2m_min.keys()) | set(t2m_max.keys()) | set(t2m.keys()))

    for date_str in all_dates:
        try:
            date = pd.to_datetime(date_str, format="%Y%m%d")
        except ValueError:
            logger.warning("Skipping unparseable date: %s", date_str)
            continue

        records.append({
            "date": date,
            "city": city["name"],
            "latitude": city["latitude"],
            "longitude": city["longitude"],
            "T2M_MIN": t2m_min.get(date_str),
            "T2M_MAX": t2m_max.get(date_str),
            "T2M": t2m.get(date_str),
        })

    df = pd.DataFrame(records)
    if not df.empty:
        df = df.sort_values("date").reset_index(drop=True)
    return df


# ---------------------------------------------------------------------------
# Fetch all cities
# ---------------------------------------------------------------------------

def fetch_all_cities(
    force_refresh: bool = False,
    cities_override: Optional[list] = None,
) -> pd.DataFrame:
    """
    Fetch data for all configured cities. Restartable — uses cache.

    Returns combined DataFrame for all successfully fetched cities.
    """
    cities, settings = load_config()
    if cities_override:
        cities = cities_override

    cache_dir = _get_project_root() / "data" / "raw"
    log_dir = _get_project_root() / "outputs" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    all_dfs = []
    fetch_log = []

    for city in cities:
        t0 = time.time()
        df = fetch_city_data(city, settings, cache_dir=cache_dir, force_refresh=force_refresh)
        elapsed = time.time() - t0

        status = "success" if df is not None and not df.empty else "failed"
        n_records = len(df) if df is not None else 0

        fetch_log.append({
            "city": city["name"],
            "latitude": city["latitude"],
            "longitude": city["longitude"],
            "status": status,
            "records": n_records,
            "fetch_time_s": round(elapsed, 2),
            "timestamp": datetime.now().isoformat(),
        })

        if df is not None and not df.empty:
            all_dfs.append(df)
            logger.info("✓ %s: %d records fetched in %.1fs", city["name"], n_records, elapsed)
        else:
            logger.error("✗ %s: fetch failed", city["name"])

    # Save fetch log
    log_df = pd.DataFrame(fetch_log)
    log_file = log_dir / "fetch_log.csv"
    log_df.to_csv(log_file, index=False)
    logger.info("Fetch log saved to %s", log_file)

    if not all_dfs:
        logger.error("No data fetched for any city!")
        return pd.DataFrame()

    combined = pd.concat(all_dfs, ignore_index=True)
    logger.info("Combined dataset: %d records across %d cities",
                len(combined), combined["city"].nunique())
    return combined


# ---------------------------------------------------------------------------
# Test request
# ---------------------------------------------------------------------------

def test_api_connection() -> bool:
    """Run a small test request to verify NASA POWER API connectivity."""
    _, settings = load_config()
    api_cfg = settings["nasa_power_api"]

    test_params = {
        "parameters": "T2M",
        "community": api_cfg["community"],
        "longitude": 77.2090,
        "latitude": 28.6139,
        "start": "20250101",
        "end": "20250107",
        "format": "JSON",
    }

    try:
        logger.info("Testing NASA POWER API connection...")
        resp = requests.get(api_cfg["base_url"], params=test_params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        props = data.get("properties", {}).get("parameter", {})
        if "T2M" in props:
            n_days = len([v for v in props["T2M"].values() if v is not None])
            logger.info("✓ API test successful: %d days returned for Delhi.", n_days)
            return True
        else:
            logger.error("✗ API test: unexpected response structure.")
            return False
    except Exception as e:
        logger.error("✗ API test failed: %s", e)
        return False


# ---------------------------------------------------------------------------
# Load from existing CSV (fallback)
# ---------------------------------------------------------------------------

def load_cached_raw_data() -> Optional[pd.DataFrame]:
    """Load previously downloaded raw data from cached JSON files."""
    cities, _ = load_config()
    cache_dir = _get_project_root() / "data" / "raw"

    all_dfs = []
    for city in cities:
        cache_file = cache_dir / f"{city['name'].lower().replace(' ', '_')}_raw.json"
        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    raw_json = json.load(f)
                df = _parse_power_response(raw_json, city)
                all_dfs.append(df)
                logger.info("Loaded cached data for %s: %d records", city["name"], len(df))
            except Exception as e:
                logger.warning("Failed to load cache for %s: %s", city["name"], e)
        else:
            logger.warning("No cached data found for %s", city["name"])

    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    return None
