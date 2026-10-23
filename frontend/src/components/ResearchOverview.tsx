import { Target, BookOpen, AlertCircle } from 'lucide-react';

export const ResearchOverview = () => {
  const researchQuestions = [
    {
      id: 'RQ1',
      title: 'Decadal Trend Trajectories',
      question: 'How have daily minimum (T2M_MIN), maximum (T2M_MAX), and mean (T2M) temperatures changed over the 2001–2025 period across climatically distinct Indian cities?',
      focus: 'Quantifies OLS decadal rates (°C/decade) and tests monotonicity using the non-parametric Mann–Kendall test with Sen’s slope estimator.',
      badge: 'Trend Estimation'
    },
    {
      id: 'RQ2',
      title: 'Warming Asymmetry (Tmin vs. Tmax)',
      question: 'Do nighttime minimum temperatures and daytime maximum temperatures exhibit statistically differing rates of warming or cooling across geographic regions?',
      focus: 'Evaluates whether nighttime minimums are warming faster than daytime maximums, a recognized hallmark of anthropogenic greenhouse forcing and urban thermal retention.',
      badge: 'Asymmetric Warming'
    },
    {
      id: 'RQ3',
      title: 'Climatological & Seasonal Variability',
      question: 'How do baseline temperature distributions, seasonal amplitudes, and climatological cycles vary across peninsular, continental, and montane Indian cities?',
      focus: 'Examines seasonal transitions across Winter (DJF), Pre-monsoon (MAM), Monsoon (JJAS), and Post-monsoon (ON) regimes.',
      badge: 'Distribution Analysis'
    },
    {
      id: 'RQ4',
      title: 'Diurnal Temperature Range (DTR) Evolution',
      question: 'Is the Daily Temperature Range (DTR = T2M_MAX − T2M_MIN) expanding or contracting, and does this pattern hold uniformly across the subcontinent?',
      focus: 'Calculates city-level DTR trends in °C/decade to understand thermal amplitude dampening and atmospheric moisture/cloud-cover interactions.',
      badge: 'DTR Contraction'
    },
    {
      id: 'RQ5',
      title: 'Percentile-Based Extreme Exceedances',
      question: 'How frequently do unusually hot days (Tmax > 90th percentile) and warm nights (Tmin > 90th percentile) occur, and are their annual frequencies accelerating?',
      focus: 'Applies city-specific calendar-month 90th percentile thresholds across 2001–2025 to monitor extreme thermal stress without assuming arbitrary heatwave definitions.',
      badge: 'Extreme Events'
    },
    {
      id: 'RQ6',
      title: 'Observational Integrity & Methodological Boundaries',
      question: 'How do reanalysis grid resolution, missing observations, outlier screening, and daily minimum vs. true night temperature distinctions constrain analytical inferences?',
      focus: 'Enforces rigorous data auditing and establishes clear scientific boundaries: purely descriptive EDA without claiming direct causality or building unverified models.',
      badge: 'Scientific Boundaries'
    }
  ];

  return (
    <section id="overview" className="py-16 bg-[#EDE6D8]/50 border-b border-[#DCD5C8]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="max-w-3xl mb-12">
          <div className="flex items-center gap-2 mb-2">
            <span className="section-label">Section 01 // Context & Scope</span>
          </div>
          <h2 className="font-serif text-3xl sm:text-4xl font-bold text-[#302F29] tracking-tight">
            Research Context & Problem Formulation
          </h2>
          <p className="mt-3 text-base text-[#77746B] leading-relaxed">
            Framing the motivation, scientific objectives, and formal research inquiries guiding our exploratory investigation of Indian thermal dynamics from 2001 to 2025.
          </p>
        </div>

        {/* Narrative Grid: Motivation, Problem, Scope */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-6 shadow-2xs">
            <div className="w-8 h-8 rounded-md bg-[#EDE6D8] text-[#355E48] flex items-center justify-center mb-4">
              <BookOpen className="w-4 h-4" />
            </div>
            <h3 className="font-serif text-lg font-bold text-[#302F29] mb-2">Background & Motivation</h3>
            <p className="text-xs text-[#77746B] leading-relaxed">
              The Indian subcontinent encompasses extraordinarily diverse climatic zones—from the alpine valleys of Kashmir to the arid plains of Rajasthan, the humid tropical coastlines of Malabar and Coromandel, and the dense alluvial plains of the Ganges. As rapid urbanization alters surface energy budgets, understanding historical thermal shifts at high temporal granularity is vital for empirical climatology.
            </p>
          </div>

          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-6 shadow-2xs">
            <div className="w-8 h-8 rounded-md bg-[#EDE6D8] text-[#C66A4A] flex items-center justify-center mb-4">
              <AlertCircle className="w-4 h-4" />
            </div>
            <h3 className="font-serif text-lg font-bold text-[#302F29] mb-2">The Empirical Problem</h3>
            <p className="text-xs text-[#77746B] leading-relaxed">
              Observational temperature records in tropical developing regions frequently suffer from station relocations, instrumentation changes, missing records, and microclimatic urbanization biases. Moreover, aggregate national means often mask striking disparities between daytime solar heating and nighttime radiative cooling, necessitating systematic comparative auditing.
            </p>
          </div>

          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-6 shadow-2xs">
            <div className="w-8 h-8 rounded-md bg-[#EDE6D8] text-[#355E48] flex items-center justify-center mb-4">
              <Target className="w-4 h-4" />
            </div>
            <h3 className="font-serif text-lg font-bold text-[#302F29] mb-2">Methodological Scope</h3>
            <p className="text-xs text-[#77746B] leading-relaxed">
              We employ NASA’s continuous, satellite-calibrated POWER reanalysis dataset at 0.5° × 0.5° resolution across 12 strategic cities over a full 25-year study period (2001–2025). This exploratory study avoids unwarranted causal claims or predictive modeling, focusing instead on rigorous descriptive statistics, verified trend testing, and data traceability.
            </p>
          </div>
        </div>

        {/* The Formal Research Questions */}
        <div>
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="font-serif text-2xl font-bold text-[#302F29]">
                Core Research Questions Under Investigation
              </h3>
              <p className="text-xs text-[#77746B] mt-1">
                Each question is systematically answered through empirical calculations in subsequent analytical sections.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {researchQuestions.map((rq) => (
              <div 
                key={rq.id}
                className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-5 flex flex-col justify-between hover:border-[#355E48] transition-colors shadow-2xs"
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="font-mono text-xs font-bold text-[#355E48] bg-[#EDE6D8] px-2 py-0.5 rounded border border-[#DCD5C8]">
                      {rq.id}
                    </span>
                    <span className="text-[10px] uppercase tracking-wider font-semibold text-[#77746B]">
                      {rq.badge}
                    </span>
                  </div>
                  <h4 className="font-serif font-bold text-base text-[#302F29] mb-2 leading-snug">
                    {rq.title}
                  </h4>
                  <p className="text-xs text-[#302F29]/90 italic mb-4 leading-relaxed bg-[#F7F4EC] p-2.5 rounded border border-[#DCD5C8]/70">
                    "{rq.question}"
                  </p>
                </div>
                <div className="pt-3 border-t border-[#DCD5C8]/60 text-[11px] text-[#77746B]">
                  <span className="font-semibold text-[#302F29]">Analytical Strategy: </span>
                  {rq.focus}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};
