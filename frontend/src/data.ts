/* Data loader — loads JSON outputs from the Python pipeline */

import type { ChartData, Findings } from './types';

const DATA_BASE = import.meta.env.BASE_URL + 'data/';

async function fetchJson<T>(path: string): Promise<T> {
  const resp = await fetch(DATA_BASE + path);
  if (!resp.ok) {
    throw new Error(`Failed to load ${path}: ${resp.status} ${resp.statusText}`);
  }
  return resp.json() as Promise<T>;
}

export async function loadChartData(): Promise<ChartData> {
  return fetchJson<ChartData>('chart_data.json');
}

export async function loadFindings(): Promise<Findings> {
  return fetchJson<Findings>('findings.json');
}

/* Color palette consistent with the editorial theme */
export const CITY_COLORS: Record<string, string> = {
  'Delhi': '#355E48',
  'Jaipur': '#C66A4A',
  'Lucknow': '#9CAF88',
  'Srinagar': '#6B8E8A',
  'Mumbai': '#D4A574',
  'Ahmedabad': '#7B6B5D',
  'Chennai': '#A0522D',
  'Bengaluru': '#708090',
  'Hyderabad': '#BDB76B',
  'Kochi': '#8FBC8F',
  'Kolkata': '#CD853F',
  'Guwahati': '#5F9EA0',
};

export const VARIABLE_LABELS: Record<string, string> = {
  'T2M_MIN': 'Minimum Temperature',
  'T2M_MAX': 'Maximum Temperature',
  'T2M': 'Mean Temperature',
  'DTR': 'Daily Temperature Range',
};

export const SEASON_ORDER = ['Winter', 'Pre-monsoon', 'Monsoon', 'Post-monsoon'];

export const MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

export function formatTemp(val: number | null | undefined): string {
  if (val == null || isNaN(val)) return '—';
  return val.toFixed(2) + ' °C';
}

export function formatSlope(val: number | null | undefined): string {
  if (val == null || isNaN(val)) return '—';
  return (val >= 0 ? '+' : '') + val.toFixed(4) + ' °C/decade';
}

export function formatPct(val: number | null | undefined): string {
  if (val == null || isNaN(val)) return '—';
  return val.toFixed(1) + '%';
}
