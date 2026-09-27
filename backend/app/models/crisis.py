import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, JSON
from app.core.database import Base

class CrisisScenario(Base):
    __tablename__ = "crisis_scenarios"

    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(String(100), unique=True, index=True)
    title = Column(String(255), nullable=False)
    region = Column(String(50), nullable=False)
    crisis_type = Column(String(50), nullable=False) # Diplomatic, Military, Humanitarian, Nuclear, Maritime, etc.
    difficulty = Column(String(30), default="Intermediate") # Beginner, Intermediate, Advanced, Expert, Chair Pressure, Final Boss
    
    # Overview
    initial_situation = Column(Text, nullable=False)
    location_details = Column(String(255), nullable=False)
    coordinates = Column(JSON, default=dict) # {lat: ..., lng: ...}
    background = Column(Text, nullable=False)
    known_facts = Column(JSON, default=list) # [{fact: "...", status: "VERIFIED FACT"}]
    unknown_facts = Column(JSON, default=list) # Uncertainty elements
    
    # Actors and interests
    key_actors = Column(JSON, default=list) # List of country codes and non-state actors
    actor_initial_stances = Column(JSON, default=dict)
    
    # France Specific Analysis
    france_interest = Column(Text, nullable=False)
    france_immediate_threat = Column(Text, nullable=False)
    france_objectives = Column(JSON, default=list)
    france_red_lines = Column(JSON, default=list)
    available_tools = Column(JSON, default=list)
    
    # Strategic Paths & Tradeoffs
    strategic_paths = Column(JSON, default=list) # 3 viable strategic avenues with pros/cons
    
    # Twists and escalation paths
    escalation_paths = Column(JSON, default=list)
    deescalation_paths = Column(JSON, default=list)
    hidden_scenario_variables = Column(JSON, default=dict)
    
    is_custom_or_imported = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class CrisisEvent(Base):
    """Dynamic Crisis Event Engine (Section 27)"""
    __tablename__ = "crisis_events"

    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(String(100), index=True)
    event_order = Column(Integer, default=1)
    trigger_condition = Column(String(100), default="TURN_ADVANCE") # TURN_ADVANCE, ACTOR_PROVOCATION, RESOLUTION_FILED
    headline = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    event_type = Column(String(50)) # border_incident, missile_strike, ceasefire_collapse, leak, etc.
    impact_escalation = Column(Integer, default=10) # Change to escalation index
    impact_humanitarian = Column(Integer, default=5)
    source_attribution = Column(String(50), default="SIMULATION")
