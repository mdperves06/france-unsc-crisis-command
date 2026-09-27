import uuid
import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.simulation import SimulationSession, SimulationWorldState, DiplomaticMessage, SimulationActionLog
from app.models.crisis import CrisisScenario
from app.ai.agents.orchestrator import CrisisOrchestrator, ensure_2026_country_states, compute_coalition_and_vote

class SimulationService:
    def __init__(self):
        self.orchestrator = CrisisOrchestrator()

    def start_session(self, db: Session, scenario_id: str, mode: str = "PRACTICE_ARENA", difficulty: str = "Intermediate", year: int = 2026) -> SimulationSession:
        session_id = f"sim-{uuid.uuid4().hex[:10]}"
        scenario = db.query(CrisisScenario).filter(CrisisScenario.scenario_id == scenario_id).first()
        if not scenario:
            # Unknown id (e.g. the frontend's "scenario-default"): use the latest generated scenario
            scenario = db.query(CrisisScenario).order_by(CrisisScenario.id.desc()).first()
            if not scenario:
                raise ValueError("Scenario not found")
            scenario_id = scenario.scenario_id
        
        session = SimulationSession(
            session_id=session_id,
            scenario_id=scenario_id,
            mode=mode,
            difficulty=difficulty,
            year=year,
            current_turn=1,
            status="ACTIVE"
        )
        db.add(session)
        db.commit()

        # Initialize initial world state (2026 Council: P5 + 10 elected members)
        initial_country_states = ensure_2026_country_states({
            "USA": {"stance": "SUPPORTIVE", "trust": 80, "demands": ["Allied security guarantees"]},
            "GBR": {"stance": "SUPPORTIVE", "trust": 85, "demands": ["E3 coordination"]},
            "RUS": {"stance": "CRITICAL", "trust": 40, "demands": ["No sanctions or Chapter VII intervention"]},
            "CHN": {"stance": "CAUTIOUS", "trust": 55, "demands": ["Protection of sovereign trade and dialogue"]},
            "SOM": {"stance": "CONDITIONAL", "trust": 65, "demands": ["Immediate humanitarian relief without preconditions", "African Union mediation primacy"]}
        })
        initial_vote = compute_coalition_and_vote(initial_country_states)
        initial_world_state = SimulationWorldState(
            session_id=session_id,
            turn=1,
            crisis_level=68,
            escalation_level=55,
            diplomatic_tension=60,
            humanitarian_status="SEVERE",
            economic_status="DISRUPTED",
            france_reputation=80,
            france_credibility=85,
            country_states=initial_country_states,
            coalition_status=initial_vote["coalition_status"],
            projected_vote=initial_vote["projected_vote"],
            france_promises=[],
            france_concessions=[],
            draft_resolution_on_table={},
            hidden_scenario_variables={"russian_true_redline": "Sanctions trigger immediate veto"},
            summary_of_turn="Turn 1: Crisis initialized. Council members await France's initial consultation move."
        )
        db.add(initial_world_state)
        
        # Add welcome intelligence message to bilateral inbox
        init_cable = DiplomaticMessage(
            session_id=session_id,
            sender="USA",
            recipient="FRANCE",
            message_type="BILATERAL",
            content="Ambassador, Washington stands ready to coordinate on a joint P3 response to this crisis. We urge Paris to ensure counter-terrorism and regional allied defense provisions are strongly framed.",
            turn=1,
            label="SIMULATION",
            reaction_mood="RECEPTIVE"
        )
        db.add(init_cable)
        db.commit()

        return session

    async def execute_action(self, db: Session, session_id: str, action_data: Dict[str, Any]) -> Dict[str, Any]:
        session = db.query(SimulationSession).filter(SimulationSession.session_id == session_id).first()
        if not session:
            raise ValueError("Session not found")

        scenario = db.query(CrisisScenario).filter(CrisisScenario.scenario_id == session.scenario_id).first()
        scenario_dict = {
            "title": scenario.title if scenario else "Regional Security Crisis",
            "initial_situation": scenario.initial_situation if scenario else "",
            "difficulty": session.difficulty
        }

        last_action = db.query(SimulationActionLog).filter(
            SimulationActionLog.session_id == session_id
        ).order_by(SimulationActionLog.turn.desc()).first()

        # Latest world state
        latest_state_record = db.query(SimulationWorldState).filter(
            SimulationWorldState.session_id == session_id
        ).order_by(SimulationWorldState.turn.desc()).first()

        current_state_dict = {
            "turn": latest_state_record.turn if latest_state_record else 1,
            "crisis_level": latest_state_record.crisis_level if latest_state_record else 65,
            "escalation_level": latest_state_record.escalation_level if latest_state_record else 50,
            "diplomatic_tension": latest_state_record.diplomatic_tension if latest_state_record else 60,
            "france_reputation": latest_state_record.france_reputation if latest_state_record else 75,
            "france_credibility": latest_state_record.france_credibility if latest_state_record else 80,
            "humanitarian_status": latest_state_record.humanitarian_status if latest_state_record else "SEVERE",
            "economic_status": latest_state_record.economic_status if latest_state_record else "DISRUPTED",
            "france_promises": latest_state_record.france_promises if latest_state_record else [],
            "france_concessions": latest_state_record.france_concessions if latest_state_record else [],
            "last_action_type": last_action.action_type if last_action else None,
            "country_states": latest_state_record.country_states if latest_state_record else {},
            "coalition_status": latest_state_record.coalition_status if latest_state_record else {},
            "projected_vote": latest_state_record.projected_vote if latest_state_record else {}
        }

        # Orchestrate next turn with Agent 4
        result = await self.orchestrator.advance_simulation_turn(
            current_world_state=current_state_dict,
            scenario_context=scenario_dict,
            france_action=action_data
        )

        new_state = result["updated_world_state"]
        new_turn = new_state["turn"]
        session.current_turn = new_turn

        # Persist new world state
        new_state_record = SimulationWorldState(
            session_id=session_id,
            turn=new_turn,
            crisis_level=new_state["crisis_level"],
            escalation_level=new_state["escalation_level"],
            diplomatic_tension=new_state["diplomatic_tension"],
            humanitarian_status=new_state["humanitarian_status"],
            economic_status=new_state["economic_status"],
            france_reputation=new_state["france_reputation"],
            france_credibility=new_state["france_credibility"],
            country_states=new_state["country_states"],
            coalition_status=new_state["coalition_status"],
            projected_vote=new_state["projected_vote"],
            france_promises=new_state["france_promises"],
            france_concessions=new_state["france_concessions"],
            summary_of_turn=result["turn_summary"]
        )
        db.add(new_state_record)

        # Record action log with authority validation
        action_log = SimulationActionLog(
            session_id=session_id,
            turn=new_turn,
            action_type=action_data.get("action_type", ""),
            action_details=action_data.get("parameters", {}),
            authority_status=result.get("authority_status", "ALLOWED"),
            authority_rationale=result.get("authority_rationale", ""),
            outcome_summary=result["turn_summary"],
            consequences=[f"Escalation shifted to {result['updated_world_state']['escalation_level']}"]
        )
        db.add(action_log)

        # Record target country cable
        primary = result.get("primary_reaction", {})
        if primary:
            msg = DiplomaticMessage(
                session_id=session_id,
                sender=primary.get("country_code", "USA"),
                recipient="FRANCE",
                message_type="BILATERAL",
                content=primary.get("diplomatic_cable_response", ""),
                turn=new_turn,
                label="SIMULATION",
                reaction_mood=primary.get("current_stance", "CAUTIOUS")
            )
            db.add(msg)

        db.commit()
        return result

    def send_bilateral_message(self, db: Session, session_id: str, recipient: str, content: str) -> DiplomaticMessage:
        session = db.query(SimulationSession).filter(SimulationSession.session_id == session_id).first()
        if not session:
            raise ValueError("Session not found")
        msg = DiplomaticMessage(
            session_id=session_id,
            sender="FRANCE",
            recipient=recipient,
            message_type="BILATERAL",
            content=content,
            turn=session.current_turn,
            label="SIMULATION",
            reaction_mood="RECEPTIVE"
        )
        db.add(msg)
        db.commit()
        db.refresh(msg)
        return msg

    def create_what_if_branch(self, db: Session, source_session_id: str, target_turn: int, alt_action: str) -> SimulationSession:
        """Section 62 Replay & What-If Branching."""
        orig_session = db.query(SimulationSession).filter(SimulationSession.session_id == source_session_id).first()
        if not orig_session:
            raise ValueError("Session not found")
        new_session_id = f"branch-{uuid.uuid4().hex[:8]}"

        branch_session = SimulationSession(
            session_id=new_session_id,
            scenario_id=orig_session.scenario_id,
            mode=orig_session.mode,
            difficulty=orig_session.difficulty,
            year=orig_session.year,
            current_turn=target_turn,
            status="ACTIVE",
            parent_session_id=source_session_id,
            branch_notes=f"Branch forked at turn {target_turn} with alternative action: {alt_action}"
        )
        db.add(branch_session)

        # Copy state at that turn
        target_state = db.query(SimulationWorldState).filter(
            SimulationWorldState.session_id == source_session_id,
            SimulationWorldState.turn == target_turn
        ).first()

        if target_state:
            forked_state = SimulationWorldState(
                session_id=new_session_id,
                turn=target_turn,
                crisis_level=target_state.crisis_level,
                escalation_level=target_state.escalation_level,
                diplomatic_tension=target_state.diplomatic_tension,
                france_reputation=target_state.france_reputation,
                country_states=target_state.country_states,
                coalition_status=target_state.coalition_status,
                projected_vote=target_state.projected_vote,
                summary_of_turn=f"Branch initialized at turn {target_turn}."
            )
            db.add(forked_state)

        db.commit()
        return branch_session
