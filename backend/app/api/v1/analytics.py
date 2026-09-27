from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.training_service import TrainingService

router = APIRouter(prefix="/analytics", tags=["Performance & Learning Analytics"])

@router.get("/metrics")
def get_analytics_metrics(user_id: str = "default_delegate", db: Session = Depends(get_db)):
    profile = TrainingService.get_user_profile(db, user_id=user_id)
    return {
        "competencies": [
            {"skill": "Crisis Analysis", "score": profile.crisis_analysis},
            {"skill": "Strategic Reasoning", "score": profile.strategic_reasoning},
            {"skill": "France Interest ID", "score": profile.france_interest_id},
            {"skill": "Diplomacy", "score": profile.diplomacy},
            {"skill": "Negotiation", "score": profile.negotiation},
            {"skill": "Coalition Building", "score": profile.coalition_building},
            {"skill": "Response Speed", "score": profile.response_speed},
            {"skill": "Evidence Use", "score": profile.evidence_use},
            {"skill": "Legal Awareness", "score": profile.legal_awareness},
            {"skill": "Resolution Writing", "score": profile.resolution_writing},
            {"skill": "Speech Delivery", "score": profile.speech_delivery},
            {"skill": "Rebuttal Strength", "score": profile.rebuttal_strength},
            {"skill": "Adaptability", "score": profile.adaptability},
            {"skill": "Contingency Planning", "score": profile.contingency_planning},
            {"skill": "Portfolio Awareness", "score": profile.portfolio_awareness},
            {"skill": "Decision Consistency", "score": profile.decision_consistency}
        ],
        "strong_areas": profile.strong_areas,
        "weak_areas": profile.weak_areas,
        "frequently_missed_actors": profile.frequently_missed_actors,
        "frequently_missed_risks": profile.frequently_missed_risks,
        "recommended_next_focus": profile.recommended_next_focus,
        "completed_scenarios_count": profile.completed_scenarios_count
    }
