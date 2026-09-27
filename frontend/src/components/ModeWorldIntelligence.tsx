import React, { useState, useEffect } from 'react';
import { Globe3D } from './Globe3D';
import { IntelligenceSource, GlobalAlert, RegionCommandProfile } from '../types';
import { fetchIntelligenceSources, fetchGlobalAlerts, fetchRegions, fetchRegionProfile } from '../lib/api';
import { AlertCircle, ExternalLink, ShieldAlert, BookOpen, Layers, X, Flame } from 'lucide-react';

interface WorldIntelligenceProps {
  onLaunchTraining: (region: string) => void;
  onLaunchPractice: (region: string) => void;
}

export const ModeWorldIntelligence: React.FC<WorldIntelligenceProps> = ({
  onLaunchTraining,
  onLaunchPractice,
}) => {
  const [sources, setSources] = useState<IntelligenceSource[]>([]);
  const [alerts, setAlerts] = useState<GlobalAlert[]>([]);
  const [regions, setRegions] = useState<RegionCommandProfile[]>([]);
  const [selectedRegionId, setSelectedRegionId] = useState<string | null>("middle-east");
  const [regionDetail, setRegionDetail] = useState<RegionCommandProfile | null>(null);
  const [activeFilter, setActiveFilter] = useState<string>("ALL");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [srcData, altData, regData] = await Promise.all([
          fetchIntelligenceSources(),
          fetchGlobalAlerts(),
          fetchRegions(),
        ]);
        setSources(srcData);
        setAlerts(altData);
        setRegions(regData);

        if (regData.length > 0) {
          const detail = await fetchRegionProfile(regData[0].region_id);
          setRegionDetail(detail);
        }
      } catch (err) {
        console.error("Failed to load world intelligence:", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const handleSelectRegion = async (regionId: string) => {
    setSelectedRegionId(regionId);
    try {
      const detail = await fetchRegionProfile(regionId);
      setRegionDetail(detail);
    } catch (err) {
      // Non-crisis pins (Paris HQ, UN HQ) have no region profile
      console.error("Error fetching region detail:", err);
      setRegionDetail(null);
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'VERIFIED FACT':
        return <span className="bg-emerald-950/80 text-emerald-400 border border-emerald-500/40 text-[9px] px-2 py-0.5 rounded font-mono font-bold">VERIFIED FACT</span>;
      case 'OFFICIAL STATEMENT':
        return <span className="bg-blue-950/80 text-cyan-300 border border-cyan-500/40 text-[9px] px-2 py-0.5 rounded font-mono font-bold">OFFICIAL STATEMENT</span>;
      case 'REPORTED':
        return <span className="bg-amber-950/80 text-amber-300 border border-amber-500/40 text-[9px] px-2 py-0.5 rounded font-mono font-bold">REPORTED</span>;
      case 'ANALYSIS':
        return <span className="bg-purple-950/80 text-purple-300 border border-purple-500/40 text-[9px] px-2 py-0.5 rounded font-mono font-bold">ANALYSIS</span>;
      default:
        return <span className="bg-slate-800 text-slate-300 text-[9px] px-2 py-0.5 rounded font-mono">{status}</span>;
    }
  };

  return (
    <div className="max-w-[1720px] mx-auto p-4 space-y-4">
      {/* Mode Banner */}
      <div className="bg-blue-950/40 border border-blue-900/60 p-3 rounded-lg flex items-center justify-between text-xs font-mono">
        <div className="flex items-center space-x-2 text-cyan-300">
          <Layers className="w-4 h-4 text-cyan-400" />
          <span className="font-bold tracking-wider">MODE A: REAL-WORLD INTELLIGENCE // SOURCE-VERIFIED SENSORS</span>
        </div>
        <div className="text-slate-400">
          STRICT PROVENANCE ENFORCED: VERIFIED FACT ≠ UNCONFIRMED
        </div>
      </div>

      {/* Main 3-Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        {/* Left Column: Alerts & Regional Profiles */}
        <div className="lg:col-span-3 space-y-4">
          {/* Active Global Alerts */}
          <div className="command-card p-3 rounded-xl border border-slate-800 space-y-2">
            <div className="flex items-center justify-between text-xs font-mono border-b border-slate-800 pb-2">
              <span className="text-red-400 flex items-center space-x-1.5 font-bold">
                <AlertCircle className="w-4 h-4" />
                <span>ACTIVE GLOBAL ALERTS</span>
              </span>
              <span className="text-slate-500">{alerts.length} NOTICES</span>
            </div>
            <div className="space-y-2 max-h-[220px] overflow-y-auto pr-1">
              {alerts.map((alt) => (
                <div key={alt.id} className="p-2.5 rounded bg-slate-900/80 border-l-2 border-red-500 text-xs space-y-1">
                  <div className="flex justify-between items-start">
                    <span className="font-semibold text-slate-200">{alt.headline}</span>
                  </div>
                  <p className="text-slate-400 text-[11px]">{alt.details}</p>
                  <div className="flex justify-between items-center text-[10px] text-slate-500 pt-1 font-mono">
                    <span>REGION: {alt.region}</span>
                    <a href={alt.source_url} target="_blank" rel="noreferrer" className="text-cyan-400 flex items-center hover:underline">
                      SOURCE <ExternalLink className="w-2.5 h-2.5 ml-0.5" />
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Regional Theaters Selector */}
          <div className="command-card p-3 rounded-xl border border-slate-800 space-y-2">
            <div className="text-xs font-mono text-cyan-400 border-b border-slate-800 pb-2 font-bold flex items-center space-x-1.5">
              <Flame className="w-4 h-4" />
              <span>GEOPOLITICAL THEATERS</span>
            </div>
            <div className="space-y-1.5">
              {regions.map((reg) => (
                <button
                  key={reg.region_id}
                  onClick={() => handleSelectRegion(reg.region_id)}
                  className={`w-full text-left p-2.5 rounded text-xs transition-all flex items-center justify-between font-mono ${
                    selectedRegionId === reg.region_id
                      ? 'bg-blue-900/50 border border-cyan-400 text-cyan-200'
                      : 'bg-slate-900/60 hover:bg-slate-800 text-slate-300 border border-transparent'
                  }`}
                >
                  <span className="font-semibold">{reg.name}</span>
                  <span className="text-[10px] text-slate-400">COMMAND VIEW &rarr;</span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Center Column: 3D Tactical Globe & Region Command Center */}
        <div className="lg:col-span-6 space-y-4">
          <div className="h-[440px]">
            <Globe3D onSelectRegion={handleSelectRegion} selectedRegion={selectedRegionId} />
          </div>

          {/* Selected Region Detailed Command Center (Section 8 & 67) */}
          {regionDetail && (
            <div className="command-card p-4 rounded-xl border border-cyan-500/40 space-y-3">
              <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                <div>
                  <span className="text-[10px] font-mono text-cyan-400 font-bold uppercase tracking-wider">
                    REGION COMMAND CENTER // {regionDetail.region_id}
                  </span>
                  <h2 className="text-base font-bold text-white">{regionDetail.name}</h2>
                </div>
                <div className="flex space-x-2">
                  <button
                    onClick={() => onLaunchTraining(regionDetail.name)}
                    className="bg-blue-700 hover:bg-blue-600 text-white text-xs font-mono font-bold px-3 py-1.5 rounded transition shadow-glow-blue"
                  >
                    TRAIN THIS REGION
                  </button>
                  <button
                    onClick={() => onLaunchPractice(regionDetail.name)}
                    className="bg-amber-600 hover:bg-amber-500 text-slate-950 text-xs font-mono font-bold px-3 py-1.5 rounded transition shadow-glow-gold"
                  >
                    PRACTICE THIS CRISIS
                  </button>
                </div>
              </div>

              {/* Current Situation & France Doctrine */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                <div className="p-2.5 rounded bg-slate-900/90 border border-slate-800 space-y-1">
                  <div className="text-cyan-400 font-mono font-semibold">CURRENT SITUATION</div>
                  <p className="text-slate-300 text-[11px] leading-relaxed">{regionDetail.current_situation}</p>
                </div>
                <div className="p-2.5 rounded bg-blue-950/40 border border-blue-900/60 space-y-1">
                  <div className="text-blue-300 font-mono font-semibold">FRANCE HISTORICAL ROLE & RELEVANCE</div>
                  <p className="text-slate-300 text-[11px] leading-relaxed">{regionDetail.france_historical_role}</p>
                </div>
              </div>

              {/* Escalation Risks & De-escalation Opportunities */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-[11px]">
                <div className="p-2 rounded bg-red-950/30 border border-red-900/40">
                  <span className="text-red-400 font-mono font-bold">ESCALATION RISKS:</span>
                  <ul className="list-disc list-inside text-slate-300 mt-1 space-y-0.5">
                    {regionDetail.escalation_risks.map((r, i) => <li key={i}>{r}</li>)}
                  </ul>
                </div>
                <div className="p-2 rounded bg-emerald-950/30 border border-emerald-900/40">
                  <span className="text-emerald-400 font-mono font-bold">DE-ESCALATION OPPORTUNITIES:</span>
                  <ul className="list-disc list-inside text-slate-300 mt-1 space-y-0.5">
                    {regionDetail.deescalation_opportunities.map((o, i) => <li key={i}>{o}</li>)}
                  </ul>
                </div>
              </div>

              {/* Benchmarked UNSC Resolutions */}
              <div className="text-[11px] font-mono flex items-center space-x-2 text-slate-400 pt-1">
                <span className="text-slate-500 font-bold">KEY UNSC INSTRUMENTS:</span>
                {regionDetail.key_resolutions.map((res, i) => (
                  <span key={i} className="bg-slate-800 text-cyan-300 px-2 py-0.5 rounded border border-slate-700">
                    {res}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Source-Backed Intelligence Stream (Sections 5 & 6) */}
        <div className="lg:col-span-3 space-y-3">
          <div className="command-card p-3 rounded-xl border border-slate-800 space-y-2">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <span className="text-xs font-mono font-bold text-cyan-400 flex items-center space-x-1.5">
                <BookOpen className="w-4 h-4" />
                <span>VERIFIED SOURCE INGESTION</span>
              </span>
              <span className="text-[10px] font-mono text-slate-500">{sources.length} SOURCES</span>
            </div>

            {/* Filter buttons */}
            <div className="flex space-x-1 text-[10px] font-mono">
              {['ALL', 'VERIFIED FACT', 'OFFICIAL STATEMENT', 'ANALYSIS'].map((filter) => (
                <button
                  key={filter}
                  onClick={() => setActiveFilter(filter)}
                  className={`px-2 py-0.5 rounded ${
                    activeFilter === filter ? 'bg-cyan-600 text-white' : 'bg-slate-900 text-slate-400 hover:text-white'
                  }`}
                >
                  {filter}
                </button>
              ))}
            </div>

            {/* Stream */}
            <div className="space-y-2.5 max-h-[620px] overflow-y-auto pr-1">
              {sources
                .filter((s) => activeFilter === 'ALL' || s.verification_status === activeFilter)
                .map((src) => (
                  <div key={src.id} className="p-3 rounded bg-slate-900/90 border border-slate-800/80 space-y-1.5">
                    <div className="flex items-center justify-between">
                      {getStatusBadge(src.verification_status)}
                      <span className="text-[10px] font-mono text-slate-500">{src.publisher}</span>
                    </div>

                    <h4 className="text-xs font-semibold text-slate-200 leading-snug">{src.title}</h4>
                    <p className="text-[11px] text-slate-400">{src.summary}</p>

                    <div className="flex items-center justify-between text-[10px] font-mono text-slate-500 pt-1 border-t border-slate-800/60">
                      <span>CONFIDENCE: {Math.round(src.confidence_score * 100)}%</span>
                      <a
                        href={src.url}
                        target="_blank"
                        rel="noreferrer"
                        className="text-cyan-400 hover:underline flex items-center"
                      >
                        OPEN SOURCE <ExternalLink className="w-2.5 h-2.5 ml-1" />
                      </a>
                    </div>
                  </div>
                ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
