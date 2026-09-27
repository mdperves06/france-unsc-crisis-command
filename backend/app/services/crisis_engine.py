import uuid
import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.crisis import CrisisScenario, CrisisEvent
from app.schemas.crisis import CrisisScenarioCreate
from app.ai.agents.orchestrator import CrisisOrchestrator
from app.ai.agents.france_coach_agent import FranceStrategyCoach

DECISION_FRAMEWORK_STEPS = [
    {"step": 1, "title": "UNDERSTAND THE CRISIS", "question": "What actually happened on the ground, and what are the verified facts versus disputed reports?"},
    {"step": 2, "title": "IDENTIFY UNCERTAINTIES", "question": "What critical facts remain unknown, unconfirmed, or disputed?"},
    {"step": 3, "title": "IDENTIFY IMMEDIATE THREAT", "question": "What is the most acute, irreversible threat to international peace or civilian life right now?"},
    {"step": 4, "title": "DEFINE FRANCE'S INTEREST", "question": "Why does France care? What specific European, multilateral, or national strategic stakes are involved?"},
    {"step": 5, "title": "DEFINE FRANCE'S OBJECTIVE", "question": "What is France's concrete diplomatic end-state (e.g. ceasefire, monitoring mission, sanctions carveout)?"},
    {"step": 6, "title": "DEFINE RED LINES", "question": "What outcomes or concessions are strictly unacceptable to Paris?"},
    {"step": 7, "title": "IDENTIFY AVAILABLE AUTHORITY", "question": "What UN Charter authority (Chapter VI vs VII, Article 40, Article 41, Article 42) applies?"},
    {"step": 8, "title": "MAP ACTORS", "question": "Which state and non-state actors have the power to change conditions on the ground or in the Council?"},
    {"step": 9, "title": "MAP SUPPORT", "question": "Who are France's natural allies, and which elected members can form a reliable coalition core?"},
    {"step": 10, "title": "MAP OPPOSITION & BLOCKERS", "question": "Who has veto power or sufficient votes to block your proposal, and what are their underlying concerns?"},
    {"step": 11, "title": "IDENTIFY NEGOTIATION SPACE", "question": "What can France realistically offer each blocking power without crossing our red lines?"},
    {"step": 12, "title": "SELECT FIRST MOVE", "question": "What is your immediate tactical action (e.g. private bilateral cable, E3 demarche, emergency consultations)?"},
    {"step": 13, "title": "PREPARE BACKUP PLAN", "question": "If your primary resolution faces a P5 veto threat, what is your secondary fallback mechanism?"},
    {"step": 14, "title": "ANTICIPATE CONSEQUENCES", "question": "What are the immediate second-order risks of this move if implemented?"}
]

class CrisisEngineService:
    def __init__(self):
        self.orchestrator = CrisisOrchestrator()
        self.coach = FranceStrategyCoach()

    def generate_scenario(self, db: Session, req: CrisisScenarioCreate) -> CrisisScenario:
        scenario_id = f"scenario-{uuid.uuid4().hex[:8]}"
        title = f"{req.region}: {req.crisis_type} Escalation in the Maritime & Border Corridors"
        
        # Comprehensive scenario with France stakes, actors, and verified facts
        scenario = CrisisScenario(
            scenario_id=scenario_id,
            title=title,
            region=req.region,
            crisis_type=req.crisis_type,
            difficulty=req.difficulty,
            initial_situation=f"An armed confrontation erupted along the strategic transit corridor in {req.region}. Opposing state forces and non-state militias have exchanged artillery, cutting off critical humanitarian supply lines and threatening international commercial navigation.",
            location_details=f"Northern Border Sector & Maritime Approaches, {req.region}",
            coordinates={"lat": 33.8938 if "Middle East" in req.region else (48.3794 if "Eastern" in req.region else 12.8628), "lng": 35.5018 if "Middle East" in req.region else (31.1656 if "Eastern" in req.region else 30.2176)},
            background=f"Tensions have simmered over contested borders, resource transit, and disputed sovereign interpretations. Past UNSC presidential statements failed to deter militarization. Host-nation authorities requested urgent Council intervention.",
            known_facts=[
                {"fact": "Artillery exchanges began at 04:30 UTC damaging two civilian relief warehouses.", "status": "VERIFIED FACT", "source": "UN OCHA Situation Report"},
                {"fact": "Hostilities have displaced over 45,000 civilians toward the southern frontier.", "status": "REPORTED", "source": "UNHCR Press Briefing"},
                {"fact": "Host state claims foreign drones violated its sovereign airspace.", "status": "OFFICIAL STATEMENT", "source": "Ministry of Foreign Affairs Statement"}
            ],
            unknown_facts=[
                "Exact casualty toll among peacekeeper detachment stationed near Sector B.",
                "Whether military escalations were pre-authorized by supreme command or triggered by rogue local militias.",
                "P5 intentions regarding Chapter VII enforcement versus Chapter VI inquiry."
            ],
            key_actors=[
                {"code": "FRA", "name": "France", "role": "Permanent Member & Mediator"},
                {"code": "USA", "name": "United States", "role": "Security Guarantor"},
                {"code": "RUS", "name": "Russian Federation", "role": "Strategic Partner to Regional Faction"},
                {"code": "CHN", "name": "China", "role": "Economic Corridor Stakeholder"},
                {"code": "DZA", "name": "Algeria", "role": "Regional & African Group Advocate"}
            ],
            actor_initial_stances={
                "USA": "Demands immediate allied protection and counter-terror clauses.",
                "RUS": "Insists on strict host-state sovereignty and cautions against Western Chapter VII mandates.",
                "CHN": "Urges bilateral negotiation, restraint, and rejects punitive economic sanctions.",
                "DZA": "Demands immediate humanitarian ceasefire and unhindered UN aid passage."
            },
            france_interest="Preserve regional peace architecture, prevent regional war, uphold international humanitarian law, safeguard French nationals, and sustain European strategic presence.",
            france_immediate_threat="Imminent collapse of humanitarian corridors and rapid military escalation triggering P5 confrontation.",
            france_objectives=[
                "Secure a binding ceasefire and humanitarian pause",
                "Deploy a neutral UN Fact-Finding / Observer detachment under Chapter VI",
                "Prevent Russian/Chinese veto through balanced compromise text"
            ],
            france_red_lines=[
                "No recognition of territorial gains acquired by armed force",
                "No obstruction of impartial humanitarian aid delivery",
                "No abandonment of French European partner security commitments"
            ],
            available_tools=[
                "Article 24/27 UNSC Draft Resolution",
                "Presidential Statement (PRST)",
                "E3 Diplomatic Demarche (France-Germany-UK)",
                "Article 34 Investigation Request",
                "Emergency Consultations of the Whole"
            ],
            strategic_paths=[
                {"path": "Humanitarian-First Fast Track (PRST/Resolution)", "tradeoff": "High consensus probability; delays military settlement."},
                {"path": "Assertive Chapter VII Mandate with Allied P3 Support", "tradeoff": "Demonstrates decisive deterrence; high Russian veto risk."},
                {"path": "Elected Member Bridge (A3+1 / E10 Co-Sponsorship)", "tradeoff": "Secures overwhelming 10+ votes; dilutes punitive enforcement."}
            ],
            escalation_paths=[
                "Artillery strikes hit UN peacekeeper outpost",
                "Armed factions blockade the maritime straits",
                "Retaliatory air strikes launched against command installations"
            ],
            deescalation_paths=[
                "48-hour humanitarian truce agreed by opposing commanders",
                "UN Secretary-General appoints Special Envoy for direct mediation",
                "UNSC adopts consensus Presidential Statement"
            ],
            hidden_scenario_variables={
                "host_nation_backchannel": "Willing to accept neutral European monitors if not labeled an intervention.",
                "russian_veto_threshold": "Will veto any resolution referencing sanctions or asset freezes."
            },
            is_custom_or_imported=False
        )

        db.add(scenario)
        db.commit()
        db.refresh(scenario)
        return scenario

    def evaluate_training_step(self, step_number: int, user_answer: str, scenario: CrisisScenario) -> Dict[str, Any]:
        """Evaluates a user's answer in the 14-step France Decision Framework."""
        framework_step = DECISION_FRAMEWORK_STEPS[min(len(DECISION_FRAMEWORK_STEPS) - 1, max(0, step_number - 1))]
        
        answer_length = len(user_answer.strip())
        score = 8.0 if answer_length > 60 else (6.0 if answer_length > 25 else 4.0)
        did_pass = score >= 5.0
        
        next_step = step_number + 1 if step_number < 14 else None
        next_q = DECISION_FRAMEWORK_STEPS[next_step - 1]["question"] if next_step else None
        
        hint = self.coach.get_progressive_hint(min(6, (step_number // 2) + 1), {})

        guidance = f"French diplomatic doctrine prioritizes rigorous legal grounding (UN Charter), multilateral legitimacy, and calculating counter-moves before tabling text. In Step {step_number} ({framework_step['title']}), your focus must balance moral urgency with P5 voting mechanics."

        return {
            "step_number": step_number,
            "step_title": framework_step["title"],
            "user_evaluation": "Good analytical instinct." if did_pass else "Answer is somewhat underdeveloped; expand on France's specific diplomatic leverage.",
            "score": score,
            "did_pass": did_pass,
            "france_doctrine_guidance": guidance,
            "next_question": next_q,
            "hint": hint["guidance"]
        }
