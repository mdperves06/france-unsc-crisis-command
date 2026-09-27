import React, { useState, useEffect } from 'react';
import { WorldState, DiplomaticMessage, CrisisScenario } from '../types';
import {
  startPracticeSession,
  executePracticeAction,
  sendNegotiateMessage,
  fetchWorldState,
  fetchMessages,
  fetchTimeline,
  triggerAfterActionReview,
} from '../lib/api';
import { Globe3D } from './Globe3D';
import {
  Shield,
  Send,
  MessageSquare,
  Users,
  Vote,
  AlertTriangle,
  Play,
  RotateCcw,
  FileText,
  Activity,
  Award,
  X,
  Radio,
  Flame,
} from 'lucide-react';

interface PracticeArenaProps {
  scenarioId?: string;
}

export const ModePracticeArena: React.FC<PracticeArenaProps> = ({
  scenarioId = "scenario-default",
}) => {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [worldState, setWorldState] = useState<WorldState | null>(null);
  const [messages, setMessages] = useState<DiplomaticMessage[]>([]);
  const [timeline, setTimeline] = useState<any[]>([]);
  const [activeChannel, setActiveChannel] = useState<string>("USA");
  const [cableInput, setCableInput] = useState<string>("");
  const [actionType, setActionType] = useState<string>("CONTACT_USA");
  const [actionTarget, setActionTarget] = useState<string>("USA");
  const [actionRationale, setActionRationale] = useState<string>("");
  const [aarModal, setAarModal] = useState<any | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [twistNotification, setTwistNotification] = useState<any | null>(null);

  const countries = ["USA", "GBR", "RUS", "CHN", "DZA", "GUY", "KOR", "SVN", "SLE"];

  useEffect(() => {
    initSession();
  }, [scenarioId]);

  const initSession = async () => {
    setLoading(true);
    try {
      const startRes = await startPracticeSession(scenarioId);
      setSessionId(startRes.session_id);

      const [stateData, msgData, timeData] = await Promise.all([
        fetchWorldState(startRes.session_id),
        fetchMessages(startRes.session_id),
        fetchTimeline(startRes.session_id),
      ]);
      setWorldState(stateData);
      setMessages(msgData);
      setTimeline(timeData);
    } catch (err) {
      console.error("Failed to start practice session:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSendCable = async () => {
    if (!sessionId || !cableInput.trim()) return;
    setLoading(true);
    try {
      await sendNegotiateMessage({
        session_id: sessionId,
        recipient_country: activeChannel,
        content: cableInput,
      });
      setCableInput("");
      const updatedMsgs = await fetchMessages(sessionId);
      setMessages(updatedMsgs);
    } catch (err) {
      console.error("Error sending cable:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleExecuteAction = async () => {
    if (!sessionId) return;
    setLoading(true);
    try {
      const res = await executePracticeAction({
        session_id: sessionId,
        action_type: actionType,
        target_country: actionTarget,
        rationale: actionRationale,
      });

      if (res.twist_event) {
        setTwistNotification(res.twist_event);
      }

      setWorldState(res.updated_world_state);
      const [updatedMsgs, updatedTimeline] = await Promise.all([
        fetchMessages(sessionId),
        fetchTimeline(sessionId),
      ]);
      setMessages(updatedMsgs);
      setTimeline(updatedTimeline);
      setActionRationale("");
    } catch (err) {
      console.error("Action execution error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleConcludeAAR = async () => {
    if (!sessionId) return;
    setLoading(true);
    try {
      const aar = await triggerAfterActionReview(sessionId);
      setAarModal(aar);
    } catch (err) {
      console.error("AAR trigger error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-[1720px] mx-auto p-4 space-y-4">
      {/* Telemetry Status Bar */}
      {worldState && (
        <div className="command-card p-3 rounded-xl border border-slate-800 grid grid-cols-2 md:grid-cols-6 gap-3 text-xs font-mono">
          <div className="flex items-center space-x-2 border-r border-slate-800 pr-2">
            <Radio className="w-4 h-4 text-cyan-400" />
            <div>
              <div className="text-[10px] text-slate-500">SIMULATION TURN</div>
              <div className="text-sm font-bold text-white">TURN {worldState.turn}</div>
            </div>
          </div>

          <div className="border-r border-slate-800 pr-2">
            <div className="text-[10px] text-slate-500">ESCALATION LEVEL</div>
            <div className="text-sm font-bold text-amber-400">{worldState.escalation_level} / 100</div>
          </div>

          <div className="border-r border-slate-800 pr-2">
            <div className="text-[10px] text-slate-500">DIPLOMATIC TENSION</div>
            <div className="text-sm font-bold text-red-400">{worldState.diplomatic_tension} / 100</div>
          </div>

          <div className="border-r border-slate-800 pr-2">
            <div className="text-[10px] text-slate-500">HUMANITARIAN</div>
            <div className="text-sm font-bold text-purple-400">{worldState.humanitarian_status}</div>
          </div>

          <div className="border-r border-slate-800 pr-2">
            <div className="text-[10px] text-slate-500">FRANCE REPUTATION</div>
            <div className="text-sm font-bold text-cyan-300">{worldState.france_reputation} / 100</div>
          </div>

          <div className="flex items-center justify-end">
            <button
              onClick={handleConcludeAAR}
              className="bg-amber-600 hover:bg-amber-500 text-slate-950 font-bold px-3 py-1.5 rounded transition shadow-glow-gold text-[11px]"
            >
              CONCLUDE & REVIEW (AAR)
            </button>
          </div>
        </div>
      )}

      {/* Dynamic Twist Alert Popup */}
      {twistNotification && (
        <div className="p-3 rounded-lg bg-red-950/80 border border-red-500 text-xs font-mono flex items-center justify-between animate-bounce">
          <div className="flex items-center space-x-2 text-red-200">
            <AlertTriangle className="w-5 h-5 text-red-400 flex-shrink-0" />
            <div>
              <span className="font-bold uppercase tracking-wider text-red-300">
                CRISIS TWIST // {twistNotification.headline}:
              </span>{" "}
              {twistNotification.description}
            </div>
          </div>
          <button onClick={() => setTwistNotification(null)} className="text-red-300 hover:text-white ml-2">
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Main 3-Column Arena */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        {/* Left: Intelligence Feed & Council Timeline */}
        <div className="lg:col-span-3 space-y-4">
          <div className="command-card p-3 rounded-xl border border-slate-800 space-y-2 text-xs font-mono">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2 text-cyan-400 font-bold">
              <span className="flex items-center space-x-1.5">
                <Activity className="w-4 h-4" />
                <span>CHAMBER TIMELINE</span>
              </span>
              <span className="text-slate-500">{timeline.length} EVENTS</span>
            </div>
            <div className="space-y-2 max-h-[460px] overflow-y-auto pr-1">
              {timeline.map((item, idx) => (
                <div key={idx} className="p-2.5 rounded bg-slate-900 border border-slate-800 text-xs space-y-1">
                  <div className="flex justify-between items-center text-[10px] text-slate-500">
                    <span className="text-cyan-400 font-bold">TURN {item.turn}</span>
                    <span className="bg-slate-800 text-slate-300 px-1.5 py-0.2 rounded font-bold">
                      {item.authority_status}
                    </span>
                  </div>
                  <div className="font-semibold text-slate-200">{item.action_type}</div>
                  <p className="text-[11px] text-slate-400">{item.outcome_summary}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Center: Tactical Globe + Live Coalition Status + Voting Calculus */}
        <div className="lg:col-span-5 space-y-4">
          <div className="h-[320px]">
            <Globe3D />
          </div>

          {/* UNSC Voting Calculus & Article 27 Math */}
          {worldState && worldState.projected_vote && (
            <div className="command-card p-3.5 rounded-xl border border-cyan-500/40 space-y-2.5 font-mono text-xs">
              <div className="flex justify-between items-center border-b border-slate-800 pb-2">
                <span className="text-cyan-400 font-bold flex items-center space-x-1.5">
                  <Vote className="w-4 h-4" />
                  <span>UNSC ARTICLE 27(3) VOTING CALCULUS</span>
                </span>
                <span className="bg-slate-800 text-amber-300 text-[10px] px-2 py-0.5 rounded font-bold">
                  {worldState.projected_vote.outcome_prediction}
                </span>
              </div>

              {/* Vote Count Bars */}
              <div className="grid grid-cols-3 gap-2 text-center text-xs">
                <div className="p-2 rounded bg-emerald-950/40 border border-emerald-500/40">
                  <div className="text-[10px] text-slate-400">YES (AFFIRMATIVE)</div>
                  <div className="text-base font-bold text-emerald-400">
                    {worldState.projected_vote.yes_estimate} / 15
                  </div>
                  <div className="text-[9px] text-slate-500">NEED &ge; 9</div>
                </div>

                <div className="p-2 rounded bg-red-950/40 border border-red-500/40">
                  <div className="text-[10px] text-slate-400">NO (OPPOSED)</div>
                  <div className="text-base font-bold text-red-400">
                    {worldState.projected_vote.no_estimate} / 15
                  </div>
                </div>

                <div className="p-2 rounded bg-slate-900 border border-slate-700">
                  <div className="text-[10px] text-slate-400">ABSTAIN / UNDECIDED</div>
                  <div className="text-base font-bold text-slate-300">
                    {worldState.projected_vote.abstain_estimate} / 15
                  </div>
                </div>
              </div>

              {/* P5 Veto Threat Warnings */}
              <div className="p-2 rounded bg-slate-950 border border-slate-800 flex items-center justify-between text-[11px]">
                <span className="text-slate-400">P5 VETO THREATS:</span>
                <div className="flex space-x-1">
                  {worldState.projected_vote.p5_veto_threats.length > 0 ? (
                    worldState.projected_vote.p5_veto_threats.map((vetoCountry) => (
                      <span key={vetoCountry} className="bg-red-950 text-red-300 border border-red-600 px-1.5 py-0.5 rounded font-bold">
                        {vetoCountry} VETO RISK
                      </span>
                    ))
                  ) : (
                    <span className="text-emerald-400 font-bold">NO ACTIVE P5 VETO THREATS</span>
                  )}
                </div>
              </div>

              {/* Coalition Alignment Breakdown */}
              <div className="grid grid-cols-2 gap-2 text-[10px]">
                <div className="p-1.5 rounded bg-blue-950/30 border border-blue-900/50">
                  <span className="text-cyan-400 font-bold">SUPPORT COALITION:</span>
                  <div className="text-slate-300 mt-0.5 font-bold">
                    {worldState.coalition_status.support.join(", ")}
                  </div>
                </div>
                <div className="p-1.5 rounded bg-amber-950/30 border border-amber-900/50">
                  <span className="text-amber-400 font-bold">SWING / CONDITIONAL:</span>
                  <div className="text-slate-300 mt-0.5 font-bold">
                    {worldState.coalition_status.conditional.join(", ") || "None"}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Right: Bilateral Diplomatic Channels & Cables */}
        <div className="lg:col-span-4 space-y-4">
          <div className="command-card p-3 rounded-xl border border-slate-800 space-y-2 font-mono text-xs">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <span className="text-cyan-400 font-bold flex items-center space-x-1.5">
                <MessageSquare className="w-4 h-4" />
                <span>BILATERAL DIPLOMATIC CABLES</span>
              </span>
              <span className="text-[10px] text-slate-500">CHANNEL: {activeChannel}</span>
            </div>

            {/* Country Channel Selector Tabs */}
            <div className="flex space-x-1 overflow-x-auto pb-1">
              {countries.map((code) => (
                <button
                  key={code}
                  onClick={() => setActiveChannel(code)}
                  className={`px-2 py-1 rounded text-[10px] font-bold ${
                    activeChannel === code
                      ? 'bg-blue-800 text-white border border-cyan-400'
                      : 'bg-slate-900 text-slate-400 hover:bg-slate-800'
                  }`}
                >
                  {code}
                </button>
              ))}
            </div>

            {/* Cable Messages Feed */}
            <div className="space-y-2 h-[280px] overflow-y-auto pr-1 p-2 rounded bg-slate-950 border border-slate-800/80">
              {messages
                .filter((m) => m.sender === activeChannel || m.recipient === activeChannel)
                .map((msg) => {
                  const isFrance = msg.sender === "FRANCE";
                  return (
                    <div
                      key={msg.id}
                      className={`p-2.5 rounded text-xs space-y-1 ${
                        isFrance
                          ? 'bg-blue-950/60 border border-blue-800 ml-4'
                          : 'bg-slate-900 border border-slate-800 mr-4'
                      }`}
                    >
                      <div className="flex justify-between items-center text-[10px] text-slate-400">
                        <span className={`font-bold ${isFrance ? 'text-cyan-300' : 'text-amber-400'}`}>
                          {msg.sender} &rarr; {msg.recipient}
                        </span>
                        <span className="text-slate-500 font-mono">TURN {msg.turn}</span>
                      </div>
                      <p className="text-slate-200 text-[11px] leading-relaxed">{msg.content}</p>
                    </div>
                  );
                })}
            </div>

            {/* Send Cable Input */}
            <div className="flex space-x-2 pt-1">
              <input
                type="text"
                value={cableInput}
                onChange={(e) => setCableInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSendCable()}
                placeholder={`Dispatch confidential cable to ${activeChannel}...`}
                className="flex-1 bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-xs text-slate-200 outline-none focus:border-cyan-400 font-mono"
              />
              <button
                onClick={handleSendCable}
                disabled={loading || !cableInput.trim()}
                className="bg-blue-600 hover:bg-blue-500 text-white px-3 py-1.5 rounded transition"
              >
                <Send className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* Action Dispatch Bar */}
          <div className="command-card p-3 rounded-xl border border-cyan-500/40 space-y-2 font-mono text-xs">
            <div className="text-cyan-400 font-bold border-b border-slate-800 pb-1">
              FRANCE DECISION ACTION BAR
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="text-[10px] text-slate-400">ACTION TYPE</label>
                <select
                  value={actionType}
                  onChange={(e) => setActionType(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded p-1 text-slate-200 mt-0.5 text-xs"
                >
                  <option value="REQUEST_EMERGENCY_MEETING">Request Emergency Meeting</option>
                  <option value="CONTACT_USA">Bilateral Demarche: USA</option>
                  <option value="CONTACT_RUSSIA">Bilateral Demarche: Russia</option>
                  <option value="CONTACT_CHINA">Bilateral Demarche: China</option>
                  <option value="PROPOSE_CEASEFIRE">Propose Ceasefire</option>
                  <option value="DRAFT_RESOLUTION">Table Draft Resolution</option>
                  <option value="DRAFT_PRST">Draft Presidential Statement (PRST)</option>
                  <option value="THREATEN_VETO">Threaten Veto</option>
                </select>
              </div>

              <div>
                <label className="text-[10px] text-slate-400">TARGET DELEGATION</label>
                <select
                  value={actionTarget}
                  onChange={(e) => setActionTarget(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded p-1 text-slate-200 mt-0.5 text-xs"
                >
                  {countries.map((c) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="text-[10px] text-slate-400">TACTICAL RATIONALE</label>
              <input
                type="text"
                value={actionRationale}
                onChange={(e) => setActionRationale(e.target.value)}
                placeholder="E.g. Secure Russian non-objection on civilian corridors..."
                className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1 text-xs text-slate-200 outline-none font-mono"
              />
            </div>

            <button
              onClick={handleExecuteAction}
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 rounded-lg transition flex items-center justify-center space-x-1.5 shadow-glow-blue"
            >
              <Play className="w-3.5 h-3.5" />
              <span>DISPATCH FORMAL COUNCIL ACTION</span>
            </button>
          </div>
        </div>
      </div>

      {/* After-Action Review (AAR) Modal (Section 61) */}
      {aarModal && (
        <div className="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-4">
          <div className="command-card max-w-3xl w-full p-6 rounded-2xl border border-amber-500/60 space-y-4 shadow-2xl max-h-[85vh] overflow-y-auto">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <div className="flex items-center space-x-2 text-amber-400 font-mono font-bold">
                <Award className="w-5 h-5" />
                <span>SECURITY COUNCIL AFTER-ACTION REVIEW (AAR)</span>
              </div>
              <button onClick={() => setAarModal(null)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-1 font-mono">
              <span className="text-[10px] text-cyan-400 font-bold">OUTCOME SUMMARY:</span>
              <p className="text-xs text-slate-200 bg-slate-900 p-2.5 rounded border border-slate-800">
                {aarModal.what_happened}
              </p>
            </div>

            <div className="space-y-1 font-mono">
              <span className="text-[10px] text-amber-400 font-bold">FULL STRATEGIC ANALYSIS & LESSONS:</span>
              <div className="text-xs text-slate-300 bg-slate-900 p-3 rounded border border-slate-800 whitespace-pre-line leading-relaxed">
                {aarModal.full_analysis}
              </div>
            </div>

            {/* Unlocked Hidden Variables */}
            {aarModal.unlocked_hidden_variables && (
              <div className="space-y-1 font-mono text-xs">
                <span className="text-[10px] text-purple-400 font-bold">UNLOCKED SCENARIO SECRETS & RED LINES:</span>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {Object.entries(aarModal.unlocked_hidden_variables).map(([k, v]) => (
                    <div key={k} className="p-2 rounded bg-purple-950/30 border border-purple-900/50">
                      <div className="text-purple-300 font-bold uppercase">{k.replace(/_/g, " ")}:</div>
                      <div className="text-slate-300 text-[11px] mt-0.5">{String(v)}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="p-3 rounded bg-emerald-950/40 border border-emerald-500/50 text-xs font-mono text-emerald-300">
              <span className="font-bold">RECOMMENDED NEXT TRAINING FOCUS:</span>{" "}
              {aarModal.next_practice_recommendation}
            </div>

            <button
              onClick={() => setAarModal(null)}
              className="w-full bg-slate-800 hover:bg-slate-700 text-white font-mono font-bold py-2 rounded-lg transition"
            >
              CLOSE AFTER-ACTION REVIEW
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
