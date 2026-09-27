import React, { useState, useEffect } from 'react';
import { CrisisScenario, PanicBreakdown } from '../types';
import { generateCrisis, submitTrainStep, triggerPanicBreakdown, fetchHint } from '../lib/api';
import { Award, HelpCircle, ChevronRight, CheckCircle2, AlertOctagon, Lightbulb, RefreshCw, Send, ArrowRight, X } from 'lucide-react';

interface CrisisTrainerProps {
  initialRegion?: string;
  onAdvanceToPractice: (scenarioId: string) => void;
}

const FRAMEWORK_STEPS = [
  "1. UNDERSTAND THE CRISIS",
  "2. IDENTIFY UNCERTAINTIES",
  "3. IDENTIFY IMMEDIATE THREAT",
  "4. DEFINE FRANCE'S INTEREST",
  "5. DEFINE FRANCE'S OBJECTIVE",
  "6. DEFINE RED LINES",
  "7. IDENTIFY AVAILABLE AUTHORITY",
  "8. MAP ACTORS",
  "9. MAP SUPPORT",
  "10. MAP OPPOSITION & BLOCKERS",
  "11. IDENTIFY NEGOTIATION SPACE",
  "12. SELECT FIRST MOVE",
  "13. PREPARE BACKUP PLAN",
  "14. ANTICIPATE CONSEQUENCES",
];

export const ModeCrisisTrainer: React.FC<CrisisTrainerProps> = ({
  initialRegion = "Middle East",
  onAdvanceToPractice,
}) => {
  const [scenario, setScenario] = useState<CrisisScenario | null>(null);
  const [currentStep, setCurrentStep] = useState<number>(1);
  const [userAnswer, setUserAnswer] = useState<string>("");
  const [feedback, setFeedback] = useState<any>(null);
  const [panicModal, setPanicModal] = useState<PanicBreakdown | null>(null);
  const [currentHint, setCurrentHint] = useState<{ question: string; guidance: string } | null>(null);
  const [hintLevel, setHintLevel] = useState<number>(1);
  const [loading, setLoading] = useState<boolean>(false);
  const [completedSteps, setCompletedSteps] = useState<number[]>([]);

  // Generation inputs
  const [region, setRegion] = useState(initialRegion);
  const [crisisType, setCrisisType] = useState("Diplomatic & Border Security");
  const [difficulty, setDifficulty] = useState("Intermediate");

  useEffect(() => {
    handleGenerateNewScenario();
  }, []);

  const handleGenerateNewScenario = async () => {
    setLoading(true);
    setFeedback(null);
    setCurrentStep(1);
    setCompletedSteps([]);
    try {
      const scen = await generateCrisis({ region, crisis_type: crisisType, difficulty });
      setScenario(scen);
    } catch (err) {
      console.error("Failed to generate scenario:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerSubmit = async () => {
    if (!scenario || !userAnswer.trim()) return;
    setLoading(true);
    try {
      const res = await submitTrainStep({
        scenario_id: scenario.scenario_id,
        current_step: currentStep,
        user_answer: userAnswer,
      });
      setFeedback(res);
      if (res.did_pass && !completedSteps.includes(currentStep)) {
        setCompletedSteps([...completedSteps, currentStep]);
      }
    } catch (err) {
      console.error("Step submission error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleNextStep = () => {
    if (currentStep < 14) {
      setCurrentStep(currentStep + 1);
      setUserAnswer("");
      setFeedback(null);
      setCurrentHint(null);
    }
  };

  const handleTriggerPanic = async () => {
    if (!scenario) return;
    setLoading(true);
    try {
      const panic = await triggerPanicBreakdown(scenario.scenario_id);
      setPanicModal(panic);
    } catch (err) {
      console.error("Panic trigger error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleRequestHint = async () => {
    try {
      const hint = await fetchHint(hintLevel);
      setCurrentHint(hint);
      setHintLevel(hintLevel < 6 ? hintLevel + 1 : 1);
    } catch (err) {
      console.error("Hint fetch error:", err);
    }
  };

  return (
    <div className="max-w-[1720px] mx-auto p-4 space-y-4">
      {/* Banner */}
      <div className="bg-amber-950/40 border border-amber-900/60 p-3 rounded-lg flex items-center justify-between text-xs font-mono">
        <div className="flex items-center space-x-2 text-amber-300">
          <Award className="w-4 h-4 text-amber-400" />
          <span className="font-bold tracking-wider">MODE B: CRISIS TRAINER // FRANCE 14-STEP DECISION FRAMEWORK</span>
        </div>
        <div className="flex items-center space-x-3">
          <button
            onClick={handleTriggerPanic}
            className="bg-red-600 hover:bg-red-500 text-white font-bold px-3 py-1 rounded shadow-glow-blue flex items-center space-x-1.5 animate-pulse"
          >
            <AlertOctagon className="w-3.5 h-3.5" />
            <span>I DON'T KNOW WHAT TO DO</span>
          </button>
          <button
            onClick={handleRequestHint}
            className="bg-blue-900/80 hover:bg-blue-800 text-cyan-300 border border-cyan-500/40 px-3 py-1 rounded flex items-center space-x-1"
          >
            <Lightbulb className="w-3.5 h-3.5" />
            <span>HINT ({hintLevel}/6)</span>
          </button>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        {/* Left: 14-Step Framework Navigation & Scenario Controls */}
        <div className="lg:col-span-4 space-y-4">
          {/* Scenario Generator Controls */}
          <div className="command-card p-3 rounded-xl border border-slate-800 space-y-2 text-xs font-mono">
            <div className="text-cyan-400 font-bold border-b border-slate-800 pb-2">CRISIS PARAMETERS</div>
            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="text-slate-400 text-[10px]">REGION</label>
                <select
                  value={region}
                  onChange={(e) => setRegion(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded p-1 text-slate-200 mt-0.5"
                >
                  <option>Middle East</option>
                  <option>Eastern Europe</option>
                  <option>Sub-Saharan Africa</option>
                  <option>Indo-Pacific</option>
                  <option>Horn of Africa</option>
                </select>
              </div>
              <div>
                <label className="text-slate-400 text-[10px]">DIFFICULTY</label>
                <select
                  value={difficulty}
                  onChange={(e) => setDifficulty(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded p-1 text-slate-200 mt-0.5"
                >
                  <option>Beginner</option>
                  <option>Intermediate</option>
                  <option>Advanced</option>
                  <option>Chair Pressure</option>
                </select>
              </div>
            </div>
            <button
              onClick={handleGenerateNewScenario}
              disabled={loading}
              className="w-full bg-slate-800 hover:bg-slate-700 border border-slate-600 text-cyan-300 py-1.5 rounded transition flex items-center justify-center space-x-1.5"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
              <span>GENERATE NEW TRAINING SCENARIO</span>
            </button>
          </div>

          {/* 14 Framework Steps Checklist */}
          <div className="command-card p-3 rounded-xl border border-slate-800 space-y-2 text-xs font-mono">
            <div className="flex justify-between items-center border-b border-slate-800 pb-2 text-slate-300">
              <span className="font-bold text-cyan-400">DECISION FRAMEWORK</span>
              <span>{completedSteps.length}/14 COMPLETE</span>
            </div>
            <div className="space-y-1 max-h-[380px] overflow-y-auto pr-1">
              {FRAMEWORK_STEPS.map((stepTitle, idx) => {
                const stepNum = idx + 1;
                const isCurrent = currentStep === stepNum;
                const isDone = completedSteps.includes(stepNum);
                return (
                  <button
                    key={idx}
                    onClick={() => {
                      setCurrentStep(stepNum);
                      setFeedback(null);
                    }}
                    className={`w-full text-left p-2 rounded flex items-center justify-between text-[11px] transition ${
                      isCurrent
                        ? 'bg-blue-900/60 border border-cyan-400 text-cyan-200 font-bold'
                        : isDone
                        ? 'bg-emerald-950/40 text-emerald-300 border border-emerald-900/40'
                        : 'bg-slate-900/60 text-slate-400 hover:bg-slate-800'
                    }`}
                  >
                    <span>{stepTitle}</span>
                    {isDone ? (
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    ) : (
                      <ChevronRight className="w-3.5 h-3.5 text-slate-600" />
                    )}
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Right: Active Step Workspace & Scenario Brief */}
        <div className="lg:col-span-8 space-y-4">
          {scenario && (
            <div className="command-card p-4 rounded-xl border border-slate-800 space-y-3">
              {/* Scenario Header */}
              <div className="flex justify-between items-start border-b border-slate-800 pb-2">
                <div>
                  <span className="text-[10px] font-mono text-cyan-400 font-bold uppercase tracking-wider">
                    TRAINING CRISIS // {scenario.region} // {scenario.difficulty}
                  </span>
                  <h2 className="text-base font-bold text-white">{scenario.title}</h2>
                </div>
                <button
                  onClick={() => onAdvanceToPractice(scenario.scenario_id)}
                  className="bg-amber-600 hover:bg-amber-500 text-slate-950 text-xs font-mono font-bold px-3 py-1.5 rounded transition flex items-center space-x-1"
                >
                  <span>TEST IN ARENA</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>

              {/* Verified Facts & Background */}
              <div className="p-3 rounded bg-slate-900/90 border border-slate-800 text-xs space-y-2">
                <p className="text-slate-300 leading-relaxed">{scenario.initial_situation}</p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2 pt-2 border-t border-slate-800/80 text-[11px] font-mono">
                  <div className="text-cyan-300">
                    <span className="font-bold text-slate-400">FRANCE CORE INTEREST:</span> {scenario.france_interest}
                  </div>
                  <div className="text-red-300">
                    <span className="font-bold text-slate-400">IMMEDIATE THREAT:</span> {scenario.france_immediate_threat}
                  </div>
                </div>
              </div>

              {/* Progressive Hint Banner if triggered */}
              {currentHint && (
                <div className="p-3 rounded bg-blue-950/60 border border-cyan-500/40 text-xs font-mono space-y-1">
                  <div className="text-cyan-400 font-bold flex items-center space-x-1.5">
                    <Lightbulb className="w-3.5 h-3.5" />
                    <span>COACH HINT: {currentHint.question}</span>
                  </div>
                  <p className="text-slate-300 text-[11px]">{currentHint.guidance}</p>
                </div>
              )}

              {/* Interactive Training Step Card */}
              <div className="p-4 rounded-xl bg-slate-950/80 border border-cyan-500/50 space-y-3">
                <div className="flex items-center justify-between text-xs font-mono border-b border-slate-800 pb-2">
                  <span className="text-cyan-300 font-bold">
                    STEP {currentStep} OF 14: {FRAMEWORK_STEPS[currentStep - 1]}
                  </span>
                  <span className="text-slate-400">QUAI D'ORSAY INSTRUCTION ENGINE</span>
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs text-slate-300 font-medium">
                    Formulate France's assessment / diplomatic action for this step:
                  </label>
                  <textarea
                    rows={4}
                    value={userAnswer}
                    onChange={(e) => setUserAnswer(e.target.value)}
                    placeholder="Provide your diplomatic analysis, citing relevant UN Charter tools, country stakes, or France's red lines..."
                    className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-xs text-slate-200 outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 font-mono"
                  />
                </div>

                <div className="flex justify-between items-center pt-2">
                  <button
                    onClick={handleTriggerPanic}
                    className="text-xs font-mono text-red-400 hover:text-red-300 flex items-center space-x-1"
                  >
                    <HelpCircle className="w-3.5 h-3.5" />
                    <span>Confused? Open 3-Sentence Breakdown</span>
                  </button>

                  <button
                    onClick={handleAnswerSubmit}
                    disabled={loading || !userAnswer.trim()}
                    className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white text-xs font-mono font-bold px-4 py-2 rounded-lg transition flex items-center space-x-1.5 shadow-glow-blue"
                  >
                    <Send className="w-3.5 h-3.5" />
                    <span>SUBMIT FOR COACH EVALUATION</span>
                  </button>
                </div>
              </div>

              {/* Socratic Feedback Evaluation */}
              {feedback && (
                <div className="p-4 rounded-xl bg-slate-900/95 border border-emerald-500/50 space-y-2 text-xs font-mono">
                  <div className="flex items-center justify-between">
                    <span className="text-emerald-400 font-bold flex items-center space-x-1.5">
                      <CheckCircle2 className="w-4 h-4" />
                      <span>COACH APPRAISAL (SCORE: {feedback.score}/10)</span>
                    </span>
                    {feedback.did_pass && currentStep < 14 && (
                      <button
                        onClick={handleNextStep}
                        className="bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold px-3 py-1 rounded transition flex items-center space-x-1"
                      >
                        <span>ADVANCE TO STEP {currentStep + 1}</span>
                        <ChevronRight className="w-3.5 h-3.5" />
                      </button>
                    )}
                  </div>
                  <p className="text-slate-200">{feedback.user_evaluation}</p>
                  <div className="p-2.5 rounded bg-blue-950/40 border border-blue-900/60 text-slate-300 text-[11px] leading-relaxed">
                    <span className="text-cyan-400 font-bold">FRANCE DOCTRINE NOTE:</span> {feedback.france_doctrine_guidance}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Panic Modal: Section 17 "I DON'T KNOW WHAT TO DO" */}
      {panicModal && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="command-card max-w-2xl w-full p-6 rounded-2xl border border-red-500/60 space-y-4 shadow-2xl">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <div className="flex items-center space-x-2 text-red-400 font-mono font-bold">
                <AlertOctagon className="w-5 h-5" />
                <span>EMERGENCY PEDAGOGICAL BREAKDOWN</span>
              </div>
              <button onClick={() => setPanicModal(null)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* 3 Sentences */}
            <div className="space-y-1">
              <span className="text-[10px] font-mono text-cyan-400 font-bold">CRISIS IN 3 SENTENCES:</span>
              <p className="text-xs text-slate-200 leading-relaxed bg-slate-900 p-2.5 rounded border border-slate-800">
                {panicModal.crisis_in_3_sentences}
              </p>
            </div>

            {/* Stakes */}
            <div className="grid grid-cols-2 gap-3 text-xs font-mono">
              <div className="p-2.5 rounded bg-red-950/30 border border-red-900/50">
                <span className="text-red-400 font-bold">IMMEDIATE THREAT:</span>
                <p className="text-slate-300 mt-1">{panicModal.immediate_threat}</p>
              </div>
              <div className="p-2.5 rounded bg-blue-950/30 border border-blue-900/50">
                <span className="text-blue-400 font-bold">FRANCE'S CORE INTEREST:</span>
                <p className="text-slate-300 mt-1">{panicModal.france_core_interest}</p>
              </div>
            </div>

            {/* 3 Strategic Paths & Tradeoffs */}
            <div className="space-y-2 text-xs font-mono">
              <span className="text-[10px] text-cyan-400 font-bold">THREE STRATEGIC PATHWAYS:</span>
              <div className="space-y-2">
                {panicModal.three_strategic_paths.map((p, i) => (
                  <div key={i} className="p-2.5 rounded bg-slate-900 border border-slate-800 space-y-1">
                    <div className="text-amber-300 font-semibold">PATH {i+1}: {p.path}</div>
                    <div className="text-slate-400 text-[11px]"><span className="text-slate-500">TRADEOFF:</span> {p.tradeoff}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* One Decisive Question */}
            <div className="p-3 rounded-lg bg-cyan-950/40 border border-cyan-500/60 font-mono text-xs text-cyan-200">
              <span className="font-bold text-white">THE DECISIVE QUESTION FOR YOU:</span>
              <p className="mt-1 font-semibold">{panicModal.one_critical_question}</p>
            </div>

            <button
              onClick={() => setPanicModal(null)}
              className="w-full bg-blue-600 hover:bg-blue-500 text-white font-mono font-bold py-2 rounded-lg transition"
            >
              I HAVE CLARITY — RETURN TO DECISION
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
