import React, { useState, useEffect } from 'react';
import { CurriculumModule } from '../types';
import { fetchCurriculum } from '../lib/api';
import { Shield, BookOpen, Award, CheckCircle, ExternalLink, X, Compass, Lock } from 'lucide-react';

export const FranceCommandCenter: React.FC = () => {
  const [modules, setModules] = useState<CurriculumModule[]>([]);
  const [selectedModule, setSelectedModule] = useState<CurriculumModule | null>(null);
  const [categoryFilter, setCategoryFilter] = useState<string>("ALL");

  useEffect(() => {
    async function loadCurriculum() {
      try {
        const data = await fetchCurriculum();
        setModules(data);
      } catch (err) {
        console.error("Failed to load curriculum:", err);
      }
    }
    loadCurriculum();
  }, []);

  const categories = ["ALL", "Foundation", "Regional", "Mechanisms", "Advanced"];

  return (
    <div className="max-w-[1720px] mx-auto p-4 space-y-4">
      {/* France Strategic Posture Header (Section 37) */}
      <div className="command-card p-4 rounded-xl border border-blue-900/60 bg-gradient-to-r from-[#002395]/20 via-[#0a1530]/60 to-[#ed2939]/20 font-mono">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
          <div>
            <span className="text-[10px] text-cyan-400 font-bold uppercase tracking-wider">
              QUAI D'ORSAY STRATEGIC POSTURE BRIEFING
            </span>
            <h2 className="text-xl font-bold text-white tracking-wide">
              FRANCE PERMANENT MISSION TO THE UNITED NATIONS
            </h2>
            <div className="text-xs text-slate-300 mt-0.5">
              Diplomatic Doctrine: European Strategic Autonomy // Multilateral Legality // Humanitarian Primacy
            </div>
          </div>

          <div className="flex items-center space-x-2 text-xs">
            <span className="bg-emerald-950/70 border border-emerald-500/50 text-emerald-400 px-3 py-1 rounded font-bold">
              VETO RESTRAINT DOCTRINE: ACTIVE (0 VETOES SINCE 1989)
            </span>
          </div>
        </div>
      </div>

      {/* France Core Strategic Matrices */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs font-mono">
        {/* Objectives */}
        <div className="command-card p-3.5 rounded-xl border border-blue-800/60 space-y-2">
          <div className="text-cyan-400 font-bold border-b border-slate-800 pb-1 flex items-center space-x-1.5">
            <Compass className="w-4 h-4" />
            <span>FRANCE CORE OBJECTIVES</span>
          </div>
          <ul className="list-disc list-inside text-slate-300 space-y-1 text-[11px]">
            <li>Preserve universal adherence to UN Charter Chapter VI/VII</li>
            <li>Maintain European Union voice and cohesion in New York</li>
            <li>Protect civilian populations and humanitarian corridors</li>
            <li>Prevent P5 Council paralysis through bridge-building</li>
          </ul>
        </div>

        {/* Red Lines */}
        <div className="command-card p-3.5 rounded-xl border border-red-800/60 space-y-2">
          <div className="text-red-400 font-bold border-b border-slate-800 pb-1 flex items-center space-x-1.5">
            <Shield className="w-4 h-4" />
            <span>FRANCE RED LINES</span>
          </div>
          <ul className="list-disc list-inside text-slate-300 space-y-1 text-[11px]">
            <li>No legal recognition of territorial gains seized by force</li>
            <li>No impunity for chemical weapons or war crimes</li>
            <li>No unilateral deployment bypassing Council legality</li>
            <li>No weaponization of humanitarian relief access</li>
          </ul>
        </div>

        {/* Strategic Leverage */}
        <div className="command-card p-3.5 rounded-xl border border-amber-800/60 space-y-2">
          <div className="text-amber-400 font-bold border-b border-slate-800 pb-1 flex items-center space-x-1.5">
            <Award className="w-4 h-4" />
            <span>DIPLOMATIC LEVERAGE</span>
          </div>
          <ul className="list-disc list-inside text-slate-300 space-y-1 text-[11px]">
            <li>Historic penholdership on Francophone Africa and Levant</li>
            <li>EU economic and development funding weight</li>
            <li>Global diplomatic network (3rd largest worldwide)</li>
            <li>Nuclear power & permanent UNSC veto authority</li>
          </ul>
        </div>

        {/* Coalitions & Swing Actors */}
        <div className="command-card p-3.5 rounded-xl border border-purple-800/60 space-y-2">
          <div className="text-purple-400 font-bold border-b border-slate-800 pb-1 flex items-center space-x-1.5">
            <Shield className="w-4 h-4" />
            <span>PARTNERSHIP ARCHITECTURE</span>
          </div>
          <div className="space-y-1 text-[11px] text-slate-300">
            <div><span className="text-cyan-400 font-bold">P3 Core:</span> USA & United Kingdom</div>
            <div><span className="text-purple-300 font-bold">European Pillars:</span> Denmark, Greece, Latvia</div>
            <div><span className="text-amber-400 font-bold">Key Swing Partners:</span> A3 (Somalia, DRC, Liberia)</div>
            <div><span className="text-red-400 font-bold">Dialogue Adversary:</span> Russian Federation</div>
          </div>
        </div>
      </div>

      {/* 24 France-Specific Training Academy Modules (Section 39) */}
      <div className="command-card p-4 rounded-xl border border-slate-800 space-y-3">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center border-b border-slate-800 pb-2 gap-2">
          <div>
            <span className="text-[10px] font-mono text-cyan-400 font-bold uppercase tracking-wider">
              DIPLOMATIC CURRICULUM // 24 MODULES
            </span>
            <h3 className="text-base font-bold text-white font-mono">
              FRANCE UNSC DIPLOMATIC ACADEMY
            </h3>
          </div>

          {/* Filter Pills */}
          <div className="flex space-x-1 text-xs font-mono">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setCategoryFilter(cat)}
                className={`px-2.5 py-1 rounded transition ${
                  categoryFilter === cat
                    ? 'bg-blue-600 text-white font-bold'
                    : 'bg-slate-900 text-slate-400 hover:text-white'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Modules Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {modules
            .filter((m) => categoryFilter === "ALL" || m.category === categoryFilter)
            .map((mod) => (
              <div
                key={mod.id}
                onClick={() => setSelectedModule(mod)}
                className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-cyan-500/60 cursor-pointer transition space-y-2 group"
              >
                <div className="flex justify-between items-start text-xs font-mono">
                  <span className="text-cyan-400 font-bold group-hover:text-cyan-300">
                    MODULE {mod.module_number}
                  </span>
                  <span className="bg-slate-800 text-slate-400 text-[10px] px-2 py-0.5 rounded">
                    {mod.category}
                  </span>
                </div>

                <h4 className="text-xs font-semibold text-slate-200 group-hover:text-white leading-snug">
                  {mod.title}
                </h4>

                <p className="text-[11px] text-slate-400 line-clamp-2 leading-relaxed">
                  {mod.description}
                </p>

                <div className="flex items-center justify-between text-[10px] font-mono text-slate-500 pt-1 border-t border-slate-800">
                  <span className="text-cyan-500">INSPECT DOCTRINE &rarr;</span>
                  <BookOpen className="w-3.5 h-3.5 text-slate-400 group-hover:text-cyan-400" />
                </div>
              </div>
            ))}
        </div>
      </div>

      {/* Module Detailed Reader Modal */}
      {selectedModule && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="command-card max-w-2xl w-full p-6 rounded-2xl border border-cyan-500/60 space-y-4 shadow-2xl max-h-[85vh] overflow-y-auto font-mono">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <div>
                <span className="text-[10px] text-cyan-400 font-bold">
                  MODULE {selectedModule.module_number} // {selectedModule.category.toUpperCase()}
                </span>
                <h3 className="text-base font-bold text-white mt-0.5">{selectedModule.title}</h3>
              </div>
              <button onClick={() => setSelectedModule(null)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-1 text-xs">
              <span className="text-[10px] text-slate-400 font-bold">OVERVIEW:</span>
              <p className="text-slate-200 leading-relaxed bg-slate-900 p-2.5 rounded border border-slate-800">
                {selectedModule.description}
              </p>
            </div>

            <div className="space-y-1 text-xs">
              <span className="text-[10px] text-cyan-400 font-bold">QUAI D'ORSAY CORE DOCTRINE:</span>
              <p className="text-slate-300 leading-relaxed bg-blue-950/40 p-2.5 rounded border border-blue-900/60">
                {selectedModule.core_doctrine}
              </p>
            </div>

            <div className="space-y-1 text-xs">
              <span className="text-[10px] text-amber-400 font-bold">FRENCH HISTORICAL PRECEDENT CASES:</span>
              <div className="space-y-1.5">
                {selectedModule.france_historical_cases.map((c, i) => (
                  <div key={i} className="p-2 rounded bg-slate-900 border border-slate-800 text-[11px]">
                    <span className="text-amber-300 font-bold">{c.case}:</span>{" "}
                    <span className="text-slate-300">{c.notes}</span>
                  </div>
                ))}
              </div>
            </div>

            <button
              onClick={() => setSelectedModule(null)}
              className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 rounded-lg transition text-xs"
            >
              CLOSE MODULE
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
