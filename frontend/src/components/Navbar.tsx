import { useState } from 'react';
import { Menu, X, Download, Thermometer } from 'lucide-react';

interface NavbarProps {
  activeSection: string;
}

export const Navbar = ({ activeSection }: NavbarProps) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems = [
    { id: 'overview', label: 'Overview' },
    { id: 'methodology', label: 'Methodology' },
    { id: 'quality', label: 'Data Quality' },
    { id: 'analysis', label: 'Exploratory Analysis' },
    { id: 'findings', label: 'Key Findings' },
    { id: 'compare', label: 'City Comparisons' },
    { id: 'limitations', label: 'Limitations' },
    { id: 'references', label: 'References' },
  ];

  const scrollTo = (id: string) => {
    setMobileMenuOpen(false);
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <header className="sticky top-0 z-50 bg-[#F7F4EC]/90 backdrop-blur-md border-b border-[#DCD5C8] transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Brand */}
          <div
            onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
            className="flex items-center gap-3 cursor-pointer group"
          >
            <div className="w-9 h-9 rounded-md bg-[#355E48] text-[#FFFEFA] flex items-center justify-center shadow-sm group-hover:bg-[#4A7A5F] transition-colors">
              <Thermometer className="w-5 h-5 text-[#9CAF88]" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-serif text-lg font-bold text-[#302F29] tracking-tight">
                  ThermoTrends India
                </span>
                <span className="hidden sm:inline-block text-[10px] font-semibold tracking-wider uppercase px-1.5 py-0.5 rounded bg-[#EDE6D8] text-[#355E48] border border-[#DCD5C8]">
                  2001–2025
                </span>
              </div>
              <p className="text-[11px] text-[#77746B] font-mono leading-none">
                NASA POWER • BACSE301 EDA
              </p>
            </div>
          </div>

          {/* Desktop Nav Links */}
          <nav className="hidden lg:flex items-center space-x-6">
            {navItems.map((item) => {
              const isActive = activeSection === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => scrollTo(item.id)}
                  className={`text-xs uppercase tracking-wider font-semibold transition-colors relative py-1 cursor-pointer ${isActive
                      ? 'text-[#355E48] font-bold'
                      : 'text-[#77746B] hover:text-[#302F29]'
                    }`}
                >
                  {item.label}
                  {isActive && (
                    <span className="absolute bottom-0 left-0 right-0 h-[2px] bg-[#355E48] rounded-full" />
                  )}
                </button>
              );
            })}
          </nav>

          {/* Right Action */}
          <div className="hidden sm:flex items-center gap-3">
            <button
              onClick={() => scrollTo('references')}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md text-[#355E48] bg-[#EDE6D8] hover:bg-[#DCD5C8] border border-[#DCD5C8] transition-colors cursor-pointer"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Datasets</span>
            </button>
          </div>

          {/* Mobile menu button */}
          <div className="flex lg:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-md text-[#77746B] hover:text-[#302F29] hover:bg-[#EDE6D8] focus:outline-none"
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-b border-[#DCD5C8] bg-[#FFFEFA] px-4 pt-3 pb-5 space-y-2 shadow-lg animate-fade-in-up">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => scrollTo(item.id)}
              className="block w-full text-left px-3 py-2 rounded-md text-sm font-medium text-[#302F29] hover:bg-[#EDE6D8] hover:text-[#355E48] transition-colors"
            >
              {item.label}
            </button>
          ))}
          <div className="pt-2 border-t border-[#DCD5C8]">
            <button
              onClick={() => scrollTo('references')}
              className="w-full flex items-center justify-center gap-2 px-4 py-2 text-xs font-semibold uppercase tracking-wider rounded-md text-[#FFFEFA] bg-[#355E48] hover:bg-[#4A7A5F]"
            >
              <Download className="w-4 h-4" />
              Download Clean Datasets
            </button>
          </div>
        </div>
      )}
    </header>
  );
};
