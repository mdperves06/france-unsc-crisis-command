import React, { useState } from 'react';
import { analyzeSpeech, validateResolution, askEBQuestion, evaluateEBAnswer, askAIDiplomat } from '../lib/api';
import { MessageSquare, FileText, ShieldAlert, Bot, Send, CheckCircle2, AlertTriangle, ArrowRight } from 'lucide-react';

export const LabsView: React.FC = () => {
  const [activeLab, setActiveLab] = useState<'SPEECH' | 'RESOLUTION' | 'EB_ATTACK' | 'AI_DIPLOMAT'>('SPEECH');

  // Speech Lab State
  const [speechType, setSpeechType] = useState('CRISIS_SPEECH');
  const [speechText, setSpeechText] = useState('');
  const [speechResult, setSpeechResult] = useState<any | null>(null);
  const [speechLoading, setSpeechLoading] = useState(false);

  // Resolution Lab State
  const [resTitle, setResTitle] = useState('Protection of Civilian Corridors in Border Conflicts');
  const [preambles, setPreambles] = useState('Recalling S/RES/1701 (2006) and S/RES/2728 (2024),\nReaffirming the primary responsibility of the Council under Article 24 of the UN Charter,');
  const [operatives, setOperatives] = useState('1. Demands the immediate cessation of hostile armed exchanges across buffer sectors;\n2. Requests the Secretary-General deploy neutral civilian observers with host-nation consent;\n3. Decides to remain seized of the matter under Chapter VI pacific settlement.');
  const [resResult, setResResult] = useState<any | null>(null);
  const [resLoading, setResLoading] = useState(false);

  // EB Attack State
  const [ebContext, setEbContext] = useState('France tables a resolution deploying neutral UN observers without Chapter VII coercive sanctions.');
  const [ebPosition, setEbPosition] = useState('France prioritizes immediate civilian protection while preserving consensus.');
  const [ebQuestion, setEbQuestion] = useState<string | null>(null);
  const [delegateAnswer, setDelegateAnswer] = useState('');
  const [ebEvaluation, setEbEvaluation] = useState<any | null>(null);
  const [ebLoading, setEbLoading] = useState(false);

  // AI Diplomat Chat State
  const [chatPrompt, setChatPrompt] = useState('');
  const [chatPersona, setChatPersona] = useState('FRANCE_COACH');
  const [chatHistory, setChatHistory] = useState<Array<{ role: string; content: string; persona: string }>>([
    {
      role: 'assistant',
      content: 'Greetings Ambassador. I am your France Diplomatic Strategy Advisor. How may I assist your Council preparations today? You may also switch personas to test arguments against the Russian or US delegations.',
      persona: 'France Strategic Coach',
    },
  ]);
  const [chatLoading, setChatLoading] = useState(false);

  // Handlers
  const handleAnalyzeSpeech = async () => {
    if (!speechText.trim()) return;
    setSpeechLoading(true);
    try {
      const res = await analyzeSpeech(speechType, speechText);
      setSpeechResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setSpeechLoading(false);
    }
  };

  const handleValidateResolution = async () => {
    setResLoading(true);
    try {
      const pList = preambles.split('\n').filter((p) => p.trim());
      const oList = operatives.split('\n').filter((o) => o.trim());
      const res = await validateResolution(resTitle, pList, oList);
      setResResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setResLoading(false);
    }
  };

  const handleGetEBQuestion = async () => {
    setEbLoading(true);
    try {
      const res = await askEBQuestion(ebContext, ebPosition);
      setEbQuestion(res.question);
      setEbEvaluation(null);
    } catch (err) {
      console.error(err);
    } finally {
      setEbLoading(false);
    }
  };

  const handleEvaluateEBAnswer = async () => {
    if (!ebQuestion || !delegateAnswer.trim()) return;
    setEbLoading(true);
    try {
      const res = await evaluateEBAnswer(ebContext, ebQuestion, delegateAnswer);
      setEbEvaluation(res);
    } catch (err) {
      console.error(err);
    } finally {
      setEbLoading(false);
    }
  };

  const handleSendChatMessage = async () => {
    if (!chatPrompt.trim()) return;
    const prompt = chatPrompt;
    setChatPrompt('');
    setChatHistory((prev) => [...prev, { role: 'user', content: prompt, persona: 'You (France)' }]);
    setChatLoading(true);

    try {
      const res = await askAIDiplomat(prompt, chatPersona);
      setChatHistory((prev) => [
        ...prev,
        { role: 'assistant', content: res.response, persona: res.persona },
      ]);
    } catch (err) {
      console.error(err);
    } finally {
      setChatLoading(false);
    }
  };

  return (
    <div className="max-w-[1720px] mx-auto p-4 space-y-4 font-mono">
      {/* Header and Lab Switcher */}
      <div className="command-card p-4 rounded-xl border border-slate-800 flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
        <div>
          <span className="text-[10px] text-cyan-400 font-bold uppercase tracking-wider">
            TRAINING LABS & BENCHMARK SIMULATION ENGINES
          </span>
          <h2 className="text-xl font-bold text-white tracking-wide">
            DIPLOMATIC SKILLS & STRATEGY LABS
          </h2>
        </div>

        <div className="flex space-x-1 text-xs">
          {[
            { id: 'SPEECH', label: 'SPEECH LAB', icon: MessageSquare },
            { id: 'RESOLUTION', label: 'RESOLUTION LAB', icon: FileText },
            { id: 'EB_ATTACK', label: 'CHAIR CROSS-EXAM', icon: ShieldAlert },
            { id: 'AI_DIPLOMAT', label: 'AI DIPLOMAT CHAT', icon: Bot },
          ].map((lab) => {
            const Icon = lab.icon;
            return (
              <button
                key={lab.id}
                onClick={() => setActiveLab(lab.id as any)}
                className={`flex items-center space-x-1.5 px-3 py-1.5 rounded transition ${
                  activeLab === lab.id
                    ? 'bg-blue-600 text-white font-bold shadow-glow-blue'
                    : 'bg-slate-900 text-slate-400 hover:text-white'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{lab.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* 1. Speech Lab */}
      {activeLab === 'SPEECH' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <div className="command-card p-4 rounded-xl border border-slate-800 space-y-3 text-xs">
            <div className="flex justify-between items-center border-b border-slate-800 pb-2">
              <span className="text-cyan-400 font-bold">SPEECH FORMULATION & SUBMISSION</span>
              <select
                value={speechType}
                onChange={(e) => setSpeechType(e.target.value)}
                className="bg-slate-900 border border-slate-700 rounded px-2 py-1 text-slate-200"
              >
                <option value="OPENING">General Debate Opening Speech</option>
                <option value="MOD_CAUCUS">Moderated Caucus Speech</option>
                <option value="CRISIS_SPEECH">Crisis Emergency Statement</option>
                <option value="PRESS_STMT">Press Stakeout Statement</option>
              </select>
            </div>

            <textarea
              rows={8}
              value={speechText}
              onChange={(e) => setSpeechText(e.target.value)}
              placeholder="Mr. President, France takes the floor today to address the urgent degradation of civilian security along the buffer demarcation..."
              className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-xs text-slate-200 outline-none focus:border-cyan-400"
            />

            <button
              onClick={handleAnalyzeSpeech}
              disabled={speechLoading || !speechText.trim()}
              className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 rounded-lg transition flex items-center justify-center space-x-1.5 shadow-glow-blue"
            >
              <Send className="w-3.5 h-3.5" />
              <span>ANALYZE SPEECH AGAINST QUAI D'ORSAY RUBRIC</span>
            </button>
          </div>

          {/* Speech Result */}
          <div className="command-card p-4 rounded-xl border border-slate-800 text-xs space-y-3">
            <span className="text-cyan-400 font-bold border-b border-slate-800 pb-2 block">
              SPEECH RUBRIC APPRAISAL
            </span>

            {speechResult ? (
              <div className="space-y-3">
                <div className="flex items-center justify-between p-3 rounded bg-blue-950/40 border border-cyan-500/40">
                  <span className="text-slate-300 font-bold">OVERALL DIPLOMATIC SCORE:</span>
                  <span className="text-xl font-bold text-cyan-300">{speechResult.overall_score} / 10</span>
                </div>

                <div className="grid grid-cols-2 gap-2 text-[11px]">
                  <div className="p-2 rounded bg-slate-900 border border-slate-800">
                    <span className="text-slate-500">CLARITY:</span> <strong className="text-white">{speechResult.metrics.clarity}</strong>
                  </div>
                  <div className="p-2 rounded bg-slate-900 border border-slate-800">
                    <span className="text-slate-500">FRANCE RELEVANCE:</span> <strong className="text-cyan-400">{speechResult.metrics.france_relevance}</strong>
                  </div>
                  <div className="p-2 rounded bg-slate-900 border border-slate-800">
                    <span className="text-slate-500">STRUCTURE:</span> <strong className="text-white">{speechResult.metrics.structure}</strong>
                  </div>
                  <div className="p-2 rounded bg-slate-900 border border-slate-800">
                    <span className="text-slate-500">DIPLOMATIC TONE:</span> <strong className="text-emerald-400">{speechResult.metrics.diplomatic_tone}</strong>
                  </div>
                </div>

                <div className="p-2.5 rounded bg-slate-900 border border-slate-800 space-y-1">
                  <span className="text-cyan-400 font-bold text-[10px]">ACTIONABLE REVISION GUIDANCE:</span>
                  <p className="text-slate-300 text-[11px] leading-relaxed">{speechResult.actionable_revisions}</p>
                </div>
              </div>
            ) : (
              <div className="text-slate-500 py-12 text-center text-xs">
                Submit a speech draft to generate actionable analytical critique.
              </div>
            )}
          </div>
        </div>
      )}

      {/* 2. Resolution Lab */}
      {activeLab === 'RESOLUTION' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 text-xs">
          <div className="command-card p-4 rounded-xl border border-slate-800 space-y-3">
            <span className="text-cyan-400 font-bold border-b border-slate-800 pb-2 block">
              DRAFT RESOLUTION WORKSPACE
            </span>

            <div>
              <label className="text-slate-400 text-[10px]">RESOLUTION TITLE</label>
              <input
                type="text"
                value={resTitle}
                onChange={(e) => setResTitle(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded p-2 text-slate-200 mt-1"
              />
            </div>

            <div>
              <label className="text-slate-400 text-[10px]">PREAMBULATORY CLAUSES</label>
              <textarea
                rows={3}
                value={preambles}
                onChange={(e) => setPreambles(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded p-2 text-slate-200 mt-1"
              />
            </div>

            <div>
              <label className="text-slate-400 text-[10px]">OPERATIVE CLAUSES</label>
              <textarea
                rows={4}
                value={operatives}
                onChange={(e) => setOperatives(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded p-2 text-slate-200 mt-1"
              />
            </div>

            <button
              onClick={handleValidateResolution}
              disabled={resLoading}
              className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 rounded-lg transition"
            >
              RUN LEGAL & P5 VETO FEASIBILITY CHECK
            </button>
          </div>

          {/* Validation Report */}
          <div className="command-card p-4 rounded-xl border border-slate-800 space-y-3">
            <span className="text-cyan-400 font-bold border-b border-slate-800 pb-2 block">
              COUNCIL FEASIBILITY & VETO RISK REPORT
            </span>

            {resResult ? (
              <div className="space-y-3">
                <div className="flex justify-between items-center p-3 rounded bg-blue-950/40 border border-cyan-500/40">
                  <span className="text-slate-300 font-bold">VOTING VIABILITY SCORE:</span>
                  <span className="text-xl font-bold text-emerald-400">{resResult.voting_viability_score}%</span>
                </div>

                <div className="p-2.5 rounded bg-slate-900 border border-slate-800 space-y-1">
                  <span className="text-cyan-400 font-bold text-[10px]">LEGAL AUTHORITY CHECK:</span>
                  <p className="text-slate-300 text-[11px]">{resResult.legal_rationale}</p>
                </div>

                <div className="space-y-1">
                  <span className="text-red-400 font-bold text-[10px]">P5 OBJECTION & VETO RISKS:</span>
                  <div className="space-y-1">
                    {Object.entries(resResult.p5_objection_risks).map(([code, risk]) => (
                      <div key={code} className="p-2 rounded bg-slate-950 border border-slate-800 text-[11px]">
                        <span className="text-amber-400 font-bold">{code}:</span>{" "}
                        <span className="text-slate-300">{String(risk)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-slate-500 py-12 text-center">
                Submit draft clauses to check legal authority and P5 veto vulnerabilities.
              </div>
            )}
          </div>
        </div>
      )}

      {/* 3. EB / Chair Attack Simulator */}
      {activeLab === 'EB_ATTACK' && (
        <div className="command-card p-4 rounded-xl border border-slate-800 space-y-3 text-xs">
          <div className="flex justify-between items-center border-b border-slate-800 pb-2">
            <span className="text-cyan-400 font-bold">EXECUTIVE BOARD CHAIR CROSS-EXAMINATION</span>
            <button
              onClick={handleGetEBQuestion}
              disabled={ebLoading}
              className="bg-amber-600 hover:bg-amber-500 text-slate-950 font-bold px-3 py-1 rounded"
            >
              TRIGGER CHAIR ATTACK QUESTION
            </button>
          </div>

          <div className="grid grid-cols-2 gap-2 text-[11px]">
            <div>
              <label className="text-slate-500">SCENARIO CONTEXT</label>
              <input
                type="text"
                value={ebContext}
                onChange={(e) => setEbContext(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-slate-200 mt-1"
              />
            </div>
            <div>
              <label className="text-slate-500">FRANCE DEFENDED STANCE</label>
              <input
                type="text"
                value={ebPosition}
                onChange={(e) => setEbPosition(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-slate-200 mt-1"
              />
            </div>
          </div>

          {ebQuestion && (
            <div className="p-3 rounded-lg bg-red-950/40 border border-red-500/50 space-y-2">
              <span className="text-red-400 font-bold flex items-center space-x-1.5">
                <AlertTriangle className="w-4 h-4" />
                <span>CHAIR INQUIRY (HOSTILE QUESTION):</span>
              </span>
              <p className="text-slate-200 font-semibold">{ebQuestion}</p>
            </div>
          )}

          {ebQuestion && (
            <div className="space-y-2 pt-2">
              <label className="text-slate-400">YOUR DEFENSE AS DELEGATE OF FRANCE:</label>
              <textarea
                rows={3}
                value={delegateAnswer}
                onChange={(e) => setDelegateAnswer(e.target.value)}
                placeholder="Mr. Chair, France underscores that under Article 24 of the UN Charter..."
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-slate-200 outline-none focus:border-cyan-400"
              />
              <button
                onClick={handleEvaluateEBAnswer}
                disabled={ebLoading || !delegateAnswer.trim()}
                className="bg-blue-600 hover:bg-blue-500 text-white font-bold px-4 py-1.5 rounded transition"
              >
                SUBMIT DEFENSE FOR CHAIR VERDICT
              </button>
            </div>
          )}

          {ebEvaluation && (
            <div className="p-3 rounded-lg bg-slate-900 border border-emerald-500/50 space-y-1.5 mt-2">
              <div className="flex justify-between items-center">
                <span className="text-emerald-400 font-bold">{ebEvaluation.chair_verdict}</span>
                <span className="text-cyan-300 font-bold">SCORE: {ebEvaluation.score} / 10</span>
              </div>
              <p className="text-slate-300 text-[11px]">{ebEvaluation.critique}</p>
              <div className="text-[10px] text-amber-400 font-bold pt-1">
                POTENTIAL TRAP AHEAD: {ebEvaluation.follow_up_trap}
              </div>
            </div>
          )}
        </div>
      )}

      {/* 4. AI Diplomat Chat (Section 51) */}
      {activeLab === 'AI_DIPLOMAT' && (
        <div className="command-card p-4 rounded-xl border border-slate-800 space-y-3 text-xs">
          <div className="flex justify-between items-center border-b border-slate-800 pb-2">
            <span className="text-cyan-400 font-bold flex items-center space-x-1.5">
              <Bot className="w-4 h-4" />
              <span>PERSISTENT AI DIPLOMAT DIALOGUE</span>
            </span>

            <div className="flex items-center space-x-2">
              <span className="text-slate-500 text-[10px]">PERSONA:</span>
              <select
                value={chatPersona}
                onChange={(e) => setChatPersona(e.target.value)}
                className="bg-slate-900 border border-slate-700 rounded px-2 py-1 text-slate-200 text-xs"
              >
                <option value="FRANCE_COACH">Quai d'Orsay Diplomatic Coach</option>
                <option value="RUSSIAN_DELEGATE">Russian Federation PR</option>
                <option value="US_DELEGATE">United States Ambassador</option>
                <option value="HOSTILE_EB">Hostile Executive Board Director</option>
              </select>
            </div>
          </div>

          {/* Chat feed */}
          <div className="space-y-2 h-[340px] overflow-y-auto p-3 rounded-lg bg-slate-950 border border-slate-800">
            {chatHistory.map((item, idx) => (
              <div
                key={idx}
                className={`p-2.5 rounded-lg text-xs space-y-1 ${
                  item.role === 'user'
                    ? 'bg-blue-950/60 border border-blue-800 ml-8'
                    : 'bg-slate-900 border border-slate-800 mr-8'
                }`}
              >
                <div className="text-[10px] font-bold text-cyan-400">{item.persona}</div>
                <p className="text-slate-200 leading-relaxed whitespace-pre-line">{item.content}</p>
              </div>
            ))}
          </div>

          <div className="flex space-x-2 pt-1">
            <input
              type="text"
              value={chatPrompt}
              onChange={(e) => setChatPrompt(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSendChatMessage()}
              placeholder="Ask a question (e.g. 'Why does Russia care about host consent?', 'Act as US and challenge my proposal')..."
              className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 outline-none focus:border-cyan-400 text-xs"
            />
            <button
              onClick={handleSendChatMessage}
              disabled={chatLoading || !chatPrompt.trim()}
              className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg transition"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
