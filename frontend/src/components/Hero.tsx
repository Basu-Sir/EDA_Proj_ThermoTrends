import type { CityMeta } from '../types';
import { CITY_COLORS } from '../data';
import { MapPin, Calendar, Database, Users, GraduationCap, ShieldCheck } from 'lucide-react';

interface HeroProps {
  cities: CityMeta[];
  selectedCity: string;
  onSelectCity: (cityName: string) => void;
}

export const Hero = ({ cities, selectedCity, onSelectCity }: HeroProps) => {
  return (
    <section className="relative pt-12 pb-16 bg-[#F7F4EC] border-b border-[#DCD5C8] overflow-hidden">
      {/* Decorative ambient subtle lines */}
      <div className="absolute inset-0 opacity-[0.03] pointer-events-none bg-[radial-gradient(#302F29_1px,transparent_1px)] [background-size:16px_16px]" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
        {/* Top Badges */}
        <div className="flex flex-wrap items-center gap-2 mb-6">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider bg-[#EDE6D8] text-[#355E48] border border-[#DCD5C8]">
            <Database className="w-3.5 h-3.5" />
            NASA POWER Satellite-Reanalysis
          </span>
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider bg-[#EDE6D8] text-[#77746B] border border-[#DCD5C8]">
            <Calendar className="w-3.5 h-3.5" />
            Quarter-Century Climatological Study (2001–2025)
          </span>
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider bg-[#355E48]/10 text-[#355E48] border border-[#355E48]/20">
            <ShieldCheck className="w-3.5 h-3.5" />
            100% Complete Records (109,572 Days)
          </span>
        </div>

        {/* Hero Title & Subtitle */}
        <div className="max-w-4xl">
          <h1 className="font-serif text-3xl sm:text-4xl lg:text-5xl font-bold text-[#302F29] tracking-tight leading-[1.18] mb-4">
            ThermoTrends India
          </h1>
          <p className="font-serif text-xl sm:text-2xl text-[#77746B] italic font-normal leading-relaxed mb-6">
            A Comparative Exploratory Data Analysis of Long-Term Temperature Patterns, Warming Asymmetry, and Extreme Thermal Events Across Selected Indian Cities (2001–2025)
          </p>
          <p className="text-base sm:text-lg text-[#302F29]/80 leading-relaxed max-w-3xl mb-8">
            An empirical investigation examining quarter-century changes in daily minimum, maximum, and mean temperatures,
            diurnal temperature range (DTR) contraction, and calendar-month extreme exceedances across 12 climatically distinct metropolitan centers of India.
          </p>
        </div>

        {/* Academic Citation Block / Team Credits */}
        <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-lg p-5 mb-10 shadow-sm max-w-4xl">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 divide-y md:divide-y-0 md:divide-x divide-[#DCD5C8]">
            {/* Team Members */}
            <div className="pr-4">
              <div className="flex items-center gap-2 mb-2 text-xs font-semibold uppercase tracking-wider text-[#355E48]">
                <Users className="w-4 h-4" />
                <span>Research Team</span>
              </div>
              <p className="text-sm font-semibold text-[#302F29]">
                Rishu Kumar • Ananda Basu • Parth Mishra
              </p>
              <p className="text-xs text-[#77746B] mt-1">
                Exploratory Data Analysts & Computational Researchers
              </p>
            </div>

            {/* Academic Course */}
            <div className="pt-3 md:pt-0 md:pl-4">
              <div className="flex items-center gap-2 mb-2 text-xs font-semibold uppercase tracking-wider text-[#355E48]">
                <GraduationCap className="w-4 h-4" />
                <span>Academic Attribution</span>
              </div>
              <p className="text-sm font-semibold text-[#302F29]">
                Course: BACSE301 — Exploratory Data Analysis
              </p>
              <p className="text-xs text-[#77746B] mt-1">
                Vellore Institute of Technology (VIT), Vellore
              </p>
            </div>
          </div>
        </div>

        {/* Key Benchmark Metrics Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-10">
          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-3.5 shadow-2xs">
            <span className="text-[10px] uppercase font-bold tracking-wider text-[#77746B] block">Study Period</span>
            <span className="font-serif text-2xl font-bold text-[#302F29] block mt-0.5">25 Yrs</span>
            <span className="text-[11px] text-[#77746B] font-mono">2001 – 2025</span>
          </div>

          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-3.5 shadow-2xs">
            <span className="text-[10px] uppercase font-bold tracking-wider text-[#77746B] block">Cities Sampled</span>
            <span className="font-serif text-2xl font-bold text-[#355E48] block mt-0.5">12</span>
            <span className="text-[11px] text-[#77746B]">6 Climate Zones</span>
          </div>

          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-3.5 shadow-2xs">
            <span className="text-[10px] uppercase font-bold tracking-wider text-[#77746B] block">Total Daily Records</span>
            <span className="font-serif text-2xl font-bold text-[#302F29] block mt-0.5 tabular-nums">109,572</span>
            <span className="text-[11px] text-[#77746B]">9,131 / city</span>
          </div>

          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-3.5 shadow-2xs">
            <span className="text-[10px] uppercase font-bold tracking-wider text-[#77746B] block">Data Quality</span>
            <span className="font-serif text-2xl font-bold text-[#355E48] block mt-0.5">100%</span>
            <span className="text-[11px] text-[#77746B]">0 Missing / 0 Imputed</span>
          </div>

          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-3.5 shadow-2xs">
            <span className="text-[10px] uppercase font-bold tracking-wider text-[#77746B] block">Mean DTR Trend</span>
            <span className="font-serif text-2xl font-bold text-[#C66A4A] block mt-0.5 tabular-nums">-0.37°C</span>
            <span className="text-[11px] text-[#77746B]">Per decade (Contracting)</span>
          </div>

          <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-3.5 shadow-2xs">
            <span className="text-[10px] uppercase font-bold tracking-wider text-[#77746B] block">Tmin vs Tmax</span>
            <span className="font-serif text-2xl font-bold text-[#355E48] block mt-0.5">12 / 12</span>
            <span className="text-[11px] text-[#77746B]">Nights warming faster</span>
          </div>
        </div>

        {/* Geographic Scope: Interactive 12-City Directory Grid */}
        <div>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
            <div>
              <h3 className="font-serif text-lg font-bold text-[#302F29] flex items-center gap-2">
                <MapPin className="w-4 h-4 text-[#355E48]" />
                Geographic Coverage & Meteorological Baseline
              </h3>
              <p className="text-xs text-[#77746B]">
                Selected representative stations across North, South, East, West, Central, and Northeast India. Click any city to view its focused profile.
              </p>
            </div>
            <div className="text-xs text-[#355E48] font-semibold bg-[#EDE6D8] px-3 py-1 rounded border border-[#DCD5C8] self-start sm:self-auto">
              Selected: <span className="underline">{selectedCity === 'All' ? 'All 12 Cities' : selectedCity}</span>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2.5">
            {cities.map((c) => {
              const isSelected = selectedCity === c.name;
              const color = CITY_COLORS[c.name] || '#355E48';
              return (
                <button
                  key={c.name}
                  onClick={() => onSelectCity(c.name)}
                  className={`text-left p-3 rounded-md transition-all cursor-pointer border ${isSelected
                      ? 'bg-[#FFFEFA] border-[#355E48] shadow-md ring-2 ring-[#355E48]/20'
                      : 'bg-[#FFFEFA]/80 hover:bg-[#FFFEFA] border-[#DCD5C8] hover:border-[#355E48]/50'
                    }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span
                      className="w-2.5 h-2.5 rounded-full inline-block"
                      style={{ backgroundColor: color }}
                    />
                    <span className="text-[10px] font-mono text-[#77746B]">{c.region}</span>
                  </div>
                  <div className="font-serif font-bold text-sm text-[#302F29] truncate">{c.name}</div>
                  <div className="text-[11px] text-[#77746B] truncate">{c.state}</div>
                  <div className="mt-1.5 pt-1.5 border-t border-[#DCD5C8]/60 flex items-center justify-between text-[10px] text-[#77746B]">
                    <span>{c.elevation_m}m asl</span>
                    <span className="font-mono">{c.latitude.toFixed(1)}°N</span>
                  </div>
                  <div className="mt-1 text-[9px] uppercase tracking-wider font-semibold text-[#355E48] truncate">
                    {c.climate_zone}
                  </div>
                </button>
              );
            })}
          </div>

          {selectedCity !== 'All' && (
            <div className="mt-2 text-right">
              <button
                onClick={() => onSelectCity('All')}
                className="text-xs font-semibold text-[#355E48] hover:underline cursor-pointer"
              >
                Reset to View All 12 Cities →
              </button>
            </div>
          )}
        </div>
      </div>
    </section>
  );
};
