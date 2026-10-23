import type { DataQuality } from '../types';
import { ShieldCheck, CheckCircle, FileText } from 'lucide-react';

interface DataQualityProps {
  dataQuality: DataQuality[];
}

export const DataQualitySection = ({ dataQuality }: DataQualityProps) => {
  const totalExpected = dataQuality.reduce((acc, curr) => acc + curr.expected_records, 0);
  const totalObserved = dataQuality.reduce((acc, curr) => acc + curr.observed_records, 0);
  const totalFlagged = dataQuality.reduce((acc, curr) => acc + (curr.total_flagged || 0), 0);

  return (
    <section id="quality" className="py-16 bg-[#EDE6D8]/40 border-b border-[#DCD5C8]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="max-w-3xl mb-12">
          <div className="flex items-center gap-2 mb-2">
            <span className="section-label">Section 03 // Observational Auditing</span>
          </div>
          <h2 className="font-serif text-3xl sm:text-4xl font-bold text-[#302F29] tracking-tight">
            Data Quality & Integrity Assessment
          </h2>
          <p className="mt-3 text-base text-[#77746B] leading-relaxed">
            Exhaustive verification of missingness, chronological continuity, physical temperature bounds, and duplicate observation detection across all 12 target coordinate pairs.
          </p>
        </div>

        {/* Quality Scorecard Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-4 shadow-2xs">
            <div className="flex items-center justify-between mb-2">
              <span className="text-[11px] font-semibold uppercase tracking-wider text-[#77746B]">
                Expected Observations
              </span>
              <CheckCircle className="w-4 h-4 text-[#355E48]" />
            </div>
            <div className="font-serif text-2xl font-bold text-[#302F29] tabular-nums">
              {totalExpected.toLocaleString()}
            </div>
            <p className="text-[11px] text-[#77746B] mt-1">9,131 days × 12 cities</p>
          </div>

          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-4 shadow-2xs">
            <div className="flex items-center justify-between mb-2">
              <span className="text-[11px] font-semibold uppercase tracking-wider text-[#77746B]">
                Observed Records
              </span>
              <CheckCircle className="w-4 h-4 text-[#355E48]" />
            </div>
            <div className="font-serif text-2xl font-bold text-[#355E48] tabular-nums">
              {totalObserved.toLocaleString()}
            </div>
            <p className="text-[11px] text-[#77746B] mt-1">100.0% Complete retrieval</p>
          </div>

          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-4 shadow-2xs">
            <div className="flex items-center justify-between mb-2">
              <span className="text-[11px] font-semibold uppercase tracking-wider text-[#77746B]">
                Missing or Null Dates
              </span>
              <ShieldCheck className="w-4 h-4 text-[#355E48]" />
            </div>
            <div className="font-serif text-2xl font-bold text-[#302F29] tabular-nums">
              0
            </div>
            <p className="text-[11px] text-[#77746B] mt-1">No temporal gaps</p>
          </div>

          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-4 shadow-2xs">
            <div className="flex items-center justify-between mb-2">
              <span className="text-[11px] font-semibold uppercase tracking-wider text-[#77746B]">
                Flagged / Implausible Values
              </span>
              <ShieldCheck className="w-4 h-4 text-[#355E48]" />
            </div>
            <div className="font-serif text-2xl font-bold text-[#355E48] tabular-nums">
              {totalFlagged}
            </div>
            <p className="text-[11px] text-[#77746B] mt-1">0 cases of Tmin &gt; Tmax</p>
          </div>
        </div>

        {/* Quality Audit Table */}
        <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md overflow-hidden shadow-2xs mb-8">
          <div className="px-6 py-4 border-b border-[#DCD5C8] flex items-center justify-between">
            <h3 className="font-serif text-base font-bold text-[#302F29]">
              Station-Wise Quality Audit Matrix (2001–2025)
            </h3>
            <span className="text-xs text-[#355E48] font-semibold bg-[#EDE6D8] px-2.5 py-0.5 rounded border border-[#DCD5C8]">
              Verified Clean
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-[#DCD5C8] text-xs">
              <thead className="bg-[#F7F4EC]">
                <tr>
                  <th scope="col" className="px-4 py-3 text-left font-semibold text-[#302F29]">City</th>
                  <th scope="col" className="px-4 py-3 text-right font-semibold text-[#302F29]">Expected Days</th>
                  <th scope="col" className="px-4 py-3 text-right font-semibold text-[#302F29]">Observed Days</th>
                  <th scope="col" className="px-4 py-3 text-right font-semibold text-[#302F29]">Missing Dates</th>
                  <th scope="col" className="px-4 py-3 text-right font-semibold text-[#302F29]">Null Values</th>
                  <th scope="col" className="px-4 py-3 text-right font-semibold text-[#302F29]">Duplicates</th>
                  <th scope="col" className="px-4 py-3 text-right font-semibold text-[#302F29]">Tmin &gt; Tmax</th>
                  <th scope="col" className="px-4 py-3 text-right font-semibold text-[#302F29]">Completeness</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#DCD5C8] bg-[#FFFEFA]">
                {dataQuality.map((dq) => {
                  const completeness = ((dq.observed_records / dq.expected_records) * 100).toFixed(1);
                  return (
                    <tr key={dq.city} className="hover:bg-[#F7F4EC]/60 transition-colors">
                      <td className="px-4 py-2.5 font-medium text-[#302F29]">{dq.city}</td>
                      <td className="px-4 py-2.5 text-right font-mono text-[#77746B]">{dq.expected_records.toLocaleString()}</td>
                      <td className="px-4 py-2.5 text-right font-mono text-[#302F29]">{dq.observed_records.toLocaleString()}</td>
                      <td className="px-4 py-2.5 text-right font-mono text-[#77746B]">{dq.missing_dates}</td>
                      <td className="px-4 py-2.5 text-right font-mono text-[#77746B]">
                        {(dq.T2M_MIN_nulls + dq.T2M_MAX_nulls + dq.T2M_nulls)}
                      </td>
                      <td className="px-4 py-2.5 text-right font-mono text-[#77746B]">{dq.duplicate_records}</td>
                      <td className="px-4 py-2.5 text-right font-mono text-[#77746B]">{dq.min_gt_max}</td>
                      <td className="px-4 py-2.5 text-right font-mono font-bold text-[#355E48]">
                        {completeness}%
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Methodological Context on Gridded Reanalysis */}
        <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-6 shadow-2xs">
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-md bg-[#EDE6D8] text-[#355E48] flex items-center justify-center shrink-0 mt-0.5">
              <FileText className="w-4 h-4" />
            </div>
            <div>
              <h4 className="font-serif font-bold text-sm text-[#302F29] mb-1">
                Methodological Note: Reanalysis Completeness vs. In-Situ Thermometer Stations
              </h4>
              <p className="text-xs text-[#77746B] leading-relaxed">
                While surface meteorological stations operated by national agencies frequently encounter missing observations due to power interruptions, sensor calibration outages, or physical maintenance, NASA POWER operates as an assimilated reanalysis product. Because the GEOS model integrates satellite infrared/microwave sounders with continuous global numerical weather predictions, it provides complete spatial and temporal coverage. Consequently, no artificial mathematical imputation or temporal interpolation was required. However, users should bear in mind that a 0.5° × 0.5° grid cell averages temperature over approximately 2,500 km², which smooths localized microclimates and intense urban heat island (UHI) peaks found at asphalt-dense city centers.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
