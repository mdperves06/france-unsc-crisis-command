export interface UNSCMember {
  id: number;
  country_code: string;
  name: string;
  status: 'PERMANENT' | 'ELECTED';
  term_start: number;
  term_end?: number | null;
  region_group?: string;
  has_veto: boolean;
  strategic_profile?: {
    doctrine?: string;
  };
}

export interface UNSCPresidency {
  year: number;
  month: number;
  country_code: string;
  country_name: string;
  signature_theme?: string;
}

export interface UNSCResolution {
  id: number;
  resolution_number: string;
  code?: string;
  title: string;
  date_adopted: string;
  agenda_item: string;
  chapter_vii: boolean;
  operative_summary: string;
  full_text_url?: string;
  yes_votes: number;
  no_votes: number;
  abstentions: number;
  outcome: string;
  france_vote: string;
  source_url: string;
}

export interface UNSCVote {
  id: number;
  resolution_id?: number;
  draft_symbol?: string;
  meeting_number?: string;
  date: string;
  agenda_item?: string;
  country_code: string;
  vote: 'YES' | 'NO' | 'ABSTAIN' | 'ABSENT';
  is_veto: boolean;
  explanation_of_vote?: string;
  source: string;
}

export interface IntelligenceSource {
  id: number;
  source_id: string;
  title: string;
  publisher: string;
  source_type: string;
  url: string;
  publication_date: string;
  region: string;
  country?: string;
  topic: string;
  verification_status: 'VERIFIED FACT' | 'OFFICIAL STATEMENT' | 'REPORTED' | 'DISPUTED' | 'UNCONFIRMED' | 'ANALYSIS' | 'SIMULATION';
  confidence_score: number;
  summary: string;
}

export interface GlobalAlert {
  id: number;
  alert_type: string;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  headline: string;
  details: string;
  region: string;
  country_code?: string;
  source_url: string;
  timestamp: string;
  active: boolean;
}

export interface RegionCommandProfile {
  id: number;
  region_id: string;
  name: string;
  current_situation: string;
  france_historical_role: string;
  france_current_relevance: string;
  unsc_involvement_summary: string;
  escalation_risks: string[];
  deescalation_opportunities: string[];
  humanitarian_status?: string;
  economic_dimension?: string;
  legal_dimension?: string;
  major_actors: Array<{ name: string; role: string }>;
  key_resolutions: string[];
  coordinates: { lat: number; lng: number; zoom?: number };
}

export interface CrisisScenario {
  id: number;
  scenario_id: string;
  title: string;
  region: string;
  crisis_type: string;
  difficulty: string;
  initial_situation: string;
  location_details: string;
  coordinates: { lat: number; lng: number };
  background: string;
  known_facts: Array<{ fact: string; status: string; source?: string }>;
  unknown_facts: string[];
  key_actors: Array<{ code: string; name: string; role: string }>;
  france_interest: string;
  france_immediate_threat: string;
  france_objectives: string[];
  france_red_lines: string[];
  available_tools: string[];
  strategic_paths: Array<{ path: string; tradeoff: string }>;
  escalation_paths: string[];
  deescalation_paths: string[];
}

export interface WorldState {
  turn: number;
  crisis_level: number;
  escalation_level: number;
  diplomatic_tension: number;
  humanitarian_status: string;
  economic_status: string;
  france_reputation: number;
  france_credibility: number;
  country_states: Record<string, {
    stance: string;
    trust: number;
    coalition: string;
    demands: string[];
    latest_cable?: string;
  }>;
  coalition_status: {
    support: string[];
    conditional: string[];
    opposed: string[];
    undecided: string[];
  };
  projected_vote: {
    yes_estimate: number;
    no_estimate: number;
    abstain_estimate: number;
    p5_veto_threats: string[];
    outcome_prediction: string;
    label: string;
  };
  summary_of_turn?: string;
  timestamp: string;
}

export interface DiplomaticMessage {
  id: number;
  sender: string;
  recipient: string;
  message_type: string;
  content: string;
  turn: number;
  label: string;
  reaction_mood: string;
  timestamp: string;
}

export interface PanicBreakdown {
  crisis_in_3_sentences: string;
  immediate_threat: string;
  france_core_interest: string;
  top_3_actors_to_consider: string[];
  three_strategic_paths: Array<{ path: string; tradeoff: string }>;
  one_critical_question: string;
}

export interface CurriculumModule {
  id: number;
  module_number: number;
  title: string;
  category: string;
  description: string;
  core_doctrine: string;
  legal_basis: string;
  france_historical_cases: Array<{ case: string; notes: string }>;
  key_takeaways: string[];
  unlocked: boolean;
}

export interface CompetencyMetric {
  skill: string;
  score: number;
}
