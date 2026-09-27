import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, SessionLocal, Base
from app.api.router import api_router

# Import all models to ensure table discovery
import app.models
from app.data.seed_unsc import seed_unsc_data
from app.data.seed_intelligence import seed_intelligence_data
from app.data.seed_curriculum import seed_curriculum_data
from app.services.crisis_engine import CrisisEngineService
from app.schemas.crisis import CrisisScenarioCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("france_unsc_command")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables and seed database
    logger.info("Initializing France UNSC Crisis Command Database...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        seed_unsc_data(db)
        seed_intelligence_data(db)
        seed_curriculum_data(db)

        # Seed default admin user
        from app.services.auth_service import AuthService
        AuthService().seed_default_admin(db)
        
        # Check if benchmark scenario exists, if not seed one
        from app.models.crisis import CrisisScenario
        if not db.query(CrisisScenario).first():
            engine_svc = CrisisEngineService()
            engine_svc.generate_scenario(db, CrisisScenarioCreate(
                region="Middle East",
                conflict_type="Military",
                crisis_type="Diplomatic & Border Security",
                difficulty="Intermediate"
            ))
            logger.info("Seeded initial benchmark crisis scenario.")
        logger.info("Database initialization and seed complete.")
    finally:
        db.close()

    yield
    logger.info("Shutting down France UNSC Crisis Command...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="France-Centric AI-Powered UNSC Intelligence, Training, Strategy Game, Diplomacy Simulator and Crisis Practice Arena.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "command_center": "RÉPUBLIQUE FRANÇAISE — MISSION PERMANENTE AUPRÈS DES NATIONS UNIES",
        "system": settings.PROJECT_NAME,
        "status": "OPERATIONAL",
        "role": "Permanent Member of the UN Security Council (France)",
        "docs_url": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "ok", "ai_mode": settings.AI_MODE}
