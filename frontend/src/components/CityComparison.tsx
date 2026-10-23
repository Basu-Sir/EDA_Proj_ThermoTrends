import { useState, useMemo } from 'react';
import type { ChartData, TempVariable } from '../types';
import { CITY_COLORS, VARIABLE_LABELS, formatTemp, formatSlope } from '../data';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';
import { Scale, Check } from 'lucide-react';

interface CityComparisonProps {
  data: ChartData;
}

export const CityComparison: React.FC<CityComparisonProps> = ({ data }) => {
  // Select 2 to 4 cities for side-by-side benchmarking
  const [selectedCities, setSelectedCities] = useState<string[]>(['Delhi', 'Mumbai', 'Chennai']);
  const [compareVariable, setCompareVariable] = useState<TempVariable>('T2M');

  const toggleCity = (cityName: string) => {
    if (selectedCities.includes(cityName)) {
      if (selectedCities.length > 2) {
        setSelectedCities(selectedCities.filter(c => c !== cityName));
      }
    } else {
      if (selectedCities.length < 4) {
        setSelectedCities([...selectedCities, cityName]);
      }
    }
  };

  // Comparative Annual Data
  const annualComparisonData = useMemo(() => {
    const years = Array.from({ length: 2025 - 2001 + 1 }, (_, i) => 2001 + i);
    return years.map(yr => {
      const row: Record<string, any> = { year: yr };
      selectedCities.forEach(city => {
        const match = data.annual.find(a => a.city === city && a.year === yr);
        if (match && match[compareVariable] != null) {
          row[city] = match[compareVariable];
        }
      });
      return row;
    });
  }, [data.annual, selectedCities, compareVariable]);

  // Comparative Monthly Climatology Data
  const monthlyComparisonData = useMemo(() => {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const valueKey = compareVariable === 'T2M_MIN' ? 'T2M_MIN_mean'
      : compareVariable === 'T2M_MAX' ? 'T2M_MAX_mean'
      : compareVariable === 'DTR' ? 'DTR_mean'
      : 'T2M_mean';

    return months.map((m, idx) => {
      const row: Record<string, any> = { month: m };
      selectedCities.forEach(city => {
        const match = data.monthly_climatology.find(mc => mc.city === city && mc.month === idx + 1);
        if (match && match[valueKey as keyof typeof match] != null) {
          row[city] = match[valueKey as keyof typeof match];
        }
      });
      return row;
    });
  }, [data.monthly_climatology, selectedCities, compareVariable]);

  return (
    <section id="compare" className="py-16 bg-[#F7F4EC] border-b border-[#DCD5C8]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="max-w-3xl mb-10">
          <div className="flex items-center gap-2 mb-2">
            <span className="section-label">Section 06 // Comparative Benchmarking</span>
          </div>
          <h2 className="font-serif text-3xl sm:text-4xl font-bold text-[#302F29] tracking-tight">
            Multi-City Comparative Matrix
          </h2>
          <p className="mt-3 text-base text-[#77746B] leading-relaxed">
            Select between 2 and 4 cities to evaluate comparative temperature distributions, climatological cycles, and decadal warming disparities.
          </p>
        </div>

        {/* City Toggle Selector Buttons */}
        <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-4 mb-8 shadow-2xs">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold uppercase tracking-wider text-[#302F29] flex items-center gap-2">
              <Scale className="w-4 h-4 text-[#355E48]" />
              Select Stations (2 to 4 Max)
            </span>
            <span className="text-xs text-[#77746B]">
              Selected: <strong className="text-[#355E48]">{selectedCities.length} / 4</strong>
            </span>
          </div>

          <div className="flex flex-wrap gap-2">
            {data.cities.map(c => {
              const isSelected = selectedCities.includes(c.name);
              return (
                <button
                  key={c.name}
                  onClick={() => toggleCity(c.name)}
                  className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-medium transition-all cursor-pointer border ${
                    isSelected
                      ? 'bg-[#355E48] text-[#FFFEFA] border-[#355E48] shadow-xs'
                      : 'bg-[#F7F4EC] text-[#302F29] border-[#DCD5C8] hover:border-[#355E48]'
                  }`}
                >
                  <span
                    className="w-2 h-2 rounded-full"
                    style={{ backgroundColor: isSelected ? '#FFFEFA' : (CITY_COLORS[c.name] || '#355E48') }}
                  />
                  <span>{c.name}</span>
                  {isSelected && <Check className="w-3 h-3" />}
                </button>
              );
            })}
          </div>
        </div>

        {/* Comparative Statistics Table */}
        <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md overflow-hidden shadow-2xs mb-10">
          <div className="px-6 py-4 border-b border-[#DCD5C8] flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <h3 className="font-serif text-base font-bold text-[#302F29]">
              Station-Wise Climatological & Trend Benchmark Matrix
            </h3>
            <div className="flex items-center gap-2">
              <span className="text-xs text-[#77746B]">Display Metric:</span>
              <select
                value={compareVariable}
                onChange={(e) => setCompareVariable(e.target.value as TempVariable)}
                className="bg-[#F7F4EC] border border-[#DCD5C8] rounded px-2.5 py-1 text-xs text-[#302F29] font-medium"
              >
                <option value="T2M">T2M (Mean)</option>
                <option value="T2M_MIN">T2M_MIN (Night Min)</option>
                <option value="T2M_MAX">T2M_MAX (Day Max)</option>
                <option value="DTR">DTR (Diurnal Range)</option>
              </select>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full text-xs divide-y divide-[#DCD5C8]">
              <thead className="bg-[#F7F4EC]">
                <tr>
                  <th className="px-4 py-3 text-left font-semibold text-[#302F29]">Station Metric</th>
                  {selectedCities.map(c => (
                    <th key={c} className="px-4 py-3 text-right font-semibold text-[#302F29]">
                      <div className="flex items-center justify-end gap-1.5">
                        <span className="w-2 h-2 rounded-full" style={{ backgroundColor: CITY_COLORS[c] || '#355E48' }} />
                        <span>{c}</span>
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-[#DCD5C8] bg-[#FFFEFA]">
                <tr>
                  <td className="px-4 py-2 font-medium text-[#77746B]">Region & State</td>
                  {selectedCities.map(c => {
                    const meta = data.cities.find(m => m.name === c);
                    return <td key={c} className="px-4 py-2 text-right font-medium text-[#302F29]">{meta?.region} ({meta?.state})</td>;
                  })}
                </tr>
                <tr>
                  <td className="px-4 py-2 font-medium text-[#77746B]">Elevation</td>
                  {selectedCities.map(c => {
                    const meta = data.cities.find(m => m.name === c);
                    return <td key={c} className="px-4 py-2 text-right font-mono text-[#77746B]">{meta?.elevation_m} m asl</td>;
                  })}
                </tr>
                <tr>
                  <td className="px-4 py-2 font-medium text-[#77746B]">Climate Zone</td>
                  {selectedCities.map(c => {
                    const meta = data.cities.find(m => m.name === c);
                    return <td key={c} className="px-4 py-2 text-right font-medium text-[#355E48]">{meta?.climate_zone}</td>;
                  })}
                </tr>
                <tr>
                  <td className="px-4 py-2 font-medium text-[#77746B]">25-Year Mean ({compareVariable})</td>
                  {selectedCities.map(c => {
                    const stat = data.city_statistics.find(s => s.city === c && s.variable === compareVariable);
                    return <td key={c} className="px-4 py-2 text-right font-mono font-bold text-[#302F29]">{formatTemp(stat?.mean)}</td>;
                  })}
                </tr>
                <tr>
                  <td className="px-4 py-2 font-medium text-[#77746B]">Standard Deviation (Variability)</td>
                  {selectedCities.map(c => {
                    const stat = data.city_statistics.find(s => s.city === c && s.variable === compareVariable);
                    return <td key={c} className="px-4 py-2 text-right font-mono text-[#77746B]">±{stat?.std}°C</td>;
                  })}
                </tr>
                <tr>
                  <td className="px-4 py-2 font-medium text-[#77746B]">Historical Min / Max</td>
                  {selectedCities.map(c => {
                    const stat = data.city_statistics.find(s => s.city === c && s.variable === compareVariable);
                    return <td key={c} className="px-4 py-2 text-right font-mono text-[#77746B]">{stat?.min}°C / {stat?.max}°C</td>;
                  })}
                </tr>
                <tr>
                  <td className="px-4 py-2 font-medium text-[#77746B]">OLS Decadal Rate</td>
                  {selectedCities.map(c => {
                    const trend = data.trends.find(t => t.city === c && t.variable === compareVariable);
                    return (
                      <td key={c} className="px-4 py-2 text-right font-mono font-bold text-[#355E48]">
                        {formatSlope(trend?.ols_slope_per_decade)}
                      </td>
                    );
                  })}
                </tr>
                <tr>
                  <td className="px-4 py-2 font-medium text-[#77746B]">Mann-Kendall Trend</td>
                  {selectedCities.map(c => {
                    const trend = data.trends.find(t => t.city === c && t.variable === compareVariable);
                    return (
                      <td key={c} className="px-4 py-2 text-right font-mono text-[#77746B] capitalize">
                        {trend?.mk_trend.replace('_', ' ')}
                      </td>
                    );
                  })}
                </tr>
                <tr>
                  <td className="px-4 py-2 font-medium text-[#77746B]">Statistical Significance</td>
                  {selectedCities.map(c => {
                    const trend = data.trends.find(t => t.city === c && t.variable === compareVariable);
                    return (
                      <td key={c} className="px-4 py-2 text-right">
                        {trend?.ols_significant ? (
                          <span className="text-[10px] bg-[#355E48]/10 text-[#355E48] font-bold px-2 py-0.5 rounded">
                            p &lt; 0.05
                          </span>
                        ) : (
                          <span className="text-[10px] text-[#77746B]">Not Sig</span>
                        )}
                      </td>
                    );
                  })}
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* Synchronized Side-by-Side Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Chart 1: Annual Trajectories */}
          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-5 shadow-2xs">
            <h4 className="font-serif font-bold text-sm text-[#302F29] mb-1">
              Annual Trajectories — {VARIABLE_LABELS[compareVariable]} (2001–2025)
            </h4>
            <p className="text-[11px] text-[#77746B] mb-3">Comparing year-over-year annual means</p>
            <div className="h-[280px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={annualComparisonData} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="year" tickLine={false} />
                  <YAxis unit="°C" domain={['auto', 'auto']} tickLine={false} />
                  <Tooltip formatter={(val: any, name: any) => [formatTemp(Number(val)), name]} />
                  <Legend />
                  {selectedCities.map(c => (
                    <Line
                      key={c}
                      type="monotone"
                      dataKey={c}
                      stroke={CITY_COLORS[c] || '#355E48'}
                      strokeWidth={2}
                      dot={{ r: 2 }}
                    />
                  ))}
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Chart 2: Climatological Monthly Curves */}
          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-5 shadow-2xs">
            <h4 className="font-serif font-bold text-sm text-[#302F29] mb-1">
              Seasonal Annual Cycle — {VARIABLE_LABELS[compareVariable]}
            </h4>
            <p className="text-[11px] text-[#77746B] mb-3">25-year average monthly climatology curves</p>
            <div className="h-[280px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={monthlyComparisonData} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="month" tickLine={false} />
                  <YAxis unit="°C" domain={['auto', 'auto']} tickLine={false} />
                  <Tooltip formatter={(val: any, name: any) => [formatTemp(Number(val)), name]} />
                  <Legend />
                  {selectedCities.map(c => (
                    <Line
                      key={c}
                      type="monotone"
                      dataKey={c}
                      stroke={CITY_COLORS[c] || '#355E48'}
                      strokeWidth={2}
                      dot={{ r: 2 }}
                    />
                  ))}
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
