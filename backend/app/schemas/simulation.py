from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class StartPracticeRequest(BaseModel):
    scenario_id: str
    difficulty: Optional[str] = "Intermediate"
    year: Optional[int] = 2026

class PracticeActionRequest(BaseModel):
    session_id: str
    action_type: str # e.g. CONTACT_USA, REQUEST_EMERGENCY_MEETING, DRAFT_RESOLUTION, THREATEN_VETO, PROPOSE_CEASEFIRE
    target_country: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    rationale: Optional[str] = None

class NegotiateMessageRequest(BaseModel):
    session_id: str
    recipient_country: str # USA, GBR, RUS, CHN, or Elected member code
    content: str
    proposals: List[str] = Field(default_factory=list)
    concessions: List[str] = Field(default_factory=list)

class DiplomaticMessageSchema(BaseModel):
    id: int
    sender: str
    recipient: str
    message_type: str
    content: str
    turn: int
    label: str
    reaction_mood: str
    timestamp: datetime

    class Config:
        from_attributes = True

class SimulationWorldStateSchema(BaseModel):
    turn: int
    crisis_level: int
    escalation_level: int
    diplomatic_tension: int
    humanitarian_status: str
    economic_status: str
    france_reputation: int
    france_credibility: int
    country_states: Dict[str, Any]
    coalition_status: Dict[str, List[str]]
    projected_vote: Dict[str, Any]
    france_promises: List[Dict[str, Any]]
    france_concessions: List[Dict[str, Any]]
    draft_resolution_on_table: Dict[str, Any]
    summary_of_turn: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True

class WhatIfBranchRequest(BaseModel):
    source_session_id: str
    target_turn: int
    alternative_action_type: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    notes: Optional[str] = None
