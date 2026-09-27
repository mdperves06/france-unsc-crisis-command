import json
import logging
from typing import Dict, Any, List, Optional
from app.ai.agents.base_agent import BaseAgent
from app.schemas.ai import LLMMessage, FranceCoachAdvice, PanicBreakdown

logger = logging.getLogger(__name__)

class FranceStrategyCoach(BaseAgent):
    """
    AGENT 3 — FRANCE STRATEGY COACH
    Responsibilities:
    - France-centric strategic analysis & Quai d'Orsay diplomatic doctrine
    - Socratic pedagogical questioning (14-step framework)
    - Progressive hint engine (Hints 1 to 6)
    - "I Don't Know What To Do" Emergency Panic breakdown
    - Speech & Resolution rubric analysis
    - EB / Chair attack simulation
    """
    def __init__(self):
        super().__init__(agent_name="France Strategy Coach", agent_type="coach")

    async def get_strategic_coaching(
        self,
        crisis_title: str,
        crisis_summary: str,
        current_state: Dict[str, Any]
    ) -> FranceCoachAdvice:
        prompt = f"""
You are the Senior Diplomatic Coach to the French Delegation at the UN Security Council.
Crisis: {crisis_title}
Situation: {crisis_summary}
World State Escalation: {current_state.get('escalation_level', 50)}/100
France Reputation: {current_state.get('france_reputation', 75)}/100

Break down the dilemma strictly following the France Diplomatic Strategic Framework:
1. WHAT IS HAPPENING?
2. WHAT DOES FRANCE WANT?
3. WHY DOES FRANCE CARE?
4. WHAT CAN FRANCE ACTUALLY DO? (Legal/Diplomatic authority)
5. WHO MATTERS?
6. WHO CAN BLOCK IT? (P5 veto or 9-vote math)
7. WHAT CAN FRANCE OFFER?
8. WHAT SHOULD FRANCE ASK FOR?
9. WHAT IS THE MAIN RISK?
10. WHAT IS THE BACKUP?
11. SUGGESTED DIPLOMATIC LANGUAGE

Teach trade-offs. Never say there is only one valid option.
"""
        messages = [
            LLMMessage(role="system", content="You are a veteran French ambassador to the UN, steeped in international law, multilateralism, and strategic diplomacy."),
            LLMMessage(role="user", content=prompt)
        ]

        structured = await self.provider.structured_generate(messages, FranceCoachAdvice)
        if structured:
            return structured

        # High-Fidelity Fallback
        return FranceCoachAdvice(
            what_is_happening=f"Escalating security crisis in {crisis_title} threatening regional peace and civilian safety.",
            what_france_wants="A multilateral de-escalation pathway under UN Charter Chapter VI/VII that preserves international law, humanitarian access, and European security interests.",
            why_france_cares="As a P5 member and EU pillar, France carries legal responsibility under Article 24 of the UN Charter and holds strategic regional security partnerships.",
            what_france_can_do=[
                "Request formal emergency consultations of the UNSC (Rule 2 provisional rules of procedure)",
                "Propose an E3 (France, UK, Germany) joint diplomatic demarche",
                "Table a draft resolution authorizing a humanitarian corridor and UN monitoring mechanism",
                "Coordinate with the African Union or regional bodies under Chapter VIII"
            ],
            who_matters=["USA (NATO ally, deterrence)", "Russia (P5 veto power)", "China (sovereignty advocate, trade corridors)", "A3+1 African elected members (swing votes)"],
            who_can_block=["Russia (veto threat on coercive mandates)", "China (veto threat on intrusive sovereignty violations)"],
            what_france_can_offer=[
                "Phased humanitarian-first text without immediate Chapter VII sanctions",
                "Neutral third-party UN observers rather than Western military deployment",
                "Language affirming host-nation territorial integrity"
            ],
            what_france_should_ask=[
                "Immediate binding cessation of hostilities",
                "Unrestricted humanitarian relief corridors for OCHA/ICRC",
                "Secretary-General special envoy appointment"
            ],
            main_risks=["A swift Russian or Chinese veto leaving the Council paralyzed", "Allied division between Paris and Washington over enforcement speed"],
            backup_options=[
                "Presidential Statement (PRST) adopted by consensus if a resolution is blocked",
                "Referral to UN General Assembly under 'Uniting for Peace' (Res 377A)"
            ],
            suggested_diplomatic_language="France solemnly calls upon all members of this Council to uphold their primary responsibility under Article 24. No state can hide behind procedural obstruction while civilian lives hang in the balance.",
            recommended_action="Initiate private bilateral consultations with Washington and Beijing before tabbing the draft resolution."
        )

    async def get_panic_breakdown(
        self,
        crisis_title: str,
        crisis_summary: str,
        actors: List[str]
    ) -> PanicBreakdown:
        """Section 17 'I DON'T KNOW WHAT TO DO' emergency rescue breakdown."""
        prompt = f"""
A Model UN delegate representing France is completely confused and panicked.
Crisis: {crisis_title}
Context: {crisis_summary}
Actors: {', '.join(actors)}

Provide an immediate, crystalline pedagogical breakdown:
1. Crisis in exactly 3 short sentences.
2. Immediate threat.
3. France's core interest.
4. Top 3 actors to consider.
5. Three viable strategic paths with their specific trade-offs.
6. Exactly ONE decisive question for the user to answer to get unstuck.
"""
        messages = [
            LLMMessage(role="system", content="You are a supportive, razor-sharp diplomatic coach helping a panicked delegate regain clarity."),
            LLMMessage(role="user", content=prompt)
        ]
        
        structured = await self.provider.structured_generate(messages, PanicBreakdown)
        if structured:
            return structured

        return PanicBreakdown(
            crisis_in_3_sentences="Hostilities have flared up, threatening an acute regional conflict. Civilian infrastructure is cut off, and opposing military forces are mobilizing. The Security Council is divided between Western interventionists and Eastern non-interference defenders.",
            immediate_threat="Imminent collapse of humanitarian corridors and uncontrolled military escalation beyond national borders.",
            france_core_interest="Protecting international humanitarian law, preventing P5 paralysis, and sustaining European strategic autonomy.",
            top_3_actors_to_consider=["USA", "Russia", "Regional Swing Elected Members"],
            three_strategic_paths=[
                {
                    "path": "Lead with a strict Humanitarian Resolution (Focus on corridors and medical aid)",
                    "tradeoff": "High chance of passing without a Russian/Chinese veto, but fails to address underlying military confrontation."
                },
                {
                    "path": "Build a P3 Western Bloc (France, UK, USA) demanding robust Chapter VII compliance",
                    "tradeoff": "Demonstrates decisive leadership and deterrence, but almost guarantees a Russian veto."
                },
                {
                    "path": "Bridge Builder with the A3/E10 (Coordinate through elected members for a compromise PRST)",
                    "tradeoff": "Bypasses immediate veto risks and secures 9+ votes, but results in softer diplomatic language."
                }
            ],
            one_critical_question="Do you want to force a public showdown on principles (risking a veto), or secure a practical humanitarian pause on the ground first?"
        )

    def get_progressive_hint(self, hint_level: int, crisis_context: Dict[str, Any]) -> Dict[str, str]:
        """Section 18 Progressive Hint System (Hints 1 to 6)"""
        hints = {
            1: {
                "question": "What is the immediate threat?",
                "guidance": "Look at what is physically changing on the ground right now. Is it a missile strike, a humanitarian blockade, or a diplomatic deadline?"
            },
            2: {
                "question": "What does France gain or lose?",
                "guidance": "Consider France's core stakes: EU border security, French nationals abroad, credibility as an independent P5 bridge-builder, or international legal norms."
            },
            3: {
                "question": "Who can block your preferred outcome?",
                "guidance": "Remember UNSC Article 27: Any P5 member (USA, RUS, CHN, GBR, FRA) can cast a negative vote to kill a substantive resolution, and you need at least 9 affirmative votes."
            },
            4: {
                "question": "What can you offer that actor?",
                "guidance": "If Russia or China fears Western regime change or unilateral sanctions, can you offer neutral UN monitoring or phased humanitarian carve-outs instead?"
            },
            5: {
                "question": "What is your fallback if negotiations stall?",
                "guidance": "If a binding Chapter VII resolution is doomed, can you pivot to a Presidential Statement (PRST), a Press Elements release, or a bilateral diplomatic demarche?"
            },
            6: {
                "question": "What would happen if your proposal fails publicly?",
                "guidance": "A vetoed French draft signals Council impotence. Ensure you have consulted at least 5 elected members and secured London's co-sponsorship before calling for a vote."
            }
        }
        return hints.get(hint_level, hints[1])
