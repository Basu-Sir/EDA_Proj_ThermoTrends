import { useState, useEffect } from 'react';
import type { ChartData, Findings } from './types';
import { loadChartData, loadFindings } from './data';
import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { ResearchOverview } from './components/ResearchOverview';
import { Methodology } from './components/Methodology';
import { DataQualitySection } from './components/DataQualitySection';
import { ExploratoryAnalysis } from './components/ExploratoryAnalysis';
import { KeyFindings } from './components/KeyFindings';
import { CityComparison } from './components/CityComparison';
import { ConclusionLimitations } from './components/ConclusionLimitations';
import { ReferencesSection } from './components/ReferencesSection';
import { Footer } from './components/Footer';
import { Thermometer, RefreshCw, AlertCircle } from 'lucide-react';

export function App() {
  const [chartData, setChartData] = useState<ChartData | null>(null);
  const [findings, setFindings] = useState<Findings | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCity, setSelectedCity] = useState<string>('All');
  const [activeSection, setActiveSection] = useState<string>('overview');

  // Load Data
  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [cd, fd] = await Promise.all([loadChartData(), loadFindings()]);
      setChartData(cd);
      setFindings(fd);
    } catch (err: any) {
      console.error('Failed to load project data:', err);
      setError(err?.message || 'Failed to load dataset');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // Track active section for navbar highlight
  useEffect(() => {
    const handleScroll = () => {
      const sections = ['overview', 'methodology', 'quality', 'analysis', 'findings', 'compare', 'limitations', 'references'];
      const scrollPosition = window.scrollY + 200;

      for (const sectionId of sections) {
        const el = document.getElementById(sectionId);
        if (el) {
          const top = el.offsetTop;
          const height = el.offsetHeight;
          if (scrollPosition >= top && scrollPosition < top + height) {
            setActiveSection(sectionId);
            break;
          }
        }
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Loading Screen
  if (loading) {
    return (
      <div className="min-h-screen bg-[#F7F4EC] flex flex-col items-center justify-center p-4">
        <div className="w-12 h-12 rounded-lg bg-[#355E48] text-[#FFFEFA] flex items-center justify-center mb-4 shadow-sm animate-pulse">
          <Thermometer className="w-6 h-6 text-[#9CAF88]" />
        </div>
        <h2 className="font-serif text-2xl font-bold text-[#302F29] mb-2">
          ThermoTrends India
        </h2>
        <p className="text-sm text-[#77746B] font-mono flex items-center gap-2">
          <RefreshCw className="w-4 h-4 animate-spin text-[#355E48]" />
          Loading 109,572 daily climate records (2001–2025)...
        </p>
      </div>
    );
  }

  // Error Screen
  if (error || !chartData || !findings) {
    return (
      <div className="min-h-screen bg-[#F7F4EC] flex flex-col items-center justify-center p-4 text-center">
        <div className="w-12 h-12 rounded-lg bg-[#C66A4A]/20 text-[#C66A4A] flex items-center justify-center mb-4">
          <AlertCircle className="w-6 h-6" />
        </div>
        <h2 className="font-serif text-2xl font-bold text-[#302F29] mb-2">
          Dataset Access Error
        </h2>
        <p className="text-sm text-[#77746B] max-w-md mb-6 leading-relaxed">
          {error || 'Unable to parse processed JSON payloads from public/data/.'}
        </p>
        <button
          onClick={fetchData}
          className="inline-flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded bg-[#355E48] text-[#FFFEFA] hover:bg-[#4A7A5F] transition-colors cursor-pointer"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Retry Loading Datasets</span>
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-[#F7F4EC] text-[#302F29]">
      {/* Navigation */}
      <Navbar activeSection={activeSection} />

      {/* Hero Header */}
      <Hero
        cities={chartData.cities}
        selectedCity={selectedCity}
        onSelectCity={setSelectedCity}
      />

      <main className="flex-1">
        {/* Section 1: Overview */}
        <ResearchOverview />

        {/* Section 2: Methodology */}
        <Methodology />

        {/* Section 3: Data Quality */}
        <DataQualitySection dataQuality={chartData.data_quality} />

        {/* Section 4: Exploratory Analysis */}
        <ExploratoryAnalysis
          data={chartData}
          selectedCity={selectedCity}
          onSelectCity={setSelectedCity}
        />

        {/* Section 5: Key Findings */}
        <KeyFindings findings={findings} />

        {/* Section 6: City Comparison */}
        <CityComparison data={chartData} />

        {/* Section 7: Limitations & Conclusion */}
        <ConclusionLimitations />

        {/* Section 8: References & Downloads */}
        <ReferencesSection />
      </main>

      {/* Academic Footer */}
      <Footer />
    </div>
  );
}

export default App;
