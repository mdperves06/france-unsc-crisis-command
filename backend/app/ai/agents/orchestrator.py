import copy
import logging
from typing import Dict, Any, List, Optional
from app.ai.agents.base_agent import BaseAgent
from app.ai.agents.research_agent import GlobalResearchAgent
from app.ai.agents.country_agent import UNSCCountrySimulationAgent
from app.ai.agents.france_coach_agent import FranceStrategyCoach
from app.schemas.ai import LLMMessage

logger = logging.getLogger(__name__)

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
        active_actors = ["USA", "GBR", "RUS", "CHN", "DZA"]
        country_reactions = {}
        
        # Primary targeted country
        target = target_country if target_country in active_actors else "USA"
        primary_reaction = await self.country_agent.generate_reaction(
            country_code=target,
            crisis_context=scenario_context.get("initial_situation", ""),
            france_action_or_message=f"{action_type}: {str(details)}",
            relationship_trust=new_state.get("country_states", {}).get(target, {}).get("trust", 70)
        )
        country_reactions[target] = primary_reaction.model_dump()

        # Update target country in state
        if "country_states" not in new_state:
            new_state["country_states"] = {}
        
        new_state["country_states"][target] = {
            "stance": primary_reaction.current_stance,
            "trust": 75 if primary_reaction.will_support else 55,
            "coalition": "SUPPORT" if primary_reaction.will_support else ("OPPOSED" if primary_reaction.will_oppose else "CONDITIONAL"),
            "demands": primary_reaction.demands,
            "latest_cable": primary_reaction.diplomatic_cable_response
        }

        # 3. Simulate Russia/China counter-moves if not targeted
        if target != "RUS":
            rus_reaction = await self.country_agent.generate_reaction(
                country_code="RUS",
                crisis_context=scenario_context.get("initial_situation", ""),
                france_action_or_message=f"France executed: {action_type}",
                relationship_trust=45
            )
            country_reactions["RUS"] = rus_reaction.model_dump()
            new_state["country_states"]["RUS"] = {
                "stance": rus_reaction.current_stance,
                "trust": 45,
                "coalition": "OPPOSED" if rus_reaction.will_oppose else "CONDITIONAL",
                "demands": rus_reaction.demands,
                "latest_cable": rus_reaction.diplomatic_cable_response
            }

        # 4. Update World State Metrics
        escalation_delta = 0
        if action_type in ["REQUEST_EMERGENCY_MEETING", "PROPOSE_CEASEFIRE", "CONTACT_CHINA", "CONTACT_RUSSIA"]:
            escalation_delta = -5
            new_state["diplomatic_tension"] = max(10, new_state.get("diplomatic_tension", 60) - 4)
            new_state["france_reputation"] = min(100, new_state.get("france_reputation", 75) + 3)
        elif action_type in ["THREATEN_VETO", "UNILATERAL_STATEMENT", "DEMAND_SANCTIONS"]:
            escalation_delta = 8
            new_state["diplomatic_tension"] = min(100, new_state.get("diplomatic_tension", 60) + 7)
        
        new_state["escalation_level"] = max(10, min(100, new_state.get("escalation_level", 50) + escalation_delta))

        # 5. Compute Coalition & UNSC Voting Calculus
        support_list = ["FRA"]
        conditional_list = []
        opposed_list = []
        undecided_list = ["GUY", "KOR", "SVN", "SLE", "ECU", "JPN", "MLT", "MOZ", "CHE"]

        for c_code, c_data in new_state.get("country_states", {}).items():
            coalition = c_data.get("coalition")
            if coalition == "SUPPORT":
                if c_code not in support_list: support_list.append(c_code)
            elif coalition == "OPPOSED":
                if c_code not in opposed_list: opposed_list.append(c_code)
            else:
                if c_code not in conditional_list: conditional_list.append(c_code)
            if c_code in undecided_list:
                undecided_list.remove(c_code)

        new_state["coalition_status"] = {
            "support": support_list,
            "conditional": conditional_list,
            "opposed": opposed_list,
            "undecided": undecided_list
        }

        # Projected Vote Math:
        # Conditional members split: half lean YES, the rest abstain (each member counted once)
        conditional_yes = len(conditional_list) // 2
        yes_count = len(support_list) + conditional_yes
        p5_veto_threats = [c for c in opposed_list if c in ["USA", "RUS", "CHN", "GBR"]]
        has_p5_veto = bool(p5_veto_threats)
        outcome_prediction = "WOULD PASS" if (yes_count >= 9 and not has_p5_veto) else ("VETO RISK" if has_p5_veto else "INSUFFICIENT VOTES")

        new_state["projected_vote"] = {
            "yes_estimate": yes_count,
            "no_estimate": len(opposed_list),
            "abstain_estimate": len(conditional_list) - conditional_yes + len(undecided_list),
            "p5_veto_threats": p5_veto_threats,
            "outcome_prediction": outcome_prediction,
            "requires_9_votes": True,
            "label": "SIMULATION ESTIMATE"
        }

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
                "headline": "A3+1 African Member States Coordinate Joint Communiqué",
                "description": "Algeria and Sierra Leone request formal clause explicitly reaffirming African Union conflict mediation primacy before voting YES.",
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
