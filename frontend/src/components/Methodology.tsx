import { Layers, GitBranch, CheckCircle2, Sliders, LineChart, Flame, Database } from 'lucide-react';

export const Methodology = () => {
  const pipelineSteps = [
    {
      step: '01',
      title: 'NASA POWER API Acquisition',
      desc: 'Automated retrieval from NASA POWER Point API (community=AG) with exponential backoff retries, response schema verification, and disk-level raw caching.',
      icon: Database,
    },
    {
      step: '02',
      title: 'Auditing & Quality Verification',
      desc: 'Screening for missing dates, -999 fill values, chronological monotonicity, duplicate keys, and physical validity (Tmin ≤ Tmax, Tmin ≤ Tmean ≤ Tmax).',
      icon: CheckCircle2,
    },
    {
      step: '03',
      title: 'Feature Engineering',
      desc: 'Computing Diurnal Temperature Range (DTR), leap day temporal parsing, and IMD-aligned meteorological seasons with December winter-year wrapping.',
      icon: Sliders,
    },
    {
      step: '04',
      title: 'Dual Statistical Trend Testing',
      desc: 'Parametric OLS linear regression (slopes in °C/decade, R², 95% CIs) paired with non-parametric Mann–Kendall test and Sen’s median slope estimation.',
      icon: LineChart,
    },
    {
      step: '05',
      title: 'Calendar-Month Extreme Baseline',
      desc: 'Calculating city-specific calendar-month 90th percentile thresholds (P90) to monitor extreme thermal anomalies without summer-season bias.',
      icon: Flame,
    },
    {
      step: '06',
      title: 'Reproducible Output Export',
      desc: 'Generation of publication-grade figures in outputs/figures/ alongside validated JSON feeds (chart_data.json, findings.json) for the interactive frontend.',
      icon: Layers,
    },
  ];

  return (
    <section id="methodology" className="py-16 bg-[#F7F4EC] border-b border-[#DCD5C8]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="max-w-3xl mb-12">
          <div className="flex items-center gap-2 mb-2">
            <span className="section-label">Section 02 // Analytical Architecture</span>
          </div>
          <h2 className="font-serif text-3xl sm:text-4xl font-bold text-[#302F29] tracking-tight">
            Data Provenance & Scientific Methodology
          </h2>
          <p className="mt-3 text-base text-[#77746B] leading-relaxed">
            Detailed breakdown of data sources, mathematical definitions, seasonal aggregation conventions, and dual statistical validation techniques.
          </p>
        </div>

        {/* Technical Data Source Specification */}
        <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-6 mb-12 shadow-2xs">
          <div className="flex items-center justify-between mb-4 border-b border-[#DCD5C8] pb-3">
            <div className="flex items-center gap-2.5">
              <span className="w-2.5 h-2.5 rounded-full bg-[#355E48]" />
              <h3 className="font-serif text-lg font-bold text-[#302F29]">
                NASA POWER (Prediction Of Worldwide Energy Resources) Reanalysis
              </h3>
            </div>
            <span className="text-xs font-mono text-[#77746B] bg-[#EDE6D8] px-2 py-0.5 rounded">
              Resolution: 0.5° × 0.5° (~50km)
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs text-[#77746B]">
            <div>
              <span className="font-bold text-[#302F29] block mb-1">Atmospheric Assimilation Models</span>
              <p className="leading-relaxed">
                Combines Goddard Earth Observing System (GEOS) atmospheric assimilation models (MERRA-2 reanalysis through recent years and GEOS FP-IT in near real-time) with satellite-derived solar radiation measurements.
              </p>
            </div>
            <div>
              <span className="font-bold text-[#302F29] block mb-1">Retrieved Parameters (2m Above Ground)</span>
              <p className="leading-relaxed">
                <code className="text-[#355E48] font-bold">T2M_MIN</code> (Daily Minimum Temperature, °C),{' '}
                <code className="text-[#355E48] font-bold">T2M_MAX</code> (Daily Maximum Temperature, °C), and{' '}
                <code className="text-[#355E48] font-bold">T2M</code> (Daily Mean Temperature, °C).
              </p>
            </div>
            <div>
              <span className="font-bold text-[#302F29] block mb-1">Derived Diurnal Index</span>
              <p className="leading-relaxed">
                <code className="text-[#C66A4A] font-bold">DTR = T2M_MAX − T2M_MIN</code>. Reflects daily thermal amplitude. Note: T2M_MIN is not equivalent to mean nighttime temperature; it represents the singular lowest reading (typically near dawn).
              </p>
            </div>
          </div>
        </div>

        {/* Methodology Workflow Steps */}
        <div className="mb-12">
          <h3 className="font-serif text-xl font-bold text-[#302F29] mb-6 flex items-center gap-2">
            <GitBranch className="w-5 h-5 text-[#355E48]" />
            End-to-End Analytical Processing Pipeline
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {pipelineSteps.map((step) => {
              const Icon = step.icon;
              return (
                <div 
                  key={step.step}
                  className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-5 relative hover:border-[#355E48] transition-colors shadow-2xs"
                >
                  <div className="flex items-center justify-between mb-3">
                    <span className="font-mono text-xs font-bold text-[#355E48] bg-[#EDE6D8] px-2 py-0.5 rounded">
                      Step {step.step}
                    </span>
                    <Icon className="w-4 h-4 text-[#77746B]" />
                  </div>
                  <h4 className="font-serif font-bold text-sm text-[#302F29] mb-1.5">
                    {step.title}
                  </h4>
                  <p className="text-xs text-[#77746B] leading-relaxed">
                    {step.desc}
                  </p>
                </div>
              );
            })}
          </div>
        </div>

        {/* Seasonal Definitions & Statistical Equations */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Seasonal Scheme */}
          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-6 shadow-2xs">
            <h4 className="font-serif font-bold text-base text-[#302F29] mb-3">
              Meteorological Seasonal Scheme (IMD Aligned)
            </h4>
            <p className="text-xs text-[#77746B] mb-4 leading-relaxed">
              To account for India’s tropical monsoon dynamics, months are classified into four recognized seasons with December assigned to the winter of the subsequent year:
            </p>
            <div className="space-y-2 text-xs">
              <div className="flex items-center justify-between p-2 rounded bg-[#F7F4EC] border border-[#DCD5C8]/70">
                <span className="font-semibold text-[#302F29]">Winter</span>
                <span className="text-[#77746B]">December, January, February (DJF)</span>
                <span className="text-[10px] font-mono text-[#355E48]">Dec year → year + 1</span>
              </div>
              <div className="flex items-center justify-between p-2 rounded bg-[#F7F4EC] border border-[#DCD5C8]/70">
                <span className="font-semibold text-[#302F29]">Pre-monsoon / Summer</span>
                <span className="text-[#77746B]">March, April, May (MAM)</span>
                <span className="text-[10px] font-mono text-[#355E48]">Peak thermal solar heating</span>
              </div>
              <div className="flex items-center justify-between p-2 rounded bg-[#F7F4EC] border border-[#DCD5C8]/70">
                <span className="font-semibold text-[#302F29]">Monsoon</span>
                <span className="text-[#77746B]">June, July, August, September (JJAS)</span>
                <span className="text-[10px] font-mono text-[#355E48]">High humidity & cloud cover</span>
              </div>
              <div className="flex items-center justify-between p-2 rounded bg-[#F7F4EC] border border-[#DCD5C8]/70">
                <span className="font-semibold text-[#302F29]">Post-monsoon</span>
                <span className="text-[#77746B]">October, November (ON)</span>
                <span className="text-[10px] font-mono text-[#355E48]">Monsoon retreat / Coromandel rains</span>
              </div>
            </div>
          </div>

          {/* Statistical Modeling Rationale */}
          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-6 shadow-2xs">
            <h4 className="font-serif font-bold text-base text-[#302F29] mb-3">
              Dual Statistical Trend Formulation
            </h4>
            <p className="text-xs text-[#77746B] mb-4 leading-relaxed">
              Ordinary regression assumes normal i.i.d. residuals which can be susceptible to outlier years. We reinforce all findings with rank-based non-parametric testing:
            </p>
            <div className="space-y-3 text-xs">
              <div className="p-3 rounded bg-[#F7F4EC] border border-[#DCD5C8]/70">
                <span className="font-bold text-[#302F29] block mb-0.5">1. Ordinary Least Squares (OLS) Regression</span>
                <p className="text-[#77746B] leading-relaxed">
                  Calculates slope in °C/year: <code className="font-mono text-[#302F29]">Slope/Decade = (β₁ × 10)</code>. Evaluates coefficient of determination (R²), standard error, and two-tailed p-value with 95% confidence intervals.
                </p>
              </div>
              <div className="p-3 rounded bg-[#F7F4EC] border border-[#DCD5C8]/70">
                <span className="font-bold text-[#302F29] block mb-0.5">2. Mann–Kendall & Sen’s Median Slope</span>
                <p className="text-[#77746B] leading-relaxed">
                  Non-parametric test calculating Kendall's tau and Sen's median slope estimator, robust to extreme years and non-normal temperature distributions.
                </p>
              </div>
              <div className="p-3 rounded bg-[#F7F4EC] border border-[#DCD5C8]/70">
                <span className="font-bold text-[#302F29] block mb-0.5">3. Calendar-Month 90th Percentile Extremes</span>
                <p className="text-[#77746B] leading-relaxed">
                  Thresholds calculated per month per city across all 25 years (2001–2025). Avoids misidentifying standard April/May heat as an "extreme" relative to winter months.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
