import json
import logging
from typing import Dict, Any, List, Optional
from app.ai.agents.base_agent import BaseAgent
from app.schemas.ai import LLMMessage, CountryReactionOutput

logger = logging.getLogger(__name__)

# Standard Geopolitical Profiles for UNSC Member States
COUNTRY_PROFILES: Dict[str, Dict[str, Any]] = {
    "USA": {
        "name": "United States of America",
        "status": "PERMANENT",
        "has_veto": True,
        "style": "Assertive, Coalition-focused, insists on strong enforcement and Israel/allies protection clauses.",
        "red_lines": ["Unconditional condemnation of allied actions", "Weakened counter-terrorism provisions", "Bypassing NATO/bilateral security pacts"],
        "concession_space": ["Humanitarian exemptions", "Multilateral monitoring missions", "Phased implementation"],
    },
    "GBR": {
        "name": "United Kingdom",
        "status": "PERMANENT",
        "has_veto": True,
        "style": "Rules-based international order, strong European coordination (E3), precise legal phrasing.",
        "red_lines": ["Undermining maritime freedom of navigation", "Rewarding unilateral aggression"],
        "concession_space": ["Bridge-building with Commonwealth members", "Technical annex amendments"],
    },
    "RUS": {
        "name": "Russian Federation",
        "status": "PERMANENT",
        "has_veto": True,
        "style": "Strict Westphalian sovereignty, anti-interventionist, swift to threaten veto against Western-drafted Chapter VII text.",
        "red_lines": ["Sanctions or military authorization against strategic partners", "Regime change mechanisms", "NATO expanding mandate"],
        "concession_space": ["Presidency statements (PRST) instead of binding resolutions", "Neutral fact-finding teams", "Balanced calls on all parties"],
    },
    "CHN": {
        "name": "People's Republic of China",
        "status": "PERMANENT",
        "has_veto": True,
        "style": "Cautious, sovereignty-oriented, non-interference, prefers consensus and political dialogue over punitive sanctions.",
        "red_lines": ["Infringement on state sovereignty", "Unilateral coercive measures", "Language affecting trade corridors/BRI"],
        "concession_space": ["Abstention rather than veto if sovereignty language is respected", "Support for regional mediation (AU/ASEAN/Arab League)"],
    },
    "DZA": {
        "name": "Algeria",
        "status": "ELECTED",
        "has_veto": False,
        "style": "Champion of the Arab and African groups, staunch defender of Palestinian self-determination, skeptical of Western unilateralism.",
        "red_lines": ["Ignoring humanitarian blockade in Gaza/Middle East", "Bypassing African Union mechanisms"],
        "concession_space": ["Language emphasizing humanitarian aid unimpeded access", "Joint AU-UN coordination"],
    },
    "GUY": {
        "name": "Guyana",
        "status": "ELECTED",
        "has_veto": False,
        "style": "Territorial integrity, international law, climate security, small states' vulnerability.",
        "red_lines": ["Violation of ICJ rulings", "Unilateral border alterations"],
        "concession_space": ["Support for multilateral peace missions", "Caribbean/CARICOM solidarity"],
    },
    "KOR": {
        "name": "Republic of Korea",
        "status": "ELECTED",
        "has_veto": False,
        "style": "Non-proliferation advocate, strict UN sanctions compliance, close coordination with USA and Japan.",
        "red_lines": ["Weakening DPRK sanctions regimes", "Lax maritime interdiction"],
        "concession_space": ["Cyber-security provisions", "Human rights reporting compromises"],
    },
    "SVN": {
        "name": "Slovenia",
        "status": "ELECTED",
        "has_veto": False,
        "style": "European Union consensus, International Humanitarian Law (IHL), protection of civilians and children in armed conflict.",
        "red_lines": ["Impunity for war crimes", "Attacks on UN and humanitarian workers"],
        "concession_space": ["Drafting compromise text on civilian corridors", "Confidence-building measures"],
    },
    "SLE": {
        "name": "Sierra Leone",
        "status": "ELECTED",
        "has_veto": False,
        "style": "A3+1 coordinator (African members), advocate for African Union peace architecture and reforming UNSC representation.",
        "red_lines": ["Excluding African Union from regional peace settlements"],
        "concession_space": ["Gradual drawdown of peacekeeping mandates", "Development-peace nexus language"],
    }
}

class UNSCCountrySimulationAgent(BaseAgent):
    """
    AGENT 2 — UNSC COUNTRY SIMULATION AGENT
    Responsibilities:
    - Simulates 14 UNSC states with distinct geopolitical realism
    - Negotiates in bilateral cables and council debates
    - Computes voting stances and veto thresholds
    - Accurately distinguishes simulation behavior from actual statements
    """
    def __init__(self):
        super().__init__(agent_name="UNSC Country Simulation Agent", agent_type="country")

    async def generate_reaction(
        self,
        country_code: str,
        crisis_context: str,
        france_action_or_message: str,
        relationship_trust: int = 70,
        current_world_state: Optional[Dict[str, Any]] = None
    ) -> CountryReactionOutput:
        country_profile = COUNTRY_PROFILES.get(country_code, {
            "name": country_code,
            "status": "ELECTED",
            "has_veto": False,
            "style": "Pragmatic, aligns with regional interests and multilateral consensus.",
            "red_lines": ["Violation of UN Charter sovereignty principles"],
            "concession_space": ["Constructive abstention or humanitarian amendments"]
        })

        system_prompt = f"""
You are the Diplomatic Delegation of {country_profile['name']} ({country_code}) on the UN Security Council.
Status: {country_profile['status']} (Veto power: {country_profile['has_veto']}).
Your Diplomatic Style: {country_profile['style']}
Your Red Lines: {', '.join(country_profile['red_lines'])}
Your Concession Space: {', '.join(country_profile['concession_space'])}
Trust Level with France: {relationship_trust}/100.

CRITICAL RULE:
- You are simulating this state's response within an academic UNSC crisis training scenario.
- Label output explicitly as SIMULATION.
- Do NOT simply agree with France. Defend your country's national interests, strategic partnerships, and domestic pressures realistically.
"""

        user_prompt = f"""
Current Crisis Context:
{crisis_context}

France's Diplomatic Action / Message to You:
"{france_action_or_message}"

Respond strictly with a structured JSON object adhering to this schema:
{{
  "country_code": "{country_code}",
  "country_name": "{country_profile['name']}",
  "current_stance": "SUPPORTIVE | CONDITIONAL | CAUTIOUS | CRITICAL | OPPOSING",
  "objective": "Concise national objective in this crisis",
  "demands": ["Demand 1", "Demand 2"],
  "red_lines": ["Red line 1"],
  "preferred_outcome": "Preferred UNSC outcome",
  "will_support": true/false,
  "conditional_support": true/false,
  "will_oppose": true/false,
  "possible_concession": "What you might offer in exchange",
  "reaction_to_france": "Internal diplomatic appraisal of France's move",
  "diplomatic_cable_response": "Formal diplomatic reply cable addressed to the Permanent Representative of France",
  "likely_next_action": "What your delegation will do in the council chamber",
  "confidence": 0.85,
  "reasoning_summary": "Why your government takes this position",
  "is_simulation": true
}}
"""
        messages = [
            LLMMessage(role="system", content=system_prompt),
            LLMMessage(role="user", content=user_prompt)
        ]

        structured = await self.provider.structured_generate(messages, CountryReactionOutput)
        if structured:
            return structured

        # Deterministic Geopolitical Fallback if LLM parsing or provider unavailable
        stance = "CONDITIONAL"
        cable = f"The Delegation of {country_profile['name']} acknowledges France's communication. While we share concerns over regional stability, any draft must rigorously respect our established positions."
        will_opp = False
        will_sup = False
        cond = True

        if country_code == "RUS":
            stance = "CRITICAL"
            will_opp = True
            cond = False
            cable = "The Russian Federation stresses that unilateral Western initiatives disregarding host-state sovereignty will not find consensus in this Council. We caution Paris against hasty Chapter VII mechanisms."
        elif country_code == "USA":
            stance = "SUPPORTIVE"
            will_sup = True
            cond = False
            cable = "The United States welcomes France's proactive leadership. We are prepared to coordinate closely on text, provided counter-terror commitments and allied defense guarantees remain ironclad."
        elif country_code == "CHN":
            stance = "CAUTIOUS"
            cable = "China emphasizes the primacy of diplomatic dialogue and regional de-escalation. We encourage France to avoid coercive sanctions language that exacerbates humanitarian strain."

        return CountryReactionOutput(
            country_code=country_code,
            country_name=country_profile["name"],
            current_stance=stance,
            objective=f"Safeguard {country_profile['name']}'s strategic and regional interests.",
            demands=[f"Respect {country_profile['name']} core principles in operative text"],
            red_lines=country_profile["red_lines"],
            preferred_outcome="Council resolution with balanced sovereign protections",
            will_support=will_sup,
            conditional_support=cond,
            will_oppose=will_opp,
            possible_concession="Constructive abstention or humanitarian carveout",
            reaction_to_france=f"Calculated reaction assessing French leverage and domestic constraints.",
            diplomatic_cable_response=cable,
            likely_next_action="Consult regional allies before floor debate.",
            confidence=0.9,
            reasoning_summary=f"Position reflects {country_profile['name']}'s historical voting doctrine on Chapter VI vs Chapter VII interventions.",
            is_simulation=True
        )
