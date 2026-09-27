from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class CurriculumModuleSchema(BaseModel):
    id: int
    module_number: int
    title: str
    category: str
    description: str
    core_doctrine: str
    legal_basis: str
    france_historical_cases: List[Dict[str, str]]
    key_takeaways: List[str]
    sources: List[Dict[str, str]]
    unlocked: bool

    model_config = {"from_attributes": True}

class LearningProfileSchema(BaseModel):
    user_id: str
    crisis_analysis: float
    strategic_reasoning: float
    france_interest_id: float
    diplomacy: float
    negotiation: float
    coalition_building: float
    response_speed: float
    evidence_use: float
    legal_awareness: float
    resolution_writing: float
    speech_delivery: float
    rebuttal_strength: float
    adaptability: float
    contingency_planning: float
    portfolio_awareness: float
    decision_consistency: float
    strong_areas: List[str]
    weak_areas: List[str]
    frequently_missed_actors: List[str]
    frequently_missed_risks: List[str]
    common_mistakes: List[str]
    recommended_next_focus: str
    completed_scenarios_count: int
    updated_at: datetime

    model_config = {"from_attributes": True}

class SpeechAnalysisRequest(BaseModel):
    speech_type: str # OPENING, MOD_CAUCUS, CRISIS_SPEECH, PRESS_STMT, EMERGENCY
    speech_text: str
    agenda_topic: Optional[str] = "Maintenance of International Peace and Security"
    target_coalition: Optional[str] = "EU and African Group"

class ResolutionValidationRequest(BaseModel):
    document_type: str = "DRAFT_RESOLUTION"
    title: str
    preambulatory_clauses: List[str]
    operative_clauses: List[str]
    sponsors: List[str] = Field(default_factory=lambda: ["France"])
    signatories: List[str] = Field(default_factory=list)

class EBQuestionRequest(BaseModel):
    scenario_context: str
    france_stated_position: str
    difficulty: Optional[str] = "Aggressive"

class EBEvaluationRequest(BaseModel):
    scenario_context: str
    eb_question: str
    france_answer: str
