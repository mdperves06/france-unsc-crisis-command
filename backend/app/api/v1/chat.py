from typing import Dict, Any, List
from fastapi import APIRouter
from pydantic import BaseModel
from app.ai.agents.france_coach_agent import FranceStrategyCoach
from app.ai.agents.country_agent import UNSCCountrySimulationAgent
from app.schemas.ai import LLMMessage

router = APIRouter(prefix="/chat", tags=["AI Diplomat"])

class ChatRequest(BaseModel):
    prompt: str
    persona: str = "FRANCE_COACH" # FRANCE_COACH, RUSSIAN_DELEGATE, US_DELEGATE, HOSTILE_EB
    context: str = ""

@router.post("")
async def diplomatic_chat(req: ChatRequest):
    prompt = req.prompt.strip()
    persona = req.persona

    if persona == "RUSSIAN_DELEGATE":
        country_agent = UNSCCountrySimulationAgent()
        res = await country_agent.provider.generate([
            LLMMessage(role="system", content="You are the Permanent Representative of the Russian Federation to the UN Security Council. Respond firmly, emphasizing state sovereignty and multipolarity."),
            LLMMessage(role="user", content=prompt)
        ])
        return {"response": res.content, "persona": "Russian Federation", "source_type": "SIMULATION"}

    elif persona == "US_DELEGATE":
        country_agent = UNSCCountrySimulationAgent()
        res = await country_agent.provider.generate([
            LLMMessage(role="system", content="You are the US Ambassador to the UN Security Council. Coordinate with allies, maintain firm deterrence."),
            LLMMessage(role="user", content=prompt)
        ])
        return {"response": res.content, "persona": "United States", "source_type": "SIMULATION"}

    elif persona == "HOSTILE_EB":
        coach = FranceStrategyCoach()
        res = await coach.provider.generate([
            LLMMessage(role="system", content="You are a skeptical, sharp MUN Executive Board Director probing the French delegate's legal grounds, voting math, and implementation feasibility."),
            LLMMessage(role="user", content=prompt)
        ])
        return {"response": res.content, "persona": "EB Director", "source_type": "TRAINING SIMULATION"}

    else: # Default France Coach
        coach = FranceStrategyCoach()
        res = await coach.provider.generate([
            LLMMessage(role="system", content="You are the France Strategic Diplomatic Coach. Break down geopolitical issues clearly, explain country incentives, and teach trade-offs rather than one dogmatic answer."),
            LLMMessage(role="user", content=prompt)
        ])
        return {"response": res.content, "persona": "Quai d'Orsay Diplomatic Coach", "source_type": "PEDAGOGICAL ANALYSIS"}
