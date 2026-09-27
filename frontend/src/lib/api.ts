const API_BASE = "http://localhost:8000/api/v1";

// ── Token Storage ─────────────────────────────────────────────
export function getToken(): string | null {
  return localStorage.getItem("unsc_token");
}

export function setToken(token: string): void {
  localStorage.setItem("unsc_token", token);
}

export function clearToken(): void {
  localStorage.removeItem("unsc_token");
  localStorage.removeItem("unsc_user");
}

export function getStoredUser(): any | null {
  const raw = localStorage.getItem("unsc_user");
  return raw ? JSON.parse(raw) : null;
}

export function storeUser(user: any): void {
  localStorage.setItem("unsc_user", JSON.stringify(user));
}

export function getAuthHeaders(): Record<string, string> {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

// ── Auth API ──────────────────────────────────────────────────
export async function authLogin(email: string, password: string) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Login failed");
  }
  const data = await res.json();
  setToken(data.access_token);
  storeUser(data.user);
  return data;
}

export async function authRegister(payload: {
  email: string;
  username: string;
  full_name: string;
  password: string;
  country_assignment?: string;
}) {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Registration failed");
  }
  const data = await res.json();
  setToken(data.access_token);
  storeUser(data.user);
  return data;
}

export async function authGetMe() {
  const res = await fetch(`${API_BASE}/auth/me`, {
    headers: getAuthHeaders(),
  });
  if (!res.ok) throw new Error("Not authenticated");
  return res.json();
}

export async function authStatus() {
  const res = await fetch(`${API_BASE}/auth/status`, {
    headers: getAuthHeaders(),
  });
  return res.json();
}

export function authLogout(): void {
  clearToken();
}



export async function fetchUNSCMembers(year: number = 2026) {
  const res = await fetch(`${API_BASE}/unsc/members?year=${year}`);
  return res.json();
}

export async function fetchUNSCPresidencies(year: number = 2026) {
  const res = await fetch(`${API_BASE}/unsc/presidencies?year=${year}`);
  return res.json();
}

export async function fetchUNSCResolutions() {
  const res = await fetch(`${API_BASE}/unsc/resolutions`);
  return res.json();
}

export async function fetchUNSCVotes() {
  const res = await fetch(`${API_BASE}/unsc/votes`);
  return res.json();
}

export async function fetchIntelligenceSources(region?: string) {
  const url = region ? `${API_BASE}/intelligence/sources?region=${encodeURIComponent(region)}` : `${API_BASE}/intelligence/sources`;
  const res = await fetch(url);
  return res.json();
}

export async function fetchGlobalAlerts() {
  const res = await fetch(`${API_BASE}/intelligence/alerts`);
  return res.json();
}

export async function fetchRegions() {
  const res = await fetch(`${API_BASE}/intelligence/regions`);
  return res.json();
}

export async function fetchRegionProfile(regionId: string) {
  const res = await fetch(`${API_BASE}/intelligence/regions/${regionId}`);
  if (!res.ok) throw new Error(`Region '${regionId}' not found`);
  return res.json();
}

export async function generateCrisis(params: {
  region: string;
  crisis_type: string;
  difficulty: string;
}) {
  const res = await fetch(`${API_BASE}/crisis/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });
  return res.json();
}

export async function submitTrainStep(params: {
  scenario_id: string;
  current_step: number;
  user_answer: string;
}) {
  const res = await fetch(`${API_BASE}/crisis/train-step`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });
  return res.json();
}

export async function triggerPanicBreakdown(scenarioId: string) {
  const res = await fetch(`${API_BASE}/crisis/panic?scenario_id=${scenarioId}`, {
    method: "POST",
  });
  return res.json();
}

export async function fetchHint(level: number) {
  const res = await fetch(`${API_BASE}/crisis/hints/${level}`);
  return res.json();
}

export async function startPracticeSession(scenarioId: string, difficulty: string = "Intermediate") {
  const res = await fetch(`${API_BASE}/practice/start`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ scenario_id: scenarioId, difficulty }),
  });
  return res.json();
}

export async function executePracticeAction(params: {
  session_id: string;
  action_type: string;
  target_country?: string;
  parameters?: any;
  rationale?: string;
}) {
  const res = await fetch(`${API_BASE}/practice/action`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });
  return res.json();
}

export async function sendNegotiateMessage(params: {
  session_id: string;
  recipient_country: string;
  content: string;
}) {
  const res = await fetch(`${API_BASE}/practice/negotiate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });
  return res.json();
}

export async function fetchWorldState(sessionId: string) {
  const res = await fetch(`${API_BASE}/practice/${sessionId}/world-state`);
  return res.json();
}

export async function fetchMessages(sessionId: string) {
  const res = await fetch(`${API_BASE}/practice/${sessionId}/messages`);
  return res.json();
}

export async function fetchTimeline(sessionId: string) {
  const res = await fetch(`${API_BASE}/practice/${sessionId}/timeline`);
  return res.json();
}

export async function triggerAfterActionReview(sessionId: string) {
  const res = await fetch(`${API_BASE}/practice/${sessionId}/aar`, {
    method: "POST",
  });
  return res.json();
}

export async function fetchCurriculum() {
  const res = await fetch(`${API_BASE}/training/curriculum`);
  return res.json();
}

export async function fetchAnalytics() {
  const res = await fetch(`${API_BASE}/analytics/metrics`);
  return res.json();
}

export async function analyzeSpeech(speechType: string, speechText: string) {
  const res = await fetch(`${API_BASE}/training/speech/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ speech_type: speechType, speech_text: speechText }),
  });
  return res.json();
}

export async function validateResolution(title: string, preambles: string[], operatives: string[]) {
  const res = await fetch(`${API_BASE}/training/resolution/validate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title,
      preambulatory_clauses: preambles,
      operative_clauses: operatives,
    }),
  });
  return res.json();
}

export async function askAIDiplomat(prompt: string, persona: string = "FRANCE_COACH") {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt, persona }),
  });
  return res.json();
}

export async function askEBQuestion(scenarioContext: string, position: string) {
  const res = await fetch(`${API_BASE}/training/eb/question`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ scenario_context: scenarioContext, france_stated_position: position }),
  });
  return res.json();
}

export async function evaluateEBAnswer(context: string, question: string, answer: string) {
  const res = await fetch(`${API_BASE}/training/eb/evaluate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ scenario_context: context, eb_question: question, france_answer: answer }),
  });
  return res.json();
}
