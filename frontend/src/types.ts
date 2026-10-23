/* TypeScript types for ThermoTrends India frontend */

export interface CityMeta {
  name: string;
  latitude: number;
  longitude: number;
  region: string;
  state: string;
  climate_zone: string;
  elevation_m: number;
}

export interface AnnualRecord {
  city: string;
  year: number;
  T2M_MIN: number | null;
  T2M_MAX: number | null;
  T2M: number | null;
  DTR: number | null;
  valid_days: number;
}

export interface MonthlyClimatology {
  city: string;
  month: number;
  month_name: string;
  T2M_mean: number | null;
  T2M_std: number | null;
  T2M_count: number | null;
  T2M_MIN_mean: number | null;
  T2M_MAX_mean: number | null;
  DTR_mean: number | null;
}

export interface TrendResult {
  city: string;
  variable: string;
  ols_slope_per_year: number | null;
  ols_slope_per_decade: number | null;
  ols_intercept: number | null;
  ols_r_squared: number | null;
  ols_p_value: number | null;
  ols_std_err: number | null;
  ols_ci_lower: number | null;
  ols_ci_upper: number | null;
  ols_n_valid: number;
  ols_significant: boolean | null;
  mk_trend: string;
  mk_p_value: number | null;
  sens_slope: number | null;
  sens_slope_per_decade: number | null;
}

export interface DataQuality {
  city: string;
  expected_records: number;
  observed_records: number;
  unique_dates: number;
  missing_dates: number;
  duplicate_records: number;
  T2M_MIN_nulls: number;
  T2M_MAX_nulls: number;
  T2M_nulls: number;
  min_gt_max: number;
  mean_outside_bounds: number;
  total_flagged: number;
}

export interface CityStatistic {
  city: string;
  variable: string;
  valid_count: number;
  missing_count: number;
  missing_pct: number;
  mean: number | null;
  median: number | null;
  std: number | null;
  min: number | null;
  max: number | null;
  range: number | null;
  q1: number | null;
  q3: number | null;
  iqr: number | null;
  skewness: number | null;
}

export interface ExtremeFrequency {
  city: string;
  year: number;
  total_days: number;
  hot_days: number;
  warm_nights: number;
  hot_day_pct: number;
  warm_night_pct: number;
}

export interface SeasonalRecord {
  city: string;
  year: number;
  season: string;
  T2M_MIN: number | null;
  T2M_MAX: number | null;
  T2M: number | null;
  DTR: number | null;
  valid_days: number;
}

export interface FindingDetail {
  variable?: string;
  label?: string;
  mean_slope_per_decade?: number;
  cities_with_positive_trend?: number;
  cities_with_significant_trend?: number;
  total_cities?: number;
  strongest_trend_city?: string;
  strongest_trend_slope?: number;
  unit?: string;
  [key: string]: unknown;
}

export interface ResearchQuestion {
  id: string;
  question: string;
  findings: FindingDetail[];
}

export interface Findings {
  study_period: string;
  data_source: string;
  research_questions: ResearchQuestion[];
}

export interface ChartData {
  cities: CityMeta[];
  annual: AnnualRecord[];
  monthly_climatology: MonthlyClimatology[];
  trends: TrendResult[];
  data_quality: DataQuality[];
  city_statistics: CityStatistic[];
  extreme_frequencies: ExtremeFrequency[];
  seasonal: SeasonalRecord[];
}

export type TempVariable = 'T2M_MIN' | 'T2M_MAX' | 'T2M' | 'DTR';
export type Season = 'Winter' | 'Pre-monsoon' | 'Monsoon' | 'Post-monsoon';
