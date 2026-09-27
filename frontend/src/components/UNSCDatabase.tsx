import React, { useState, useEffect } from 'react';
import { UNSCMember, UNSCPresidency, UNSCResolution, UNSCVote } from '../types';
import { fetchUNSCMembers, fetchUNSCPresidencies, fetchUNSCResolutions, fetchUNSCVotes } from '../lib/api';
import { Database, Calendar, Vote, Shield, ExternalLink, Search } from 'lucide-react';

interface UNSCDatabaseProps {
  unscYear: number;
}

export const UNSCDatabase: React.FC<UNSCDatabaseProps> = ({ unscYear }) => {
  const [members, setMembers] = useState<UNSCMember[]>([]);
  const [presidencies, setPresidencies] = useState<UNSCPresidency[]>([]);
  const [resolutions, setResolutions] = useState<UNSCResolution[]>([]);
  const [votes, setVotes] = useState<UNSCVote[]>([]);
  const [activeTab, setActiveTab] = useState<'MEMBERS' | 'RESOLUTIONS' | 'VOTING' | 'PRESIDENCY'>('MEMBERS');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    async function loadUNSCData() {
      try {
        const [memData, presData, resData, voteData] = await Promise.all([
          fetchUNSCMembers(unscYear),
          fetchUNSCPresidencies(unscYear),
          fetchUNSCResolutions(),
          fetchUNSCVotes(),
        ]);
        setMembers(memData);
        setPresidencies(presData);
        setResolutions(resData);
        setVotes(voteData);
      } catch (err) {
        console.error("Failed to fetch UNSC data:", err);
      }
    }
    loadUNSCData();
  }, [unscYear]);

  return (
    <div className="max-w-[1720px] mx-auto p-4 space-y-4 font-mono">
      {/* Header Banner */}
      <div className="command-card p-4 rounded-xl border border-slate-800 flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
        <div>
          <span className="text-[10px] text-cyan-400 font-bold uppercase tracking-wider">
            OFFICIAL UN REPOSITORY // UNITED NATIONS DIGITAL LIBRARY SYNC
          </span>
          <h2 className="text-xl font-bold text-white tracking-wide">
            UN SECURITY COUNCIL INTELLIGENCE DATABASE
          </h2>
          <div className="text-xs text-slate-400">
            Active Roster Year: {unscYear} // Dynamic Membership & Presidencies Engine
          </div>
        </div>

        {/* Tab Controls */}
        <div className="flex space-x-1 text-xs">
          {[
            { id: 'MEMBERS', label: 'MEMBERSHIP ROSTER', icon: Shield },
            { id: 'RESOLUTIONS', label: 'RESOLUTIONS', icon: Database },
            { id: 'VOTING', label: 'VOTING RECORDS & VETOES', icon: Vote },
            { id: 'PRESIDENCY', label: 'PRESIDENCIES', icon: Calendar },
          ].map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center space-x-1.5 px-3 py-1.5 rounded transition ${
                  activeTab === tab.id
                    ? 'bg-blue-600 text-white font-bold shadow-glow-blue'
                    : 'bg-slate-900 text-slate-400 hover:text-white'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* 1. Membership Tab */}
      {activeTab === 'MEMBERS' && (
        <div className="space-y-3">
          <div className="text-xs text-slate-400 flex items-center justify-between border-b border-slate-800 pb-2">
            <span>MEMBERS OF THE SECURITY COUNCIL FOR {unscYear} (5 PERMANENT + 10 ELECTED)</span>
            <span className="text-cyan-400 font-bold">{members.length} SEATS LOADED</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {members.map((mem) => {
              const isP5 = mem.status === 'PERMANENT';
              const isFrance = mem.country_code === 'FRA';
              return (
                <div
                  key={mem.id}
                  className={`p-3.5 rounded-xl border transition ${
                    isFrance
                      ? 'bg-blue-950/50 border-cyan-400 shadow-glow-blue'
                      : isP5
                      ? 'bg-slate-900/90 border-slate-700'
                      : 'bg-slate-900/60 border-slate-800'
                  }`}
                >
                  <div className="flex justify-between items-start text-xs">
                    <span className="text-sm font-bold text-white flex items-center space-x-1.5">
                      <span>{mem.name}</span>
                      <span className="text-slate-400 text-xs">({mem.country_code})</span>
                    </span>
                    <span
                      className={`text-[9px] px-2 py-0.5 rounded font-bold ${
                        isP5 ? 'bg-blue-900 text-cyan-300' : 'bg-slate-800 text-slate-300'
                      }`}
                    >
                      {mem.status}
                    </span>
                  </div>

                  <div className="mt-2 text-[11px] text-slate-300 space-y-1">
                    <div>
                      <span className="text-slate-500">REGION GROUP:</span> {mem.region_group || 'N/A'}
                    </div>
                    <div>
                      <span className="text-slate-500">VETO POWER:</span>{" "}
                      <span className={mem.has_veto ? "text-amber-400 font-bold" : "text-slate-400"}>
                        {mem.has_veto ? "YES (ARTICLE 27)" : "NO"}
                      </span>
                    </div>
                    {mem.strategic_profile && (
                      <p className="text-[10px] text-slate-400 pt-1 border-t border-slate-800 line-clamp-2">
                        {mem.strategic_profile.doctrine}
                      </p>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* 2. Resolutions Tab */}
      {activeTab === 'RESOLUTIONS' && (
        <div className="space-y-3">
          <div className="space-y-2">
            {resolutions.map((res) => (
              <div key={res.id} className="command-card p-4 rounded-xl border border-slate-800 text-xs space-y-2">
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-1">
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-bold text-cyan-300">{res.resolution_number}</span>
                    {res.chapter_vii && (
                      <span className="bg-red-950 text-red-300 border border-red-500/50 text-[9px] px-2 py-0.5 rounded font-bold">
                        CHAPTER VII
                      </span>
                    )}
                    <span className="bg-emerald-950 text-emerald-300 text-[9px] px-2 py-0.5 rounded font-bold">
                      {res.outcome}
                    </span>
                  </div>
                  <span className="text-slate-500 text-[11px]">
                    ADOPTED: {new Date(res.date_adopted).toLocaleDateString()}
                  </span>
                </div>

                <h3 className="text-sm font-semibold text-white">{res.title}</h3>
                <p className="text-slate-300 text-[11px] leading-relaxed">{res.operative_summary}</p>

                <div className="flex flex-wrap items-center justify-between text-[11px] text-slate-400 pt-2 border-t border-slate-800">
                  <div className="flex space-x-3">
                    <span>YES: <strong className="text-emerald-400">{res.yes_votes}</strong></span>
                    <span>NO: <strong className="text-red-400">{res.no_votes}</strong></span>
                    <span>ABSTAIN: <strong className="text-slate-300">{res.abstentions}</strong></span>
                    <span>FRANCE VOTE: <strong className="text-cyan-400">{res.france_vote}</strong></span>
                  </div>
                  <a
                    href={res.source_url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-cyan-400 hover:underline flex items-center"
                  >
                    UN DIGITAL LIBRARY <ExternalLink className="w-2.5 h-2.5 ml-1" />
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 3. Voting Records & Vetoes Tab */}
      {activeTab === 'VOTING' && (
        <div className="space-y-3">
          <div className="space-y-2">
            {votes.map((v) => (
              <div
                key={v.id}
                className={`p-3.5 rounded-xl border text-xs space-y-1.5 ${
                  v.is_veto
                    ? 'bg-red-950/40 border-red-500/60'
                    : 'bg-slate-900/80 border-slate-800'
                }`}
              >
                <div className="flex justify-between items-center">
                  <div className="flex items-center space-x-2">
                    <span className="font-bold text-white">{v.country_code}</span>
                    <span
                      className={`font-bold px-2 py-0.5 rounded text-[10px] ${
                        v.vote === 'YES'
                          ? 'bg-emerald-950 text-emerald-300'
                          : v.vote === 'NO'
                          ? 'bg-red-950 text-red-300'
                          : 'bg-slate-800 text-slate-400'
                      }`}
                    >
                      {v.vote}
                    </span>
                    {v.is_veto && (
                      <span className="bg-red-600 text-white font-bold px-2 py-0.2 rounded text-[9px] animate-pulse">
                        P5 VETO CAST
                      </span>
                    )}
                  </div>
                  <span className="text-[10px] text-slate-500">{v.meeting_number || 'S/PV'}</span>
                </div>

                {v.explanation_of_vote && (
                  <p className="text-[11px] text-slate-300 italic bg-slate-950/60 p-2 rounded border border-slate-800">
                    "{v.explanation_of_vote}"
                  </p>
                )}

                <div className="flex justify-between items-center text-[10px] text-slate-500 pt-1">
                  <span>AGENDA: {v.agenda_item}</span>
                  <a href={v.source} target="_blank" rel="noreferrer" className="text-cyan-400 hover:underline flex items-center">
                    VERIFIED UN RECORD <ExternalLink className="w-2.5 h-2.5 ml-1" />
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 4. Presidencies Tab */}
      {activeTab === 'PRESIDENCY' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {presidencies.map((p) => {
            const isFrance = p.country_code === 'FRA';
            const monthNames = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
            return (
              <div
                key={p.month}
                className={`p-3.5 rounded-xl border ${
                  isFrance ? 'bg-blue-950/60 border-cyan-400' : 'bg-slate-900 border-slate-800'
                } text-xs space-y-1.5`}
              >
                <div className="flex justify-between items-center">
                  <span className="text-cyan-400 font-bold">{monthNames[p.month]} {p.year}</span>
                  <span className="bg-slate-800 text-slate-300 text-[10px] px-2 py-0.5 rounded font-bold">
                    {p.country_code}
                  </span>
                </div>
                <div className="text-sm font-semibold text-white">{p.country_name}</div>
                {p.signature_theme && (
                  <div className="text-[11px] text-slate-400 pt-1 border-t border-slate-800">
                    <span className="text-slate-500 font-bold">SIGNATURE THEME:</span> {p.signature_theme}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
