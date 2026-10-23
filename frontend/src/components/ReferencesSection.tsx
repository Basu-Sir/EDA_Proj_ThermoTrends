import { BookOpen, Download, ExternalLink, FileSpreadsheet } from 'lucide-react';

export const ReferencesSection = () => {
  const references = [
    {
      citation: 'Stackhouse, P. W., Zhang, T., Westberg, D., Barnett, A. J., Bristow, T., Macpherson, B., & Hoell, J. M. (2021). The NASA POWER Project: Prediction of Worldwide Energy Resources. NASA Langley Research Center.',
      url: 'https://power.larc.nasa.gov/',
      tag: 'Data Source',
    },
    {
      citation: 'IPCC (2021). Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change. Cambridge University Press.',
      url: 'https://doi.org/10.1017/9781009157896',
      tag: 'Climatology',
    },
    {
      citation: 'Karl, T. R., Jones, P. D., Knight, R. W., Kukla, G., Plummer, N., Razuvayev, V., Gallo, K. P., Lindseay, J., Charlson, R. J., & Peterson, T. C. (1993). A new perspective on recent global warming: Asymmetric trends of daily maximum and minimum temperature. Bulletin of the American Meteorological Society, 74(6), 1007–1024.',
      url: 'https://doi.org/10.1175/1520-0477(1993)074<1007:ANPORG>2.0.CO;2',
      tag: 'DTR Asymmetry',
    },
    {
      citation: 'Mann, H. B. (1945). Nonparametric tests against trend. Econometrica: Journal of the Econometric Society, 245–259.',
      url: 'https://doi.org/10.2307/1907187',
      tag: 'Statistics',
    },
    {
      citation: 'Sen, P. K. (1968). Estimates of the regression coefficient based on Kendall\'s tau. Journal of the American Statistical Association, 63(324), 1379–1389.',
      url: 'https://doi.org/10.1080/01621459.1968.10480934',
      tag: 'Statistics',
    },
    {
      citation: 'World Meteorological Organization (2017). WMO Guidelines on the Calculation of Climate Normals (WMO-No. 1203). World Meteorological Organization, Geneva.',
      url: 'https://library.wmo.int/records/item/55797-wmo-guidelines-on-the-calculation-of-climate-normals',
      tag: 'Methodology',
    },
    {
      citation: 'India Meteorological Department (2020). Climate of India 2020. National Climate Centre, India Meteorological Department, Ministry of Earth Sciences, Pune, India.',
      url: 'https://mausam.imd.gov.in/',
      tag: 'National IMD',
    },
  ];

  const downloadDatasets = [
    {
      name: 'temperature_annual.csv',
      desc: 'Annual mean temperatures (T2M, Tmin, Tmax, DTR) for all 12 cities (2001–2025).',
      path: '/data/temperature_annual.csv',
      size: '13.6 KB',
    },
    {
      name: 'city_statistics.csv',
      desc: 'Comprehensive 25-year descriptive statistics (mean, median, std, IQR, skewness) per variable.',
      path: '/data/city_statistics.csv',
      size: '4.1 KB',
    },
    {
      name: 'trend_results.csv',
      desc: 'OLS regression parameters, R², p-values, 95% CIs, Mann-Kendall statistics, and Sen’s slopes.',
      path: '/data/trend_results.csv',
      size: '6.7 KB',
    },
    {
      name: 'extreme_annual_frequencies.csv',
      desc: 'Annual counts and percentages of Hot Days (Tmax > P90) and Warm Nights (Tmin > P90).',
      path: '/data/extreme_annual_frequencies.csv',
      size: '10.5 KB',
    },
    {
      name: 'data_quality_summary.csv',
      desc: 'Station-wise audit metrics: expected vs observed records, null counts, and flags.',
      path: '/data/data_quality_summary.csv',
      size: '0.7 KB',
    },
    {
      name: 'chart_data.json',
      desc: 'Complete precomputed JSON payload driving all interactive charts and heatmaps on this site.',
      path: '/data/chart_data.json',
      size: '483 KB',
    },
  ];

  return (
    <section id="references" className="py-16 bg-[#F7F4EC] border-b border-[#DCD5C8]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="max-w-3xl mb-12">
          <div className="flex items-center gap-2 mb-2">
            <span className="section-label">Section 08 // Attribution & Reproducibility</span>
          </div>
          <h2 className="font-serif text-3xl sm:text-4xl font-bold text-[#302F29] tracking-tight">
            Scientific References & Downloadable Datasets
          </h2>
          <p className="mt-3 text-base text-[#77746B] leading-relaxed">
            Formal academic citations, NASA POWER attribution, and direct access to processed CSV and JSON datasets for independent audit and reproducibility.
          </p>
        </div>

        {/* Downloadable Processed Datasets */}
        <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-6 shadow-2xs mb-12">
          <div className="flex items-center justify-between mb-4 border-b border-[#DCD5C8] pb-3">
            <div className="flex items-center gap-2 text-sm font-bold text-[#302F29]">
              <FileSpreadsheet className="w-5 h-5 text-[#355E48]" />
              <span>Reproducible Open Data Exports (CSV & JSON)</span>
            </div>
            <span className="text-xs text-[#77746B]">
              Processed from NASA POWER Point API
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {downloadDatasets.map((ds) => (
              <div
                key={ds.name}
                className="p-4 rounded border border-[#DCD5C8] bg-[#F7F4EC]/60 hover:bg-[#F7F4EC] flex flex-col justify-between transition-colors"
              >
                <div>
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-mono text-xs font-bold text-[#355E48]">
                      {ds.name}
                    </span>
                    <span className="text-[10px] font-mono text-[#77746B] bg-[#EDE6D8] px-1.5 py-0.5 rounded">
                      {ds.size}
                    </span>
                  </div>
                  <p className="text-xs text-[#77746B] leading-relaxed mb-3">
                    {ds.desc}
                  </p>
                </div>
                <a
                  href={ds.path}
                  download={ds.name}
                  className="inline-flex items-center justify-center gap-1.5 w-full py-1.5 px-3 rounded text-xs font-semibold text-[#FFFEFA] bg-[#355E48] hover:bg-[#4A7A5F] transition-colors cursor-pointer"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Download File</span>
                </a>
              </div>
            ))}
          </div>
        </div>

        {/* Academic Bibliography */}
        <div className="bg-[#FFFEFA] border border-[#DCD5C8] rounded-md p-6 shadow-2xs">
          <div className="flex items-center gap-2 mb-4 border-b border-[#DCD5C8] pb-3">
            <BookOpen className="w-5 h-5 text-[#355E48]" />
            <h3 className="font-serif text-lg font-bold text-[#302F29]">
              Bibliographic References & Primary Literature
            </h3>
          </div>

          <div className="space-y-4">
            {references.map((ref, idx) => (
              <div
                key={idx}
                className="p-3.5 rounded bg-[#F7F4EC]/60 border border-[#DCD5C8]/80 text-xs flex flex-col sm:flex-row sm:items-start justify-between gap-3"
              >
                <div className="pr-4">
                  <span className="inline-block text-[10px] font-bold uppercase tracking-wider text-[#355E48] bg-[#EDE6D8] px-2 py-0.5 rounded mb-1.5">
                    {ref.tag}
                  </span>
                  <p className="text-[#302F29] leading-relaxed font-serif">
                    {ref.citation}
                  </p>
                </div>
                <a
                  href={ref.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 text-[11px] font-semibold text-[#355E48] hover:underline shrink-0 self-start sm:self-auto"
                >
                  <span>Source / DOI</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};
