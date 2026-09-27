import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class SimulationSession(Base):
    __tablename__ = "simulation_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True)
    scenario_id = Column(String(100), index=True)
    mode = Column(String(30), default="PRACTICE_ARENA") # CRISIS_TRAINER or PRACTICE_ARENA
    difficulty = Column(String(30), default="Intermediate")
    year = Column(Integer, default=2026)
    
    # State tracking
    current_turn = Column(Integer, default=1)
    status = Column(String(30), default="ACTIVE") # ACTIVE, CONCLUDED, ABANDONED
    parent_session_id = Column(String(100), nullable=True) # For What-If branches
    branch_notes = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    world_states = relationship("SimulationWorldState", back_populates="session", cascade="all, delete-orphan")
    diplomatic_messages = relationship("DiplomaticMessage", back_populates="session", cascade="all, delete-orphan")
    action_logs = relationship("SimulationActionLog", back_populates="session", cascade="all, delete-orphan")

class SimulationWorldState(Base):
    """Section 26 World State Engine"""
    __tablename__ = "simulation_world_states"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), ForeignKey("simulation_sessions.session_id"), index=True)
    turn = Column(Integer, default=1)
    
    crisis_level = Column(Integer, default=65) # 0 to 100
    escalation_level = Column(Integer, default=50) # 0 to 100
    diplomatic_tension = Column(Integer, default=60) # 0 to 100
    humanitarian_status = Column(String(50), default="SEVERE") # CRITICAL, SEVERE, DETERIORATING, STABLE
    economic_status = Column(String(50), default="DISRUPTED")
    
    # France metrics
    france_reputation = Column(Integer, default=75) # 0-100
    france_credibility = Column(Integer, default=80) # 0-100
    
    # Country stances dictionary: { "USA": { stance: "SUPPORTIVE", trust: 80, coalition: "SUPPORT", demands: [...] }, ... }
    country_states = Column(JSON, default=dict)
    
    # Coalitions: { "support": ["USA", "GBR"], "conditional": ["JPN", "KOR"], "undecided": [...], "opposed": ["RUS", "CHN"] }
    coalition_status = Column(JSON, default=dict)
    
    # Voting projection: { "yes": 9, "no": 2, "abstain": 4, "veto_threats": ["RUS"] }
    projected_vote = Column(JSON, default=dict)
    
    # Commitments, concessions and promises recorded
    france_promises = Column(JSON, default=list) # [{to: "RUS", promise: "no sanctions clause", broken: false}]
    france_concessions = Column(JSON, default=list)
    
    # Active resolutions on table
    draft_resolution_on_table = Column(JSON, default=dict)
    
    # Hidden scenario variables (revealed only in AAR)
    hidden_scenario_variables = Column(JSON, default=dict)
    
    summary_of_turn = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("SimulationSession", back_populates="world_states")

class DiplomaticMessage(Base):
    """Section 31 & 32 Diplomatic Chat & Private Negotiations"""
    __tablename__ = "diplomatic_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), ForeignKey("simulation_sessions.session_id"), index=True)
    sender = Column(String(50), nullable=False) # "FRANCE" or Country Code "USA", "RUS", "CHN", etc.
    recipient = Column(String(50), nullable=False) # "FRANCE" or Country Code
    message_type = Column(String(30), default="BILATERAL") # BILATERAL, MULTILATERAL, PUBLIC_STATEMENT, CAUCUS_NOTE
    content = Column(Text, nullable=False)
    turn = Column(Integer, default=1)
    
    # Simulation labels and diplomatic intent
    label = Column(String(30), default="SIMULATION")
    demands = Column(JSON, default=list)
    concessions_offered = Column(JSON, default=list)
    reaction_mood = Column(String(30), default="CAUTIOUS") # RECEPTIVE, CAUTIOUS, HOSTILE, FIRM
    
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("SimulationSession", back_populates="diplomatic_messages")

class SimulationActionLog(Base):
    """Section 20 & 21 Practice Actions & Action Authority Engine"""
    __tablename__ = "simulation_action_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), ForeignKey("simulation_sessions.session_id"), index=True)
    turn = Column(Integer, default=1)
    action_type = Column(String(50), nullable=False) # REQUEST_EMERGENCY_MEETING, CONTACT_USA, DRAFT_RESOLUTION, THREATEN_VETO, etc.
    action_details = Column(JSON, default=dict)
    
    authority_status = Column(String(30), default="ALLOWED") # ALLOWED, LIMITED, UNCERTAIN, NOT_AVAILABLE
    authority_rationale = Column(Text, nullable=False)
    
    outcome_summary = Column(Text, nullable=False)
    consequences = Column(JSON, default=list)
    state_delta = Column(JSON, default=dict) # {"escalation_level": -5, "france_reputation": +3}
    
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("SimulationSession", back_populates="action_logs")
