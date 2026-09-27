import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, JSON
from app.core.database import Base

class TrainingCurriculumModule(Base):
    """Section 39 France-Specific Training Academy (24 Modules)"""
    __tablename__ = "training_curriculum_modules"

    id = Column(Integer, primary_key=True, index=True)
    module_number = Column(Integer, unique=True, index=True) # 1 to 24
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False) # Foundation, Regional, Mechanism, Advanced
    description = Column(Text, nullable=False)
    core_doctrine = Column(Text, nullable=False)
    legal_basis = Column(Text, nullable=False)
    france_historical_cases = Column(JSON, default=list) # [{case: "Suez 1956", notes: "..."}]
    key_takeaways = Column(JSON, default=list)
    sources = Column(JSON, default=list) # [{title: "...", url: "..."}]
    unlocked = Column(Boolean, default=True)

class UserLearningProfile(Base):
    """Section 59 & 60 User Learning Memory and 16-Competency Performance Analytics"""
    __tablename__ = "user_learning_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), default="default_delegate", unique=True, index=True)
    
    # 16 Tracked Competencies (Score 0 - 100)
    crisis_analysis = Column(Float, default=50.0)
    strategic_reasoning = Column(Float, default=50.0)
    france_interest_id = Column(Float, default=50.0)
    diplomacy = Column(Float, default=50.0)
    negotiation = Column(Float, default=50.0)
    coalition_building = Column(Float, default=50.0)
    response_speed = Column(Float, default=50.0)
    evidence_use = Column(Float, default=50.0)
    legal_awareness = Column(Float, default=50.0)
    resolution_writing = Column(Float, default=50.0)
    speech_delivery = Column(Float, default=50.0)
    rebuttal_strength = Column(Float, default=50.0)
    adaptability = Column(Float, default=50.0)
    contingency_planning = Column(Float, default=50.0)
    portfolio_awareness = Column(Float, default=50.0)
    decision_consistency = Column(Float, default=50.0)
    
    # Qualitative insights & memory
    strong_areas = Column(JSON, default=list)
    weak_areas = Column(JSON, default=list)
    frequently_missed_actors = Column(JSON, default=list)
    frequently_missed_risks = Column(JSON, default=list)
    common_mistakes = Column(JSON, default=list)
    recommended_next_focus = Column(String(255), default="Coalition Building with Elected Members")
    
    completed_scenarios_count = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class SpeechEvaluation(Base):
    """Section 40 Speech Trainer"""
    __tablename__ = "speech_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    speech_type = Column(String(50), nullable=False) # OPENING, MOD_CAUCUS, CRISIS_SPEECH, PRESS_STMT, EMERGENCY
    speech_text = Column(Text, nullable=False)
    
    # Scores (0-10)
    clarity_score = Column(Float)
    france_relevance_score = Column(Float)
    structure_score = Column(Float)
    argument_score = Column(Float)
    evidence_score = Column(Float)
    diplomatic_tone_score = Column(Float)
    coalition_appeal_score = Column(Float)
    rebuttal_strength_score = Column(Float)
    overall_score = Column(Float)
    
    strengths = Column(JSON, default=list)
    areas_for_improvement = Column(JSON, default=list)
    actionable_revisions = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ResolutionEvaluation(Base):
    """Section 42 Resolution Lab"""
    __tablename__ = "resolution_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    document_type = Column(String(50), default="DRAFT_RESOLUTION") # DRAFT_RESOLUTION, PRST, PRESS_STATEMENT, DIRECTIVE
    title = Column(String(255), nullable=False)
    preambulatory_clauses = Column(JSON, default=list)
    operative_clauses = Column(JSON, default=list)
    
    # Validation checklist
    legal_authority_check = Column(String(50)) # VALID, DEFICIENT, VIOLATES_CHARTER
    legal_rationale = Column(Text)
    enforcement_feasibility = Column(String(50))
    financing_mechanism = Column(String(50))
    p5_objection_risks = Column(JSON, default=dict) # {"RUS": "Clause 4 sovereignty violation", ...}
    voting_viability_score = Column(Float) # 0 to 100
    suggested_amendments = Column(JSON, default=list)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AfterActionReviewRecord(Base):
    """Section 61 After Action Review (AAR)"""
    __tablename__ = "after_action_reviews"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True)
    what_user_did = Column(JSON, default=list)
    what_happened = Column(Text, nullable=False)
    why_it_happened = Column(Text, nullable=False)
    what_user_missed = Column(JSON, default=list)
    actors_misread = Column(JSON, default=list)
    assumptions_failed = Column(JSON, default=list)
    france_alternative_options = Column(JSON, default=list)
    unlocked_hidden_variables = Column(JSON, default=dict)
    next_practice_recommendation = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
