import { CheckCircle, ShieldAlert, Lightbulb } from 'lucide-react';

export const ConclusionLimitations = () => {
  return (
    <section id="limitations" className="py-16 bg-[#EDE6D8]/40 border-b border-[#DCD5C8]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="max-w-3xl mb-12">
          <div className="flex items-center gap-2 mb-2">
            <span className="section-label">Section 07 // Scientific Synthesis</span>
          </div>
          <h2 className="font-serif text-3xl sm:text-4xl font-bold text-[#302F29] tracking-tight">
            Scientific Conclusions & Methodological Limitations
          </h2>
          <p className="mt-3 text-base text-[#77746B] leading-relaxed">
            Distilling the empirical takeaways while explicitly documenting data constraints, spatial boundaries, and non-causal boundaries of exploratory analysis.
          </p>
        </div>

        {/* 3 Core Scientific Takeaways */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-6 shadow-2xs">
            <div className="w-8 h-8 rounded-md bg-[#EDE6D8] text-[#355E48] flex items-center justify-center mb-4">
              <CheckCircle className="w-4 h-4" />
            </div>
            <h3 className="font-serif text-base font-bold text-[#302F29] mb-2">
              1. Persistent Nocturnal Warming
            </h3>
            <p className="text-xs text-[#77746B] leading-relaxed">
              Minimum temperatures (T2M_MIN) exhibited widespread positive warming across 9 of 12 stations, averaging +0.122 °C/decade. Nocturnal temperatures warmed faster than daytime highs across 100% of the sample, demonstrating persistent heat retention after sunset.
            </p>
          </div>

          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-6 shadow-2xs">
            <div className="w-8 h-8 rounded-md bg-[#EDE6D8] text-[#C66A4A] flex items-center justify-center mb-4">
              <CheckCircle className="w-4 h-4" />
            </div>
            <h3 className="font-serif text-base font-bold text-[#302F29] mb-2">
              2. Subcontinental DTR Contraction
            </h3>
            <p className="text-xs text-[#77746B] leading-relaxed">
              Daily Temperature Range (DTR) contracted in all 12 cities without exception, averaging -0.374 °C/decade. This narrowing of diurnal thermal amplitude suggests widespread atmospheric damping, increased greenhouse back-radiation, and boundary-layer moisture shifts.
            </p>
          </div>

          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-6 shadow-2xs">
            <div className="w-8 h-8 rounded-md bg-[#EDE6D8] text-[#355E48] flex items-center justify-center mb-4">
              <CheckCircle className="w-4 h-4" />
            </div>
            <h3 className="font-serif text-base font-bold text-[#302F29] mb-2">
              3. Regional Climatological Diversity
            </h3>
            <p className="text-xs text-[#77746B] leading-relaxed">
              Subcontinental geography creates pronounced thermal regimes: continental stations (Srinagar, Delhi, Jaipur) exhibit vast seasonal swings and rapid DTR shifts, whereas maritime stations (Mumbai, Kochi, Chennai) display buffered, humid thermal trajectories.
            </p>
          </div>
        </div>

        {/* The 5 Explicit Methodological Limitations */}
        <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-6 shadow-2xs mb-10">
          <div className="flex items-center gap-2 mb-4 border-b border-[#DCD5C8] pb-3">
            <ShieldAlert className="w-5 h-5 text-[#C66A4A]" />
            <h3 className="font-serif text-lg font-bold text-[#302F29]">
              Methodological Boundaries & Analytical Limitations
            </h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs text-[#77746B]">
            <div className="space-y-3">
              <div>
                <strong className="text-[#302F29] block mb-1">
                  1. Gridded Spatial Resolution (0.5° × 0.5° ~ 2,500 km²)
                </strong>
                <p className="leading-relaxed">
                  NASA POWER represents area-averaged assimilation cells. It naturally attenuates high-intensity microclimatic Urban Heat Island (UHI) hotspots found at high-density commercial junctions, asphalt corridors, and industrial belts. Grid cell coordinates should not be conflated with localized rooftop thermometers.
                </p>
              </div>

              <div>
                <strong className="text-[#302F29] block mb-1">
                  2. Reanalysis Model Reliance vs. Surface Ground Telemetry
                </strong>
                <p className="leading-relaxed">
                  While NASA POWER provides complete continuity without missing observations, it is generated via GEOS atmospheric assimilation models and satellite radiances rather than direct in-situ mercury thermometer logs. Minor model boundary biases can exist, particularly over complex mountainous terrain like Kashmir.
                </p>
              </div>

              <div>
                <strong className="text-[#302F29] block mb-1">
                  3. 25-Year Climatological Span vs. 30-Year Normal Baselines
                </strong>
                <p className="leading-relaxed">
                  The World Meteorological Organization (WMO) conventionally benchmarks climate normals over 30-year blocks (e.g., 1991–2020). Our 25-year study (2001–2025) captures the 21st-century trajectory with great temporal precision, but decadal modes (El Niño–Southern Oscillation, Indian Ocean Dipole) can influence short-term slopes.
                </p>
              </div>
            </div>

            <div className="space-y-3">
              <div>
                <strong className="text-[#302F29] block mb-1">
                  4. Minimum Temperature vs. Nighttime Integrated Thermal Exposure
                </strong>
                <p className="leading-relaxed">
                  Daily minimum temperature (T2M_MIN) typically occurs during a brief pre-dawn window (~05:00 IST). It does not represent integrated nighttime thermal discomfort or nocturnal human physiological heat exposure during early sleeping hours (22:00–02:00 IST).
                </p>
              </div>

              <div>
                <strong className="text-[#302F29] block mb-1">
                  5. Non-Causal Nature of Exploratory Data Analysis (EDA)
                </strong>
                <p className="leading-relaxed">
                  This investigation is strictly descriptive and exploratory. In adherence to statistical rigor, we report observed trends, correlations, and distributions without asserting causal attribution to specific greenhouse gas concentrations, aerosol optical depths, or land-use land-cover transitions.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Future Research Avenues */}
        <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-6 shadow-2xs">
          <div className="flex items-center gap-2 mb-3">
            <Lightbulb className="w-5 h-5 text-[#355E48]" />
            <h4 className="font-serif font-bold text-base text-[#302F29]">
              Recommended Directions for Future Research
            </h4>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-[#77746B]">
            <div className="p-3 rounded bg-[#F7F4EC] border border-[#DCD5C8]/70">
              <span className="font-bold text-[#302F29] block mb-1">In-Situ Ground Sensor Pairing</span>
              Coupling NASA POWER with ground automatic weather stations (AWS) from the India Meteorological Department (IMD) to quantify localized urban canopy thermal gradients.
            </div>
            <div className="p-3 rounded bg-[#F7F4EC] border border-[#DCD5C8]/70">
              <span className="font-bold text-[#302F29] block mb-1">Aerosol & Moisture Covariates</span>
              Incorporating atmospheric optical depth (AOD), cloud fraction, and specific humidity to explore the microphysical mechanisms dampening daytime maximums.
            </div>
            <div className="p-3 rounded bg-[#F7F4EC] border border-[#DCD5C8]/70">
              <span className="font-bold text-[#302F29] block mb-1">Hourly Thermal Discomfort Indices</span>
              Computing Universal Thermal Climate Index (UTCI) and Wet Bulb Globe Temperature (WBGT) to evaluate human biometeorological health impacts during extreme events.
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
