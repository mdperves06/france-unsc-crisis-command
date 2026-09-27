from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class CrisisScenarioCreate(BaseModel):
    region: str
    conflict_type: Optional[str] = "Military"
    crisis_type: str = "Diplomatic"
    difficulty: str = "Intermediate"
    actors_count: Optional[int] = 5
    france_relevance: Optional[str] = "High"
    custom_prompt: Optional[str] = None

class CrisisScenarioSchema(BaseModel):
    id: int
    scenario_id: str
    title: str
    region: str
    crisis_type: str
    difficulty: str
    initial_situation: str
    location_details: str
    coordinates: Dict[str, float]
    background: str
    known_facts: List[Dict[str, str]]
    unknown_facts: List[str]
    key_actors: List[Dict[str, Any]]
    france_interest: str
    france_immediate_threat: str
    france_objectives: List[str]
    france_red_lines: List[str]
    available_tools: List[str]
    strategic_paths: List[Dict[str, str]]
    escalation_paths: List[str]
    deescalation_paths: List[str]
    is_custom_or_imported: bool

    model_config = {"from_attributes": True}

class CrisisTrainStepRequest(BaseModel):
    scenario_id: str
    current_step: int = Field(ge=1, le=14)  # 14-step France Decision Framework
    user_answer: str

class CrisisTrainStepResponse(BaseModel):
    step_number: int
    step_title: str
    user_evaluation: str
    score: float # 0-10
    did_pass: bool
    france_doctrine_guidance: str
    next_question: Optional[str]
    hint: Optional[str]
