import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, JSON
from app.core.database import Base

class IntelligenceSource(Base):
    __tablename__ = "intelligence_sources"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(String(100), unique=True, index=True)
    title = Column(String(255), nullable=False)
    publisher = Column(String(100), nullable=False) # UN News, Reuters, CrisisWatch, Quai d'Orsay
    source_type = Column(String(50), nullable=False) # PRIMARY_OFFICIAL, REPUTABLE_SECONDARY, RESEARCH_INSTITUTE
    url = Column(String(500), nullable=False)
    publication_date = Column(DateTime, nullable=False)
    retrieved_at = Column(DateTime, default=datetime.datetime.utcnow)
    region = Column(String(50), nullable=False) # Middle East, Eastern Europe, Sub-Saharan Africa, etc.
    country = Column(String(100), nullable=True)
    topic = Column(String(100), nullable=False) # Security, Humanitarian, Sanctions, Maritime, Peacekeeping
    
    # Strict Provenance & Verification
    # VERIFIED FACT, OFFICIAL STATEMENT, REPORTED, DISPUTED, UNCONFIRMED, ANALYSIS, SIMULATION, SCENARIO ASSUMPTION
    verification_status = Column(String(50), nullable=False, default="REPORTED")
    confidence_score = Column(Float, default=0.85) # 0.0 to 1.0
    summary = Column(Text, nullable=False)
    raw_content = Column(Text, nullable=True)

class NewsCluster(Base):
    """Event Deduplication and Clustering per Section 48 & 49"""
    __tablename__ = "news_clusters"

    id = Column(Integer, primary_key=True, index=True)
    cluster_title = Column(String(255), nullable=False)
    region = Column(String(50), nullable=False)
    primary_event_summary = Column(Text, nullable=False)
    primary_source_id = Column(String(100), nullable=False)
    associated_source_ids = Column(JSON, default=list) # List of source_ids
    conflicting_reporting = Column(Text, nullable=True)
    unsc_relevance_notes = Column(Text, nullable=True)
    france_relevance_notes = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class GlobalAlert(Base):
    """Section 50 Alert Engine"""
    __tablename__ = "global_alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String(50), nullable=False) # NEW_UNSC_VETO, CONFLICT_ESCALATION, FRANCE_STATEMENT, etc.
    severity = Column(String(20), default="HIGH") # CRITICAL, HIGH, MEDIUM, LOW
    headline = Column(String(255), nullable=False)
    details = Column(Text, nullable=False)
    region = Column(String(50), nullable=False)
    country_code = Column(String(3), nullable=True)
    source_url = Column(String(500), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    active = Column(Boolean, default=True)

class RegionCommandProfile(Base):
    """Section 8 & 67 Region Command Center Profile"""
    __tablename__ = "region_command_profiles"

    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(String(50), unique=True, index=True) # middle-east, eastern-europe, etc.
    name = Column(String(100), nullable=False)
    current_situation = Column(Text, nullable=False)
    france_historical_role = Column(Text, nullable=False)
    france_current_relevance = Column(Text, nullable=False)
    unsc_involvement_summary = Column(Text, nullable=False)
    escalation_risks = Column(JSON, default=list)
    deescalation_opportunities = Column(JSON, default=list)
    humanitarian_status = Column(Text, nullable=True)
    economic_dimension = Column(Text, nullable=True)
    legal_dimension = Column(Text, nullable=True)
    major_actors = Column(JSON, default=list)
    key_resolutions = Column(JSON, default=list)
    coordinates = Column(JSON, default=dict) # lat, lng, zoom for 3D globe focus
