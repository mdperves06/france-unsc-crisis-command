from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class LLMMessage(BaseModel):
    role: str # "system", "user", "assistant"
    content: str

class LLMResponse(BaseModel):
    content: str
    provider: str
    model: str
    usage: Optional[Dict[str, Any]] = None

class CountryReactionOutput(BaseModel):
    country_code: str
    country_name: str
    current_stance: str # SUPPORTIVE, CONDITIONAL, CAUTIOUS, CRITICAL, OPPOSING
    objective: str
    demands: List[str] = Field(default_factory=list)
    red_lines: List[str] = Field(default_factory=list)
    preferred_outcome: str
    will_support: bool = False
    conditional_support: bool = False
    will_oppose: bool = False
    possible_concession: Optional[str] = None
    reaction_to_france: str
    diplomatic_cable_response: str
    likely_next_action: str
    confidence: float = 0.85
    reasoning_summary: str
    is_simulation: bool = True

class FranceCoachAdvice(BaseModel):
    what_is_happening: str
    what_france_wants: str
    why_france_cares: str
    what_france_can_do: List[str] = Field(default_factory=list)
    who_matters: List[str] = Field(default_factory=list)
    who_can_block: List[str] = Field(default_factory=list)
    what_france_can_offer: List[str] = Field(default_factory=list)
    what_france_should_ask: List[str] = Field(default_factory=list)
    main_risks: List[str] = Field(default_factory=list)
    backup_options: List[str] = Field(default_factory=list)
    suggested_diplomatic_language: str
    recommended_action: str

class PanicBreakdown(BaseModel):
    """Section 17 'I Don't Know What To Do' Emergency Breakdown"""
    crisis_in_3_sentences: str
    immediate_threat: str
    france_core_interest: str
    top_3_actors_to_consider: List[str]
    three_strategic_paths: List[Dict[str, str]] # [{"path": "...", "tradeoff": "..."}]
    one_critical_question: str
