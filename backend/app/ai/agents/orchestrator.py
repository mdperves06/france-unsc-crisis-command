import copy
import logging
from typing import Dict, Any, List, Optional
from app.ai.agents.base_agent import BaseAgent
from app.ai.agents.research_agent import GlobalResearchAgent
from app.ai.agents.country_agent import UNSCCountrySimulationAgent
from app.ai.agents.france_coach_agent import FranceStrategyCoach
from app.schemas.ai import LLMMessage

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 2026 UN Security Council roster used by the vote calculus
# ---------------------------------------------------------------------------
UNSC_P5 = ["CHN", "FRA", "RUS", "GBR", "USA"]
UNSC_ELECTED_2026 = ["DNK", "GRC", "PAK", "PAN", "SOM", "BHR", "COL", "COD", "LVA", "LBR"]
UNSC_MEMBERS_2026 = UNSC_P5 + UNSC_ELECTED_2026

A3_MEMBERS = ["SOM", "COD", "LBR"]        # African members (no Caribbean "+1" in 2026)
EU_MEMBERS = ["DNK", "GRC", "LVA"]        # Elected EU partners for E3/EU coordination
OIC_MEMBERS = ["PAK", "BHR"]              # OIC / Arab Group voices
GRULAC_MEMBERS = ["PAN", "COL"]

# Leaning toward France's draft, 0-100 (persisted per member in country_states["leaning"]).
#   >= 65 SUPPORT | 45-64 CONDITIONAL | 30-44 UNDECIDED | < 30 OPPOSED
# Projected vote: NO if OPPOSED, YES if leaning >= 55, otherwise ABSTAIN.
INITIAL_LEANINGS_2026 = {
    "USA": 75, "GBR": 80, "RUS": 20, "CHN": 48,
    "DNK": 55, "GRC": 55, "LVA": 52,
    "PAK": 40, "BHR": 42, "PAN": 45, "COL": 45,
    "SOM": 45, "COD": 48, "LBR": 45,
}
YES_THRESHOLD = 55

# Deterministic effect of each France action on member leanings.
# Keys are member codes or blocs ("A3", "EU", "OIC", "GRULAC", "ELECTED" = all ten elected).
ACTION_LEANING_EFFECTS: Dict[str, Dict[str, int]] = {
    # Consultative / de-escalatory
    "REQUEST_EMERGENCY_MEETING": {"ELECTED": 4, "CHN": 3, "RUS": 2},
    "PROPOSE_CEASEFIRE": {"A3": 8, "OIC": 6, "GRULAC": 5, "EU": 4, "CHN": 5, "RUS": 4},
    "HUMANITARIAN_CORRIDOR": {"A3": 8, "OIC": 6, "GRULAC": 5, "EU": 4, "CHN": 3, "RUS": 2},
    "CONSULT_A3": {"A3": 14, "OIC": 3, "CHN": 3},
    "COORDINATE_EU": {"EU": 12, "GBR": 4, "USA": 2, "RUS": -2},
    "CONTACT_USA": {"USA": 5, "GBR": 3, "EU": 4, "RUS": -3},
    "CONTACT_RUSSIA": {"RUS": 12, "CHN": 4, "PAK": 3, "LVA": -4},
    "CONTACT_CHINA": {"CHN": 12, "RUS": 3, "PAK": 6, "BHR": 3, "A3": 3},
    "DRAFT_PRST": {"ELECTED": 4, "CHN": 6, "RUS": 8},
    "DRAFT_RESOLUTION": {"EU": 5, "USA": 3, "GBR": 3, "GRULAC": 3, "CHN": -2, "RUS": -4},
    # Escalatory
    "THREATEN_VETO": {"A3": -8, "OIC": -6, "GRULAC": -5, "EU": -3, "CHN": -8, "RUS": -10},
    "UNILATERAL_STATEMENT": {"ELECTED": -5, "CHN": -5, "RUS": -5, "GBR": -3, "USA": -3},
    "DEMAND_SANCTIONS": {"A3": -6, "OIC": -6, "GRULAC": -3, "EU": 2, "USA": 3, "GBR": 3, "CHN": -12, "RUS": -15},
}
ESCALATORY_ACTIONS = ["THREATEN_VETO", "UNILATERAL_STATEMENT", "DEMAND_SANCTIONS"]
TARGET_ATTENTION_BONUS = 6   # a non-escalatory action addressed to a delegation warms it further
REPEAT_ACTION_FACTOR = 0.5   # repeating last turn's move has diminishing diplomatic returns

BLOCS = {"A3": A3_MEMBERS, "EU": EU_MEMBERS, "OIC": OIC_MEMBERS, "GRULAC": GRULAC_MEMBERS, "ELECTED": UNSC_ELECTED_2026}


def coalition_from_leaning(leaning: int) -> str:
    if leaning >= 65:
        return "SUPPORT"
    if leaning >= 45:
        return "CONDITIONAL"
    if leaning >= 30:
        return "UNDECIDED"
    return "OPPOSED"


def ensure_2026_country_states(country_states: Dict[str, Any]) -> Dict[str, Any]:
    """Returns country_states for the 14 non-French 2026 members, each with a numeric leaning.
    Members missing from older saved states get their initial leaning; stale (non-2026) codes are dropped."""
    states = {}
    for code in UNSC_MEMBERS_2026:
        if code == "FRA":
            continue
        c_data = dict(country_states.get(code, {}))
        c_data.setdefault("leaning", INITIAL_LEANINGS_2026[code])
        c_data.setdefault("stance", "CONDITIONAL")
        c_data.setdefault("trust", 60)
        c_data.setdefault("demands", [])
        c_data["coalition"] = coalition_from_leaning(c_data["leaning"])
        states[code] = c_data
    return states


def apply_action_to_leanings(country_states: Dict[str, Any], action_type: str, target: Optional[str],
                             last_action_type: Optional[str] = None) -> None:
    """Shifts member leanings in place according to ACTION_LEANING_EFFECTS."""
    factor = REPEAT_ACTION_FACTOR if action_type == last_action_type else 1.0
    deltas: Dict[str, int] = {}
    for key, delta in ACTION_LEANING_EFFECTS.get(action_type, {}).items():
        for code in BLOCS.get(key, [key]):
            deltas[code] = deltas.get(code, 0) + int(delta * factor)
    if target in country_states and action_type not in ESCALATORY_ACTIONS:
        deltas[target] = deltas.get(target, 0) + TARGET_ATTENTION_BONUS

    for code, delta in deltas.items():
        if code in country_states:
            leaning = max(0, min(100, country_states[code]["leaning"] + delta))
            country_states[code]["leaning"] = leaning
            country_states[code]["coalition"] = coalition_from_leaning(leaning)


def compute_coalition_and_vote(country_states: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Article 27 calculus over all 15 members; each member is counted exactly once."""
    support_list = ["FRA"]
    conditional_list = []
    opposed_list = []
    undecided_list = []
    yes_count, no_count, abstain_count = 1, 0, 0  # France votes for its own draft

    for c_code in UNSC_MEMBERS_2026:
        if c_code == "FRA":
            continue
        leaning = country_states[c_code]["leaning"]
        coalition = coalition_from_leaning(leaning)
        if coalition == "SUPPORT":
            support_list.append(c_code)
        elif coalition == "CONDITIONAL":
            conditional_list.append(c_code)
        elif coalition == "UNDECIDED":
            undecided_list.append(c_code)
        else:
            opposed_list.append(c_code)

        if coalition == "OPPOSED":
            no_count += 1
        elif leaning >= YES_THRESHOLD:
            yes_count += 1
        else:
            abstain_count += 1

    p5_veto_threats = [c for c in opposed_list if c in UNSC_P5]
    has_p5_veto = bool(p5_veto_threats)
    outcome_prediction = "WOULD PASS" if (yes_count >= 9 and not has_p5_veto) else ("VETO RISK" if has_p5_veto else "INSUFFICIENT VOTES")

    return {
        "coalition_status": {
            "support": support_list,
            "conditional": conditional_list,
            "opposed": opposed_list,
            "undecided": undecided_list
        },
        "projected_vote": {
            "yes_estimate": yes_count,
            "no_estimate": no_count,
            "abstain_estimate": abstain_count,
            "p5_veto_threats": p5_veto_threats,
            "outcome_prediction": outcome_prediction,
            "requires_9_votes": True,
            "label": "SIMULATION ESTIMATE"
        }
    }


class CrisisOrchestrator(BaseAgent):
    """
    AGENT 4 — CRISIS ORCHESTRATOR & SYNTHESIZER
    Responsibilities:
    - Coordinates Agent 1 (Research), Agent 2 (Country Simulation), and Agent 3 (Coach)
    - Reconciles conflicting agent outputs into a unified simulation reality
    - Maintains and updates persistent World State
    - Injects dynamic crisis events, twists, and hidden variables
    - Computes UNSC voting calculus (Article 27: 9 votes + No P5 veto)
    - Compiles comprehensive After-Action Reviews (AAR)
    """
    def __init__(self):
        super().__init__(agent_name="Crisis Orchestrator", agent_type="orchestrator")
        self.research_agent = GlobalResearchAgent()
        self.country_agent = UNSCCountrySimulationAgent()
        self.coach_agent = FranceStrategyCoach()

    async def advance_simulation_turn(
        self,
        current_world_state: Dict[str, Any],
        scenario_context: Dict[str, Any],
        france_action: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Processes a full turn in the Crisis Arena:
        1. Validates France's action
        2. Calls Country Agent for targeted country and affected UNSC members
        3. Updates World State (escalation, diplomatic tension, trust)
        4. Calculates Coalition shifts & UNSC Voting viability
        5. Injects potential dynamic twists/events
        6. Reconciles with research/international law
        """
        new_state = copy.deepcopy(current_world_state)
        turn = new_state.get("turn", 1) + 1
        new_state["turn"] = turn

        action_type = france_action.get("action_type", "")
        target_country = france_action.get("target_country")
        details = france_action.get("parameters", {})
        rationale = france_action.get("rationale", "")

        # 1. Evaluate Action Authority & Consequences
        authority_status = "ALLOWED"
        authority_rationale = "Action falls within normal diplomatic prerogatives of a UNSC Permanent Member."
        
        if action_type == "USE_VETO" and details.get("stage") != "VOTING_PROCEDURE":
            authority_status = "LIMITED"
            authority_rationale = "Veto can only be formally registered during substantive voting on a tabled draft resolution (Article 27(3))."

        # 2. Simulate Key Country Reactions via Agent 2
        country_reactions = {}
        new_state["country_states"] = ensure_2026_country_states(new_state.get("country_states") or {})

        # Primary targeted country (any 2026 Council member other than France)
        target = target_country if target_country in new_state["country_states"] else "USA"
        primary_reaction = await self.country_agent.generate_reaction(
            country_code=target,
            crisis_context=scenario_context.get("initial_situation", ""),
            france_action_or_message=f"{action_type}: {str(details)}",
            relationship_trust=new_state["country_states"][target].get("trust", 70)
        )
        country_reactions[target] = primary_reaction.model_dump()

        # Update target country in state. Its leaning is shifted by France's action in step 5;
        # the agent's explicit support/opposition adds a small nudge on top.
        reaction_nudge = 5 if primary_reaction.will_support else (-5 if primary_reaction.will_oppose else 0)
        new_state["country_states"][target].update({
            "stance": primary_reaction.current_stance,
            "trust": 75 if primary_reaction.will_support else 55,
            "leaning": max(0, min(100, new_state["country_states"][target]["leaning"] + reaction_nudge)),
            "demands": primary_reaction.demands,
            "latest_cable": primary_reaction.diplomatic_cable_response
        })

        # 3. Simulate Russia/China counter-moves if not targeted
        if target != "RUS":
            rus_reaction = await self.country_agent.generate_reaction(
                country_code="RUS",
                crisis_context=scenario_context.get("initial_situation", ""),
                france_action_or_message=f"France executed: {action_type}",
                relationship_trust=45
            )
            country_reactions["RUS"] = rus_reaction.model_dump()
            # Russia's counter-move updates its rhetoric; its vote leaning follows France's actions (step 5)
            new_state["country_states"]["RUS"].update({
                "stance": rus_reaction.current_stance,
                "trust": 45,
                "demands": rus_reaction.demands,
                "latest_cable": rus_reaction.diplomatic_cable_response
            })

        # 4. Update World State Metrics
        escalation_delta = 0
        if action_type in ["REQUEST_EMERGENCY_MEETING", "PROPOSE_CEASEFIRE", "CONTACT_CHINA", "CONTACT_RUSSIA", "HUMANITARIAN_CORRIDOR", "CONSULT_A3"]:
            escalation_delta = -5
            new_state["diplomatic_tension"] = max(10, new_state.get("diplomatic_tension", 60) - 4)
            new_state["france_reputation"] = min(100, new_state.get("france_reputation", 75) + 3)
        elif action_type in ESCALATORY_ACTIONS:
            escalation_delta = 8
            new_state["diplomatic_tension"] = min(100, new_state.get("diplomatic_tension", 60) + 7)
        
        new_state["escalation_level"] = max(10, min(100, new_state.get("escalation_level", 50) + escalation_delta))

        # 5. Compute Coalition & UNSC Voting Calculus
        # France's action shifts the persisted member leanings deterministically: consultative and
        # humanitarian moves win over elected members (A3 on humanitarian/AU primacy, EU partners on
        # E3/EU coordination); escalatory moves push members toward abstention or opposition.
        apply_action_to_leanings(new_state["country_states"], action_type, target, new_state.pop("last_action_type", None))
        new_state.update(compute_coalition_and_vote(new_state["country_states"]))

        # 6. Inject dynamic events / twists (Section 27)
        twist_event = None
        if turn == 2:
            twist_event = {
                "headline": "Humanitarian Convoy Stalled at Buffer Zone",
                "description": "UN OCHA reports aid trucks carrying emergency medical supplies have been halted due to renewed artillery fire. Regional media leaks private French diplomatic overtures.",
                "source_type": "SIMULATION",
                "impact": "Heightened humanitarian urgency"
            }
        elif turn == 3:
            twist_event = {
                "headline": "A3 African Member States Coordinate Joint Communiqué",
                "description": "Somalia, the Democratic Republic of the Congo and Liberia request a formal clause explicitly reaffirming African Union conflict mediation primacy before voting YES.",
                "source_type": "SIMULATION",
                "impact": "Crucial swing vote leverage opened"
            }

        summary_turn = f"Turn {turn}: France initiated '{action_type}'. {target} responded ({primary_reaction.current_stance}). Council escalation shifted to {new_state['escalation_level']}."
        new_state["summary_of_turn"] = summary_turn

        return {
            "updated_world_state": new_state,
            "authority_status": authority_status,
            "authority_rationale": authority_rationale,
            "primary_reaction": primary_reaction.model_dump(),
            "all_reactions": country_reactions,
            "twist_event": twist_event,
            "turn_summary": summary_turn
        }

    async def generate_after_action_review(
        self,
        session_id: str,
        scenario: Dict[str, Any],
        final_state: Dict[str, Any],
        action_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Section 61 After-Action Review (AAR) synthesis."""
        actions_taken = [a.get("action_type") for a in action_history]
        reputation = final_state.get("france_reputation", 75)
        escalation = final_state.get("escalation_level", 50)
        veto_threats = final_state.get("projected_vote", {}).get("p5_veto_threats", [])
        
        prompt = f"""
Synthesize a comprehensive, rigorous After-Action Review (AAR) for the French Delegation at the UN Security Council:
Scenario: {scenario.get('title')}
Difficulty: {scenario.get('difficulty')}
Actions Taken by France: {', '.join(actions_taken)}
Final Escalation Level: {escalation}/100
Final France Reputation: {reputation}/100
Remaining P5 Veto Threats: {', '.join(veto_threats) if veto_threats else 'None'}

Provide:
1. WHAT YOU DID: Summary of user strategy.
2. WHAT HAPPENED: World state and diplomatic outcome.
3. WHY IT HAPPENED: Structural diplomatic reasons.
4. WHAT YOU MISSED: Blind spots, ignored elected members or legal tools.
5. WHICH ACTORS YOU MISREAD: Realistic analysis of adversary/partner incentives.
6. WHAT FRANCE COULD HAVE CONSIDERED: Alternative high-impact moves.
7. WHAT TO PRACTICE NEXT: Targeted MUN skill recommendation.
"""
        messages = [
            LLMMessage(role="system", content="You are the Dean of the Diplomatic Academy analyzing a delegate's performance."),
            LLMMessage(role="user", content=prompt)
        ]

        review_res = await self.provider.generate(messages, temperature=0.3)
        return {
            "session_id": session_id,
            "what_user_did": actions_taken,
            "what_happened": f"Crisis concluded with Escalation at {escalation}/100 and France Reputation at {reputation}/100.",
            "full_analysis": review_res.content,
            "unlocked_hidden_variables": {
                "russian_true_redline": "Host nation consent clause was non-negotiable",
                "us_domestic_constraint": "Upcoming midterm election limited troop deployment",
                "elected_members_swing": "A3 members were waiting for humanitarian priority wording"
            },
            "next_practice_recommendation": "Nine-vote coalition building with A3 African Group members under Article 27."
        }
