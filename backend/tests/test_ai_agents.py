import sys
import pytest
sys.path.insert(0, 'backend')
from app.ai.agents.research_agent import GlobalResearchAgent
from app.ai.agents.country_agent import UNSCCountrySimulationAgent
from app.ai.agents.france_coach_agent import FranceStrategyCoach
from app.ai.agents.orchestrator import CrisisOrchestrator

@pytest.mark.asyncio
async def test_country_simulation_agent():
    agent = UNSCCountrySimulationAgent()
    # Test Russia simulation
    rus_reaction = await agent.generate_reaction(
        country_code="RUS",
        crisis_context="Armed confrontation along international corridor",
        france_action_or_message="France proposes Chapter VII sanctions and monitors",
        relationship_trust=40
    )
    assert rus_reaction.country_code == "RUS"
    assert rus_reaction.is_simulation is True
    assert rus_reaction.current_stance in ["CRITICAL", "OPPOSING", "CONDITIONAL"]
    assert len(rus_reaction.diplomatic_cable_response) > 20

@pytest.mark.asyncio
async def test_france_strategy_coach():
    coach = FranceStrategyCoach()
    panic = await coach.get_panic_breakdown(
        crisis_title="Maritime Chokepoint Confrontation",
        crisis_summary="Hostile forces have mined the strait and attacked commercial tankers.",
        actors=["USA", "RUS", "CHN", "FRA"]
    )
    assert len(panic.three_strategic_paths) == 3
    assert len(panic.one_critical_question) > 10

    # Progressive hint
    h1 = coach.get_progressive_hint(1, {})
    assert "immediate threat" in h1["question"].lower()
    h3 = coach.get_progressive_hint(3, {})
    assert "block" in h3["question"].lower()

@pytest.mark.asyncio
async def test_orchestrator_turn_flow():
    orchestrator = CrisisOrchestrator()
    init_state = {
        "turn": 1,
        "escalation_level": 50,
        "diplomatic_tension": 60,
        "france_reputation": 75,
        "country_states": {},
        "coalition_status": {}
    }
    result = await orchestrator.advance_simulation_turn(
        current_world_state=init_state,
        scenario_context={"initial_situation": "Tense border standoff"},
        france_action={"action_type": "REQUEST_EMERGENCY_MEETING", "target_country": "USA"}
    )
    assert result["updated_world_state"]["turn"] == 2
    assert "projected_vote" in result["updated_world_state"]
    assert result["authority_status"] == "ALLOWED"
