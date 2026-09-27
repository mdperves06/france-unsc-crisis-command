import React, { useState, useEffect } from 'react';
import { fetchAnalytics } from '../lib/api';
import { CompetencyMetric } from '../types';
import { BarChart3, TrendingUp, AlertTriangle, Target, CheckCircle2, Shield } from 'lucide-react';

export const AnalyticsView: React.FC = () => {
  const [metrics, setMetrics] = useState<CompetencyMetric[]>([]);
  const [profile, setProfile] = useState<any | null>(null);

  useEffect(() => {
    async function loadMetrics() {
      try {
        const data = await fetchAnalytics();
        setMetrics(data.competencies);
        setProfile(data);
      } catch (err) {
        console.error("Failed to fetch analytics:", err);
      }
    }
    loadMetrics();
  }, []);

  return (
    <div className="max-w-[1720px] mx-auto p-4 space-y-4 font-mono">
      {/* Header */}
      <div className="command-card p-4 rounded-xl border border-slate-800 flex justify-between items-center">
        <div>
          <span className="text-[10px] text-cyan-400 font-bold uppercase tracking-wider">
            DELEGATE PERFORMANCE & LEARNING MEMORY // 16 COMPETENCIES
          </span>
          <h2 className="text-xl font-bold text-white tracking-wide">
            FRANCE DIPLOMATIC DIAGNOSTICS & ANALYTICS
          </h2>
          <div className="text-xs text-slate-400">
            Persistent Tracking Across Simulation Runs // Non-Arbitrary Multi-Dimensional Appraisal
          </div>
        </div>

        <div className="text-right">
          <div className="text-xs text-slate-400">SCENARIOS COMPLETED</div>
          <div className="text-xl font-bold text-cyan-300">
            {profile ? profile.completed_scenarios_count : 0}
          </div>
        </div>
      </div>

      {/* 16 Competency Grid */}
      <div className="command-card p-4 rounded-xl border border-slate-800 space-y-3">
        <div className="flex justify-between items-center border-b border-slate-800 pb-2 text-xs">
          <span className="text-cyan-400 font-bold flex items-center space-x-1.5">
            <BarChart3 className="w-4 h-4" />
            <span>16 CORE DIPLOMATIC COMPETENCY METRICS</span>
          </span>
          <span className="text-slate-500">BENCHMARK: 100 PTS</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
          {metrics.map((m, idx) => {
            const pct = Math.min(100, Math.max(0, m.score));
            const colorClass =
              pct >= 75 ? 'bg-emerald-500' : pct >= 55 ? 'bg-cyan-500' : 'bg-amber-500';

            return (
              <div key={idx} className="p-3 rounded-lg bg-slate-900 border border-slate-800 space-y-1.5">
                <div className="flex justify-between items-center text-xs">
                  <span className="text-slate-200 font-semibold">{m.skill}</span>
                  <span className="font-bold text-cyan-300">{Math.round(m.score)}%</span>
                </div>
                <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div
                    className={`h-full ${colorClass} transition-all duration-500`}
                    style={{ width: `${pct}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Qualitative Diagnostic Memory (Section 59) */}
      {profile && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          {/* Strong Areas */}
          <div className="command-card p-3.5 rounded-xl border border-emerald-900/60 space-y-2">
            <span className="text-emerald-400 font-bold flex items-center space-x-1.5 border-b border-slate-800 pb-1">
              <CheckCircle2 className="w-4 h-4" />
              <span>CONFIRMED STRENGTHS</span>
            </span>
            <ul className="list-disc list-inside text-slate-300 space-y-1 text-[11px]">
              {profile.strong_areas.map((s: string, i: number) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          </div>

          {/* Weak Areas & Blind Spots */}
          <div className="command-card p-3.5 rounded-xl border border-red-900/60 space-y-2">
            <span className="text-red-400 font-bold flex items-center space-x-1.5 border-b border-slate-800 pb-1">
              <AlertTriangle className="w-4 h-4" />
              <span>FREQUENT BLIND SPOTS</span>
            </span>
            <div className="space-y-1 text-[11px] text-slate-300">
              <div>
                <span className="text-amber-400 font-bold">Frequently Missed Actors:</span>{" "}
                {profile.frequently_missed_actors.join(", ")}
              </div>
              <div>
                <span className="text-red-400 font-bold">Frequently Missed Risks:</span>{" "}
                {profile.frequently_missed_risks.join(", ")}
              </div>
            </div>
          </div>

          {/* Recommended Next Focus */}
          <div className="command-card p-3.5 rounded-xl border border-cyan-900/60 space-y-2">
            <span className="text-cyan-400 font-bold flex items-center space-x-1.5 border-b border-slate-800 pb-1">
              <Target className="w-4 h-4" />
              <span>TARGETED NEXT TRAINING EXERCISE</span>
            </span>
            <p className="text-slate-200 text-xs leading-relaxed bg-blue-950/40 p-2.5 rounded border border-blue-900/60">
              {profile.recommended_next_focus}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
