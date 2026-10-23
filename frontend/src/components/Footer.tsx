import { Thermometer, ArrowUp, GraduationCap } from 'lucide-react';

export const Footer = () => {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <footer className="bg-[#EDE6D8] border-t border-[#DCD5C8] py-12 text-[#302F29]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 pb-8 border-b border-[#DCD5C8]">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-md bg-[#355E48] text-[#FFFEFA] flex items-center justify-center">
              <Thermometer className="w-5 h-5 text-[#9CAF88]" />
            </div>
            <div>
              <span className="font-serif text-lg font-bold text-[#302F29] tracking-tight block">
                ThermoTrends India
              </span>
              <p className="text-xs text-[#77746B]">
                Comparative Exploratory Data Analysis (2001–2025)
              </p>
            </div>
          </div>

          <button
            onClick={scrollToTop}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded bg-[#FFFEFA] text-[#355E48] border border-[#DCD5C8] hover:bg-[#F7F4EC] transition-colors cursor-pointer"
          >
            <ArrowUp className="w-3.5 h-3.5" />
            <span>Back to Top</span>
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-8 text-xs text-[#77746B]">
          <div>
            <div className="flex items-center gap-1.5 font-bold text-[#302F29] mb-1.5 uppercase tracking-wider text-[11px]">
              <GraduationCap className="w-4 h-4 text-[#355E48]" />
              Academic Attribution
            </div>
            <p className="leading-relaxed">
              Course: BACSE301 — Exploratory Data Analysis<br />
              Department of Computer Science and Engineering<br />
              Vellore Institute of Technology (VIT), Vellore, Tamil Nadu, India.
            </p>
          </div>

          <div>
            <div className="font-bold text-[#302F29] mb-1.5 uppercase tracking-wider text-[11px]">
              Research Authors
            </div>
            <p className="leading-relaxed font-medium text-[#302F29]">
              Rishu Kumar • Ananda Basu • Parth Mishra
            </p>
            <p className="mt-1 leading-relaxed">
              Comprehensive exploratory investigation of thermal asymmetry, diurnal dampening, and calendar-month percentile extremes.
            </p>
          </div>

          <div>
            <div className="font-bold text-[#302F29] mb-1.5 uppercase tracking-wider text-[11px]">
              Data Source & Disclaimer
            </div>
            <p className="leading-relaxed">
              Data retrieved via NASA POWER API (Langley Research Center). This study is purely exploratory and descriptive. It does not assert direct physical causation or construct predictive forecasting models.
            </p>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-[#DCD5C8]/70 flex flex-col sm:flex-row items-center justify-between text-[11px] text-[#77746B]">
          <p>© 2026 ThermoTrends India. Built with React, Vite, TypeScript & Recharts.</p>
          <p className="mt-2 sm:mt-0 font-mono">109,572 Daily Observations • 12 Indian Cities</p>
        </div>
      </div>
    </footer>
  );
};
