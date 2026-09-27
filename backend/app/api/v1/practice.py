from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.simulation import SimulationSession, SimulationWorldState, DiplomaticMessage, SimulationActionLog
from app.models.crisis import CrisisScenario
from app.schemas.simulation import (
    StartPracticeRequest,
    PracticeActionRequest,
    NegotiateMessageRequest,
    DiplomaticMessageSchema,
    SimulationWorldStateSchema,
    WhatIfBranchRequest
)
from app.services.simulation_service import SimulationService

router = APIRouter(prefix="/practice", tags=["Crisis Arena Practice"])
simulation_service = SimulationService()

@router.post("/start")
def start_practice(req: StartPracticeRequest, db: Session = Depends(get_db)):
    try:
        session = simulation_service.start_session(
            db,
            scenario_id=req.scenario_id,
            difficulty=req.difficulty or "Intermediate",
            year=req.year or 2026
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"session_id": session.session_id, "turn": session.current_turn, "status": session.status}

@router.post("/action")
async def execute_action(req: PracticeActionRequest, db: Session = Depends(get_db)):
    action_dict = {
        "action_type": req.action_type,
        "target_country": req.target_country,
        "parameters": req.parameters,
        "rationale": req.rationale
    }
    try:
        return await simulation_service.execute_action(db, session_id=req.session_id, action_data=action_dict)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/negotiate")
def send_negotiation_message(req: NegotiateMessageRequest, db: Session = Depends(get_db)):
    try:
        msg = simulation_service.send_bilateral_message(
            db,
            session_id=req.session_id,
            recipient=req.recipient_country,
            content=req.content
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message_id": msg.id, "sender": msg.sender, "recipient": msg.recipient, "content": msg.content}

@router.get("/{session_id}/world-state", response_model=SimulationWorldStateSchema)
def get_world_state(session_id: str, db: Session = Depends(get_db)):
    state = db.query(SimulationWorldState).filter(
        SimulationWorldState.session_id == session_id
    ).order_by(SimulationWorldState.turn.desc()).first()
    if not state:
        raise HTTPException(status_code=404, detail="World state not found for this session")
    return state

@router.get("/{session_id}/messages", response_model=List[DiplomaticMessageSchema])
def get_messages(session_id: str, db: Session = Depends(get_db)):
    return db.query(DiplomaticMessage).filter(
        DiplomaticMessage.session_id == session_id
    ).order_by(DiplomaticMessage.id.asc()).all()

@router.get("/{session_id}/timeline")
def get_timeline(session_id: str, db: Session = Depends(get_db)):
    actions = db.query(SimulationActionLog).filter(
        SimulationActionLog.session_id == session_id
    ).order_by(SimulationActionLog.turn.asc()).all()
    return [{
        "turn": a.turn,
        "action_type": a.action_type,
        "authority_status": a.authority_status,
        "authority_rationale": a.authority_rationale,
        "outcome_summary": a.outcome_summary,
        "timestamp": a.timestamp
    } for a in actions]

@router.post("/what-if")
def create_what_if_branch(req: WhatIfBranchRequest, db: Session = Depends(get_db)):
    try:
        branch = simulation_service.create_what_if_branch(
            db,
            source_session_id=req.source_session_id,
            target_turn=req.target_turn,
            alt_action=req.alternative_action_type
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"branch_session_id": branch.session_id, "parent_session_id": branch.parent_session_id, "turn": branch.current_turn}

@router.post("/{session_id}/aar")
async def generate_after_action_review(session_id: str, db: Session = Depends(get_db)):
    session = db.query(SimulationSession).filter(SimulationSession.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    scenario = db.query(CrisisScenario).filter(CrisisScenario.scenario_id == session.scenario_id).first()
    scenario_dict = {"title": scenario.title if scenario else "UNSC Crisis", "difficulty": session.difficulty}
    
    final_state = db.query(SimulationWorldState).filter(
        SimulationWorldState.session_id == session_id
    ).order_by(SimulationWorldState.turn.desc()).first()
    
    final_state_dict = {
        "france_reputation": final_state.france_reputation if final_state else 75,
        "escalation_level": final_state.escalation_level if final_state else 50,
        "projected_vote": final_state.projected_vote if final_state else {}
    }

    actions = db.query(SimulationActionLog).filter(SimulationActionLog.session_id == session_id).all()
    action_dicts = [{"action_type": a.action_type} for a in actions]

    return await simulation_service.orchestrator.generate_after_action_review(
        session_id=session_id,
        scenario=scenario_dict,
        final_state=final_state_dict,
        action_history=action_dicts
    )
