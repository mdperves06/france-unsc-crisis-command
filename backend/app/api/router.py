from fastapi import APIRouter
from app.api.v1.unsc import router as unsc_router
from app.api.v1.intelligence import router as intelligence_router
from app.api.v1.crisis import router as crisis_router
from app.api.v1.practice import router as practice_router
from app.api.v1.training import router as training_router
from app.api.v1.research import router as research_router
from app.api.v1.chat import router as chat_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.auth import router as auth_router

api_router = APIRouter()
api_router.include_router(unsc_router)
api_router.include_router(intelligence_router)
api_router.include_router(crisis_router)
api_router.include_router(practice_router)
api_router.include_router(training_router)
api_router.include_router(research_router)
api_router.include_router(chat_router)
api_router.include_router(analytics_router)
api_router.include_router(auth_router)
