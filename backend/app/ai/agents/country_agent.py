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
    # Elected members, term 2025-2026
    "DNK": {
        "name": "Denmark",
        "status": "ELECTED",
        "has_veto": False,
        "style": "Nordic multilateralism, EU coordination, human rights, climate-security nexus and women, peace and security agenda.",
        "red_lines": ["Impunity for violations of international humanitarian law", "Weakening of UN human rights mechanisms"],
        "concession_space": ["Co-drafting civilian protection language with EU partners", "Humanitarian carve-outs in sanctions regimes"],
    },
    "GRC": {
        "name": "Greece",
        "status": "ELECTED",
        "has_veto": False,
        "style": "Law of the Sea (UNCLOS) advocate, maritime security, Mediterranean stability, close EU coordination.",
        "red_lines": ["Legitimizing territorial or maritime claims made by force", "Undermining UNCLOS"],
        "concession_space": ["Maritime de-escalation mechanisms", "EU-aligned compromise text"],
    },
    "PAK": {
        "name": "Pakistan",
        "status": "ELECTED",
        "has_veto": False,
        "style": "OIC voice, self-determination, counter-terrorism, major peacekeeping contributor, wary of Western-led coercive measures.",
        "red_lines": ["Selective application of counter-terrorism language", "Ignoring Palestinian and Kashmiri self-determination"],
        "concession_space": ["Peacekeeper safety provisions", "Balanced calls on all parties to exercise restraint"],
    },
    "PAN": {
        "name": "Panama",
        "status": "ELECTED",
        "has_veto": False,
        "style": "Consensus builder from GRULAC, maritime corridors and freedom of navigation, migration and transnational crime.",
        "red_lines": ["Disruption of international shipping lanes", "Unilateral use of force outside the Charter"],
        "concession_space": ["Support for mediation and humanitarian pauses", "Maritime safety annexes"],
    },
    "SOM": {
        "name": "Somalia",
        "status": "ELECTED",
        "has_veto": False,
        "style": "A3 member, post-conflict stabilization, counter-insurgency, strong defender of sovereignty and African Union primacy.",
        "red_lines": ["Bypassing African Union mechanisms", "External interference in sovereign affairs"],
        "concession_space": ["AU-UN partnership language", "Humanitarian access and development-peace nexus"],
    },
    # Elected members, term 2026-2027
    "BHR": {
        "name": "Bahrain",
        "status": "ELECTED",
        "has_veto": False,
        "style": "Arab Group seat, Gulf maritime security, counter-terrorism, favors regional de-escalation and Arab League mediation.",
        "red_lines": ["Threats to Gulf shipping and maritime security", "Ignoring Arab League positions"],
        "concession_space": ["Regional mediation mechanisms", "Humanitarian corridors with maritime security guarantees"],
    },
    "COL": {
        "name": "Colombia",
        "status": "ELECTED",
        "has_veto": False,
        "style": "Peace-process experience, transitional justice, supports UN verification missions and dialogue over sanctions.",
        "red_lines": ["Militarized solutions that close space for negotiation"],
        "concession_space": ["Ceasefire verification mechanisms", "Dialogue and mediation clauses"],
    },
    "COD": {
        "name": "Democratic Republic of the Congo",
        "status": "ELECTED",
        "has_veto": False,
        "style": "A3 member, sovereignty and territorial integrity, protection of civilians, insists on African ownership of peace processes.",
        "red_lines": ["Legitimizing armed groups or foreign-backed incursions", "Excluding the African Union from settlements"],
        "concession_space": ["Phased peacekeeping transitions", "AU-led mediation with UN support"],
    },
    "LVA": {
        "name": "Latvia",
        "status": "ELECTED",
        "has_veto": False,
        "style": "EU and Baltic solidarity, territorial integrity, accountability for aggression, resilience against disinformation.",
        "red_lines": ["Rewarding aggression or recognizing territory seized by force"],
        "concession_space": ["EU-coordinated compromise text", "Accountability and monitoring mechanisms"],
    },
    "LBR": {
        "name": "Liberia",
        "status": "ELECTED",
        "has_veto": False,
        "style": "A3 member, post-conflict peacebuilding experience, advocate of African Union peace architecture and UNSC reform.",
        "red_lines": ["Excluding African Union from regional peace settlements"],
        "concession_space": ["Peacebuilding and development-peace nexus language", "Humanitarian access provisions"],
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
