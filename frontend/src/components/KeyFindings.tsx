import type { Findings } from '../types';
import { formatSlope, formatTemp } from '../data';

interface KeyFindingsProps {
  findings: Findings;
}

export const KeyFindings = ({ findings }: KeyFindingsProps) => {
  // Extract RQ findings
  const rq1 = findings.research_questions.find(q => q.id === 'rq1');
  const rq3 = findings.research_questions.find(q => q.id === 'rq3');
  const rq4 = findings.research_questions.find(q => q.id === 'rq4');
  const rq5 = findings.research_questions.find(q => q.id === 'rq5');
  const rq6 = findings.research_questions.find(q => q.id === 'rq6');

  const rq1Min = rq1?.findings.find(f => f.variable === 'T2M_MIN');
  const rq1Max = rq1?.findings.find(f => f.variable === 'T2M_MAX');

  const rq3Data = rq3?.findings[0] as any;
  const rq4Data = rq4?.findings[0] as any;
  const rq5Data = rq5?.findings[0] as any;
  const rq6Data = rq6?.findings[0] as any;

  return (
    <section id="findings" className="py-16 bg-[#EDE6D8]/50 border-b border-[#DCD5C8]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="max-w-3xl mb-12">
          <div className="flex items-center gap-2 mb-2">
            <span className="section-label">Section 05 // Empirical Evidence</span>
          </div>
          <h2 className="font-serif text-3xl sm:text-4xl font-bold text-[#302F29] tracking-tight">
            Key Empirical Findings & Statistical Synthesis
          </h2>
          <p className="mt-3 text-base text-[#77746B] leading-relaxed">
            Data-driven answers directly computed from the 25-year daily temperature record across all 12 Indian cities.
          </p>
        </div>

        {/* 6 Finding Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Finding 1: Temperature Trends (RQ1) */}
          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-6 shadow-2xs flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="font-mono text-xs font-bold text-[#355E48] bg-[#EDE6D8] px-2 py-0.5 rounded">
                  RQ1 Findings
                </span>
                <span className="text-[10px] uppercase font-bold text-[#77746B]">Trend Rates</span>
              </div>
              <h3 className="font-serif font-bold text-lg text-[#302F29] mb-2">
                Decadal Warming Trajectories
              </h3>
              <p className="text-xs text-[#77746B] leading-relaxed mb-4">
                Nighttime minimums exhibit nationwide positive warming, whereas daytime maximums exhibit localized stabilization or cooling across several northern stations.
              </p>

              <div className="space-y-2.5 text-xs mb-4">
                <div className="p-2.5 rounded bg-[#F7F4EC] border border-[#DCD5C8]/70 flex items-center justify-between">
                  <div>
                    <span className="font-semibold text-[#302F29] block">Tmin (Night Minimum)</span>
                    <span className="text-[10px] text-[#77746B]">{rq1Min?.cities_with_positive_trend} of 12 cities warming</span>
                  </div>
                  <span className="font-mono font-bold text-[#355E48] text-sm">
                    {formatSlope(rq1Min?.mean_slope_per_decade)}
                  </span>
                </div>

                <div className="p-2.5 rounded bg-[#F7F4EC] border border-[#DCD5C8]/70 flex items-center justify-between">
                  <div>
                    <span className="font-semibold text-[#302F29] block">Tmax (Day Maximum)</span>
                    <span className="text-[10px] text-[#77746B]">{rq1Max?.cities_with_positive_trend} of 12 cities warming</span>
                  </div>
                  <span className="font-mono font-bold text-[#C66A4A] text-sm">
                    {formatSlope(rq1Max?.mean_slope_per_decade)}
                  </span>
                </div>

                <div className="p-2.5 rounded bg-[#F7F4EC] border border-[#DCD5C8]/70 flex items-center justify-between">
                  <div>
                    <span className="font-semibold text-[#302F29] block">Strongest Tmin Warming</span>
                    <span className="text-[10px] text-[#77746B]">{rq1Min?.strongest_trend_city}</span>
                  </div>
                  <span className="font-mono font-bold text-[#355E48]">
                    {formatSlope(rq1Min?.strongest_trend_slope)}
                  </span>
                </div>
              </div>
            </div>
            <div className="pt-3 border-t border-[#DCD5C8] text-[11px] text-[#77746B]">
              <span className="font-semibold text-[#302F29]">Takeaway: </span>
              Minimum temperatures exhibit clear, persistent warming (+0.12°C/dec avg), confirming nocturnal heat accumulation.
            </div>
          </div>

          {/* Finding 2: Asymmetric Warming (RQ2) */}
          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-6 shadow-2xs flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="font-mono text-xs font-bold text-[#355E48] bg-[#EDE6D8] px-2 py-0.5 rounded">
                  RQ2 Findings
                </span>
                <span className="text-[10px] uppercase font-bold text-[#355E48] bg-[#355E48]/10 px-2 py-0.5 rounded">
                  100% Consistency
                </span>
              </div>
              <h3 className="font-serif font-bold text-lg text-[#302F29] mb-2">
                Universal Nocturnal Asymmetry
              </h3>
              <p className="text-xs text-[#77746B] leading-relaxed mb-4">
                In <strong className="text-[#355E48]">12 out of 12 cities (100%)</strong>, minimum temperatures warmed faster (or cooled slower) than maximum temperatures.
              </p>

              <div className="p-3 rounded bg-[#F7F4EC] border border-[#DCD5C8]/70 mb-4">
                <span className="text-[10px] uppercase font-bold text-[#77746B] block mb-1">
                  Average Warming Asymmetry (Tmin Slope − Tmax Slope)
                </span>
                <span className="font-serif text-2xl font-bold text-[#355E48] block tabular-nums">
                  +0.374 °C / decade
                </span>
                <span className="text-[11px] text-[#77746B]">
                  Universal across inland, coastal, and montane regions
                </span>
              </div>

              <div className="space-y-1.5 text-xs">
                <div className="flex items-center justify-between py-1 border-b border-[#DCD5C8]/50">
                  <span className="text-[#77746B]">Highest Asymmetry:</span>
                  <span className="font-bold text-[#302F29]">Srinagar (+0.958 °C/dec)</span>
                </div>
                <div className="flex items-center justify-between py-1 border-b border-[#DCD5C8]/50">
                  <span className="text-[#77746B]">Second Highest:</span>
                  <span className="font-bold text-[#302F29]">Jaipur (+0.645 °C/dec)</span>
                </div>
                <div className="flex items-center justify-between py-1">
                  <span className="text-[#77746B]">Third Highest:</span>
                  <span className="font-bold text-[#302F29]">Ahmedabad (+0.633 °C/dec)</span>
                </div>
              </div>
            </div>
            <div className="pt-3 border-t border-[#DCD5C8] text-[11px] text-[#77746B]">
              <span className="font-semibold text-[#302F29]">Takeaway: </span>
              Asymmetric warming is robustly verified; nights are persistently losing less heat across all monitored Indian cities.
            </div>
          </div>

          {/* Finding 3: Climatological Extremes & Distributions (RQ3) */}
          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-6 shadow-2xs flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="font-mono text-xs font-bold text-[#355E48] bg-[#EDE6D8] px-2 py-0.5 rounded">
                  RQ3 Findings
                </span>
                <span className="text-[10px] uppercase font-bold text-[#77746B]">Climatology</span>
              </div>
              <h3 className="font-serif font-bold text-lg text-[#302F29] mb-2">
                Subcontinental Thermal Spectrum
              </h3>
              <p className="text-xs text-[#77746B] leading-relaxed mb-4">
                Long-term 25-year temperature distributions reveal broad continental divergence across peninsular, maritime, and Himalayan zones.
              </p>

              <div className="space-y-2.5 text-xs mb-4">
                <div className="p-2.5 rounded bg-[#F7F4EC] border border-[#DCD5C8]/70 flex items-center justify-between">
                  <div>
                    <span className="font-semibold text-[#302F29] block">Warmest Long-Term Mean</span>
                    <span className="text-[10px] text-[#77746B]">{rq3Data?.warmest_city}</span>
                  </div>
                  <span className="font-mono font-bold text-[#C66A4A] text-sm">
                    {formatTemp(rq3Data?.warmest_mean)}
                  </span>
                </div>

                <div className="p-2.5 rounded bg-[#F7F4EC] border border-[#DCD5C8]/70 flex items-center justify-between">
                  <div>
                    <span className="font-semibold text-[#302F29] block">Coolest Long-Term Mean</span>
                    <span className="text-[10px] text-[#77746B]">{rq3Data?.coolest_city}</span>
                  </div>
                  <span className="font-mono font-bold text-[#355E48] text-sm">
                    {formatTemp(rq3Data?.coolest_mean)}
                  </span>
                </div>

                <div className="p-2.5 rounded bg-[#F7F4EC] border border-[#DCD5C8]/70 flex items-center justify-between">
                  <div>
                    <span className="font-semibold text-[#302F29] block">Highest Thermal Variability</span>
                    <span className="text-[10px] text-[#77746B]">{rq3Data?.most_variable_city} (Standard Dev)</span>
                  </div>
                  <span className="font-mono font-bold text-[#302F29]">
                    ±{rq3Data?.most_variable_std}°C
                  </span>
                </div>
              </div>
            </div>
            <div className="pt-3 border-t border-[#DCD5C8] text-[11px] text-[#77746B]">
              <span className="font-semibold text-[#302F29]">Takeaway: </span>
              A 18.75°C spread separates Chennai from Srinagar, with maritime cities showing dampened standard deviations (&lt;3.5°C).
            </div>
          </div>

          {/* Finding 4: DTR Contraction (RQ4) */}
          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-6 shadow-2xs flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="font-mono text-xs font-bold text-[#355E48] bg-[#EDE6D8] px-2 py-0.5 rounded">
                  RQ4 Findings
                </span>
                <span className="text-[10px] uppercase font-bold text-[#C66A4A] bg-[#C66A4A]/10 px-2 py-0.5 rounded">
                  DTR Contraction
                </span>
              </div>
              <h3 className="font-serif font-bold text-lg text-[#302F29] mb-2">
                Subcontinental DTR Narrowing
              </h3>
              <p className="text-xs text-[#77746B] leading-relaxed mb-4">
                The Daily Temperature Range (DTR) is decreasing at an average rate of <strong className="text-[#C66A4A]">{formatSlope(rq4Data?.mean_dtr_slope_per_decade)}</strong>.
              </p>

              <div className="p-3 rounded bg-[#F7F4EC] border border-[#DCD5C8]/70 mb-4">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-[#302F29]">Decreasing DTR Cities:</span>
                  <span className="font-mono font-bold text-[#C66A4A] text-sm">12 / 12 (100%)</span>
                </div>
                <div className="flex items-center justify-between mt-1">
                  <span className="text-xs font-semibold text-[#302F29]">Increasing DTR Cities:</span>
                  <span className="font-mono font-bold text-[#77746B] text-sm">0 / 12 (0%)</span>
                </div>
              </div>

              <div className="text-xs text-[#77746B] leading-relaxed bg-[#EDE6D8]/50 p-2.5 rounded border border-[#DCD5C8]">
                <strong>Scientific Note: </strong>
                {rq4Data?.note || 'Daily minimum is not equivalent to mean night temperature; it represents lowest pre-dawn reading.'}
              </div>
            </div>
            <div className="pt-3 border-t border-[#DCD5C8] text-[11px] text-[#77746B]">
              <span className="font-semibold text-[#302F29]">Takeaway: </span>
              No city in the sample demonstrated an expanding DTR; diurnal thermal dampening is subcontinental in scale.
            </div>
          </div>

          {/* Finding 5: Extreme Hot Days & Warm Nights (RQ5) */}
          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-6 shadow-2xs flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="font-mono text-xs font-bold text-[#355E48] bg-[#EDE6D8] px-2 py-0.5 rounded">
                  RQ5 Findings
                </span>
                <span className="text-[10px] uppercase font-bold text-[#77746B]">Percentile Extremes</span>
              </div>
              <h3 className="font-serif font-bold text-lg text-[#302F29] mb-2">
                Calendar-Month Extreme Exceedances
              </h3>
              <p className="text-xs text-[#77746B] leading-relaxed mb-4">
                Extreme thermal stress is evaluated using city-specific calendar-month 90th percentile thresholds across 2001–2025.
              </p>

              <div className="space-y-2.5 text-xs mb-4">
                <div className="p-2.5 rounded bg-[#F7F4EC] border border-[#DCD5C8]/70 flex items-center justify-between">
                  <div>
                    <span className="font-semibold text-[#302F29] block">City with Most Hot Days</span>
                    <span className="text-[10px] text-[#77746B]">{rq5Data?.city_with_most_hot_days}</span>
                  </div>
                  <span className="font-mono font-bold text-[#C66A4A]">
                    {rq5Data?.avg_hot_days_per_year} days/yr
                  </span>
                </div>

                <div className="p-2.5 rounded bg-[#F7F4EC] border border-[#DCD5C8]/70 flex items-center justify-between">
                  <div>
                    <span className="font-semibold text-[#302F29] block">City with Most Warm Nights</span>
                    <span className="text-[10px] text-[#77746B]">{rq5Data?.city_with_most_warm_nights}</span>
                  </div>
                  <span className="font-mono font-bold text-[#355E48]">
                    {rq5Data?.avg_warm_nights_per_year} nights/yr
                  </span>
                </div>

                <div className="text-[11px] text-[#77746B] leading-relaxed pt-1">
                  Threshold Method: {rq5Data?.threshold_method}
                </div>
              </div>
            </div>
            <div className="pt-3 border-t border-[#DCD5C8] text-[11px] text-[#77746B]">
              <span className="font-semibold text-[#302F29]">Takeaway: </span>
              Inland Gangetic plains (Lucknow, Delhi) experience the highest absolute frequency of month-relative extreme exceedance days.
            </div>
          </div>

          {/* Finding 6: Data Quality & Methodological Integrity (RQ6) */}
          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-6 shadow-2xs flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="font-mono text-xs font-bold text-[#355E48] bg-[#EDE6D8] px-2 py-0.5 rounded">
                  RQ6 Findings
                </span>
                <span className="text-[10px] uppercase font-bold text-[#355E48] bg-[#355E48]/10 px-2 py-0.5 rounded">
                  Audited Clean
                </span>
              </div>
              <h3 className="font-serif font-bold text-lg text-[#302F29] mb-2">
                Data Completeness & Boundaries
              </h3>
              <p className="text-xs text-[#77746B] leading-relaxed mb-4">
                NASA POWER reanalysis provided a 100% complete dataset across 109,572 station-days with zero missing values and zero physical inconsistencies.
              </p>

              <div className="space-y-2 text-xs mb-4">
                <div className="flex items-center justify-between py-1 border-b border-[#DCD5C8]/50">
                  <span className="text-[#77746B]">Total Daily Records:</span>
                  <span className="font-mono font-bold text-[#302F29]">{rq6Data?.total_observed_records?.toLocaleString()}</span>
                </div>
                <div className="flex items-center justify-between py-1 border-b border-[#DCD5C8]/50">
                  <span className="text-[#77746B]">Overall Completeness:</span>
                  <span className="font-mono font-bold text-[#355E48]">{rq6Data?.overall_completeness_pct}%</span>
                </div>
                <div className="flex items-center justify-between py-1">
                  <span className="text-[#77746B]">Cities Validated:</span>
                  <span className="font-mono font-bold text-[#302F29]">{rq6Data?.cities_analyzed}</span>
                </div>
              </div>

              <div className="text-[11px] text-[#77746B] bg-[#F7F4EC] p-2.5 rounded border border-[#DCD5C8]">
                <strong>Scientific Boundary: </strong>
                Because this is an exploratory study, findings describe empirical associations rather than physical causal attribution.
              </div>
            </div>
            <div className="pt-3 border-t border-[#DCD5C8] text-[11px] text-[#77746B]">
              <span className="font-semibold text-[#302F29]">Takeaway: </span>
              High data integrity without synthetic interpolation enables transparent, reproducible comparative climatology.
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
