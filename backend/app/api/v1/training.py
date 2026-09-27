from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.training import (
    CurriculumModuleSchema,
    LearningProfileSchema,
    SpeechAnalysisRequest,
    ResolutionValidationRequest,
    EBQuestionRequest,
    EBEvaluationRequest
)
from app.services.training_service import TrainingService

router = APIRouter(prefix="/training", tags=["Training Academy & Labs"])
training_service = TrainingService()

@router.get("/curriculum", response_model=List[CurriculumModuleSchema])
def get_curriculum(db: Session = Depends(get_db)):
    return training_service.get_curriculum(db)

@router.get("/profile", response_model=LearningProfileSchema)
def get_learning_profile(db: Session = Depends(get_db)):
    return training_service.get_user_profile(db)

@router.post("/speech/analyze")
async def analyze_speech(req: SpeechAnalysisRequest, db: Session = Depends(get_db)):
    return await training_service.analyze_speech(db, req)

@router.post("/resolution/validate")
async def validate_resolution(req: ResolutionValidationRequest, db: Session = Depends(get_db)):
    return await training_service.validate_resolution(db, req)

@router.post("/eb/question")
async def get_eb_question(req: EBQuestionRequest):
    return await training_service.generate_eb_question(req)

@router.post("/eb/evaluate")
async def evaluate_eb_answer(req: EBEvaluationRequest):
    return await training_service.evaluate_eb_answer(req)
