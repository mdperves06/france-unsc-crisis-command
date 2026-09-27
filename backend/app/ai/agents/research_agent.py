import logging
from typing import List, Dict, Any, Optional
from app.ai.agents.base_agent import BaseAgent
from app.schemas.ai import LLMMessage

logger = logging.getLogger(__name__)

class GlobalResearchAgent(BaseAgent):
    """
    AGENT 1 — GLOBAL RESEARCH AGENT
    Responsibilities:
    - Real-world research & source discovery
    - Source provenance & validation
    - Timeline building
    - UNSC data retrieval & precedent analysis
    """
    def __init__(self):
        super().__init__(agent_name="Global Research Agent", agent_type="research")

    async def analyze_precedent(self, crisis_type: str, region: str) -> Dict[str, Any]:
        """Find historical UNSC precedents, relevant Chapter VII resolutions, and France's past stance."""
        prompt = f"""
You are the Global Research Agent for the France UNSC Crisis Command.
Task: Identify historical UN Security Council precedents, key resolutions, and France's historical doctrine for:
Region: {region}
Crisis Type: {crisis_type}

Provide:
1. Relevant historical UNSC resolutions (exact numbers if known, e.g. S/RES/1973, S/RES/2254, S/RES/1701).
2. France's established legal and diplomatic position on this type of conflict.
3. Common voting patterns (P5 alignments, typical abstentions).
4. Sourced legal principles (UN Charter Chapter VI, Chapter VII, Article 51, R2P).

Distinguish strictly:
- VERIFIED FACT
- OFFICIAL STATEMENT
- ANALYSIS
"""
        messages = [
            LLMMessage(role="system", content="You are a senior UN archival researcher and international law scholar."),
            LLMMessage(role="user", content=prompt)
        ]
        
        response = await self.provider.generate(messages, temperature=0.2)
        return {
            "source_type": "PRIMARY_ARCHIVAL",
            "precedent_analysis": response.content,
            "verification_status": "ANALYSIS"
        }

    async def verify_statement(self, statement: str, claiming_actor: str) -> Dict[str, Any]:
        """Evaluate factual veracity and assign provenance labels per Section 6."""
        prompt = f"""
Evaluate the following diplomatic statement or reported fact:
Actor: {claiming_actor}
Statement: "{statement}"

Classify into one of these strict labels:
- VERIFIED FACT
- OFFICIAL STATEMENT
- REPORTED
- DISPUTED
- UNCONFIRMED
- ANALYSIS

Provide brief confidence justification.
"""
        messages = [
            LLMMessage(role="system", content="You are an intelligence verification officer. Never convert reported claims into confirmed facts."),
            LLMMessage(role="user", content=prompt)
        ]
        res = await self.provider.generate(messages, temperature=0.1)
        return {
            "evaluation": res.content,
            "provenance_checked": True
        }
