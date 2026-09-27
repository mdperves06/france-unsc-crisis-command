from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.crisis import CrisisScenario
from app.schemas.crisis import CrisisScenarioCreate, CrisisScenarioSchema, CrisisTrainStepRequest, CrisisTrainStepResponse
from app.services.crisis_engine import CrisisEngineService
from app.ai.agents.france_coach_agent import FranceStrategyCoach
from app.schemas.ai import PanicBreakdown

router = APIRouter(prefix="/crisis", tags=["Crisis Engine & Trainer"])
crisis_service = CrisisEngineService()
coach_agent = FranceStrategyCoach()

@router.post("/generate", response_model=CrisisScenarioSchema)
def generate_crisis_scenario(req: CrisisScenarioCreate, db: Session = Depends(get_db)):
    return crisis_service.generate_scenario(db, req)

@router.get("/{scenario_id}", response_model=CrisisScenarioSchema)
def get_crisis_scenario(scenario_id: str, db: Session = Depends(get_db)):
    scenario = db.query(CrisisScenario).filter(CrisisScenario.scenario_id == scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario

@router.post("/train-step", response_model=CrisisTrainStepResponse)
def train_step(req: CrisisTrainStepRequest, db: Session = Depends(get_db)):
    scenario = db.query(CrisisScenario).filter(CrisisScenario.scenario_id == req.scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return crisis_service.evaluate_training_step(req.current_step, req.user_answer, scenario)

@router.post("/panic", response_model=PanicBreakdown)
async def emergency_panic_breakdown(scenario_id: str, db: Session = Depends(get_db)):
    """Section 17 'I DON'T KNOW WHAT TO DO' Emergency breakdown."""
    scenario = db.query(CrisisScenario).filter(CrisisScenario.scenario_id == scenario_id).first()
    if not scenario:
        # Provide default crisis context
        return await coach_agent.get_panic_breakdown(
            crisis_title="Maritime & Border Security Confrontation",
            crisis_summary="Hostilities have flared along the buffer corridor. Civilians are trapped and opposing military forces are mobilizing.",
            actors=["USA", "Russia", "China", "Algeria"]
        )
    return await coach_agent.get_panic_breakdown(
        crisis_title=scenario.title,
        crisis_summary=scenario.initial_situation,
        actors=[a.get("code", "ACTOR") for a in scenario.key_actors]
    )

@router.get("/hints/{level}")
def get_progressive_hint(level: int):
    """Section 18 Progressive Hint System (Hints 1 to 6)."""
    return coach_agent.get_progressive_hint(hint_level=level, crisis_context={})
