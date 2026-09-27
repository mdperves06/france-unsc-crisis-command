import logging
import secrets
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings

# backend/ directory — .env and relative SQLite paths resolve here regardless of CWD
BACKEND_DIR = Path(__file__).resolve().parents[2]
DEFAULT_SECRET_KEY = "france-unsc-secret-key-change-in-production-mun-defense"

class Settings(BaseSettings):
    PROJECT_NAME: str = "FRANCE UNSC CRISIS COMMAND"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = DEFAULT_SECRET_KEY
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    DATABASE_URL: str = "sqlite:///./france_unsc_crisis.db"
    
    # AI System Configuration
    # AI Modes: "LOCAL", "CLOUD", "HYBRID"
    AI_MODE: str = "HYBRID"
    
    # Model assignments for the 4 Specialist Agents
    AGENT_RESEARCH_PROVIDER: str = "gemini"  # gemini, claude, openai, local
    AGENT_RESEARCH_MODEL: str = "gemini-3.8-flash"
    
    AGENT_COUNTRY_PROVIDER: str = "local"    # local, gemini, claude, openai
    AGENT_COUNTRY_MODEL: str = "llama3"
    
    AGENT_COACH_PROVIDER: str = "gemini"     # gemini, claude, openai, local
    AGENT_COACH_MODEL: str = "gemini-3.8-flash"
    
    AGENT_ORCHESTRATOR_PROVIDER: str = "gemini"
    AGENT_ORCHESTRATOR_MODEL: str = "gemini-3.8-flash"
    
    # API Keys & Local Endpoints (Never exposed to frontend)
    GEMINI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    
    LOCAL_AI_BASE_URL: str = "http://localhost:11434"  # Default Ollama
    LOCAL_AI_MODEL: str = "llama3"
    LOCAL_AI_CONTEXT_WINDOW: int = 8192
    LOCAL_AI_TEMPERATURE: float = 0.4
    LOCAL_AI_MAX_TOKENS: int = 4096
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    class Config:
        case_sensitive = True
        env_file = BACKEND_DIR / ".env"
        extra = "allow"

settings = Settings()

if settings.DATABASE_URL.startswith("sqlite:///./"):
    settings.DATABASE_URL = "sqlite:///" + (BACKEND_DIR / settings.DATABASE_URL[len("sqlite:///./"):]).as_posix()

# Treat template placeholders (e.g. "YOUR_GOOGLE_API_KEY_HERE") as unset so providers use offline mode
for _key in ("GEMINI_API_KEY", "ANTHROPIC_API_KEY", "OPENAI_API_KEY"):
    if (getattr(settings, _key) or "").upper().startswith("YOUR_"):
        setattr(settings, _key, None)

if not settings.SECRET_KEY or settings.SECRET_KEY == DEFAULT_SECRET_KEY:
    # Never sign tokens with a public key; a per-process key means logins reset on restart
    settings.SECRET_KEY = secrets.token_urlsafe(48)
    logging.getLogger(__name__).warning(
        "SECRET_KEY not set in backend/.env — using a temporary random key (logins will not survive restarts)."
    )
