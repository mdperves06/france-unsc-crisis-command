import React from 'react';
import { Shield, Globe, Award, Database, MessageSquare, BarChart3, AlertTriangle, Radio } from 'lucide-react';

interface TopCommandBarProps {
  currentTab: string;
  onTabChange: (tab: string) => void;
  unscYear: number;
  onYearChange: (year: number) => void;
  alertsCount: number;
  currentUser?: any;
  onLogout?: () => void;
}

export const TopCommandBar: React.FC<TopCommandBarProps> = ({
  currentTab,
  onTabChange,
  unscYear,
  onYearChange,
  alertsCount,
  currentUser,
  onLogout,
}) => {
  const tabs = [
    { id: 'world', label: 'WORLD INTELLIGENCE', icon: Globe, mode: 'MODE A' },
    { id: 'trainer', label: 'CRISIS TRAINER', icon: Award, mode: 'MODE B' },
    { id: 'arena', label: 'CRISIS ARENA', icon: Shield, mode: 'MODE C' },
    { id: 'france', label: 'FRANCE COMMAND', icon: Radio, mode: 'DOCTRINE' },
    { id: 'unsc', label: 'UNSC DATABASE', icon: Database, mode: 'ARCHIVE' },
    { id: 'labs', label: 'DIPLOMACY LABS', icon: MessageSquare, mode: 'SPEECH/EB' },
    { id: 'analytics', label: 'ANALYTICS', icon: BarChart3, mode: 'METRICS' },
  ];

  return (
    <header className="sticky top-0 z-50 bg-[#050814]/95 backdrop-blur-md border-b border-slate-800 shadow-xl">
      {/* French Republic Tricolor Ribbon Bar */}
      <div className="h-1 w-full flex">
        <div className="flex-1 bg-[#002395]" />
        <div className="flex-1 bg-[#FFFFFF]" />
        <div className="flex-1 bg-[#ED2939]" />
      </div>

      {/* Primary Command Header */}
      <div className="max-w-[1720px] mx-auto px-4 py-2 flex flex-col md:flex-row items-center justify-between gap-3">
        {/* State Identity & UNSC Role */}
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-[#002395] to-[#040c1e] border border-cyan-500/40 flex items-center justify-center shadow-glow-blue">
            <span className="font-serif font-bold text-white text-base">RF</span>
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-sm font-black tracking-wider uppercase text-white font-mono">
                RÉPUBLIQUE FRANÇAISE
              </h1>
              <span className="bg-blue-900/60 text-cyan-300 text-[10px] font-mono px-2 py-0.5 rounded border border-cyan-500/40 font-semibold">
                P5 PERMANENT MEMBER
              </span>
              <span className="bg-amber-950/70 text-amber-300 text-[10px] font-mono px-2 py-0.5 rounded border border-amber-500/40">
                VETO POWER: ACTIVE
              </span>
            </div>
            <div className="text-[11px] font-mono text-slate-400">
              MISSION PERMANENTE AUPRÈS DES NATIONS UNIES // NEW YORK HQ
            </div>
          </div>
        </div>

        {/* Global Alert Bar & Dynamic Year */}
        <div className="flex items-center space-x-4 text-xs font-mono">
          <div className="flex items-center space-x-1.5 bg-red-950/40 border border-red-500/40 px-3 py-1 rounded-full text-red-300 animate-pulse">
            <AlertTriangle className="w-3.5 h-3.5" />
            <span>{alertsCount} ACTIVE GLOBAL ALERTS</span>
          </div>

          <div className="flex items-center space-x-2 bg-slate-900 border border-slate-700 px-2.5 py-1 rounded text-slate-300">
            <span className="text-slate-400">UNSC YEAR:</span>
            <select
              value={unscYear}
              onChange={(e) => onYearChange(Number(e.target.value))}
              aria-label="UNSC Year"
              className="bg-transparent text-cyan-400 font-bold outline-none cursor-pointer"
            >
              <option value={2026} className="bg-slate-900 text-white">2026</option>
              <option value={2025} className="bg-slate-900 text-white">2025</option>
              <option value={2024} className="bg-slate-900 text-white">2024</option>
            </select>
          </div>

          <div className="hidden lg:flex items-center space-x-1 text-slate-400">
            <span className="w-2 h-2 rounded-full bg-emerald-400 inline-block animate-ping" />
            <span className="text-[11px] text-emerald-400 font-bold">PARIS SECURE CABLE: ONLINE</span>
          </div>

          {/* User Info & Logout */}
          {currentUser && (
            <div className="flex items-center space-x-2 bg-slate-900/60 border border-slate-700 px-3 py-1 rounded-lg">
              <div className="w-6 h-6 rounded-full bg-gradient-to-br from-blue-600 to-cyan-500 flex items-center justify-center text-[10px] font-bold text-white">
                {currentUser.full_name?.[0]?.toUpperCase() || 'U'}
              </div>
              <div className="hidden md:block">
                <div className="text-[10px] text-slate-300 font-mono font-semibold leading-none">{currentUser.username}</div>
                <div className="text-[9px] text-slate-500 leading-none mt-0.5 uppercase">{currentUser.role} · {currentUser.country_assignment}</div>
              </div>
              <button
                id="logout-btn"
                onClick={onLogout}
                className="ml-1 text-[10px] text-slate-500 hover:text-red-400 transition-colors font-mono border border-slate-700 hover:border-red-500/40 px-2 py-0.5 rounded"
              >
                EXIT
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Tactical Mode Navigation Tabs */}
      <div className="max-w-[1720px] mx-auto px-4 flex items-center space-x-1 overflow-x-auto border-t border-slate-800/80 pt-1 pb-1 text-xs font-mono">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = currentTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`flex items-center space-x-2 px-3.5 py-1.5 rounded transition-all whitespace-nowrap ${
                isActive
                  ? 'bg-blue-900/60 border border-cyan-400/80 text-cyan-300 shadow-glow-cyan font-bold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 border border-transparent'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{tab.label}</span>
              <span className={`text-[9px] px-1 py-0.2 rounded ${isActive ? 'bg-cyan-500/20 text-cyan-200' : 'bg-slate-800 text-slate-500'}`}>
                {tab.mode}
              </span>
            </button>
          );
        })}
      </div>
    </header>
  );
};
