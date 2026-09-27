import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class UNSCMember(Base):
    __tablename__ = "unsc_members"

    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(String(3), index=True) # e.g. FRA, USA, GBR, RUS, CHN
    name = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False) # PERMANENT or ELECTED
    term_start = Column(Integer, nullable=False) # Year e.g. 1945, 2026
    term_end = Column(Integer, nullable=True) # Null for P5, or ending year
    region_group = Column(String(50)) # WEOG, Eastern Europe, GRULAC, Asia-Pacific, African Group
    has_veto = Column(Boolean, default=False)
    strategic_profile = Column(JSON, default=dict) # Key diplomatic priorities, typical positions

class UNSCPresidency(Base):
    __tablename__ = "unsc_presidencies"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False) # 1-12
    country_code = Column(String(3), nullable=False)
    country_name = Column(String(100), nullable=False)
    signature_theme = Column(String(255), nullable=True)

class UNSCResolution(Base):
    __tablename__ = "unsc_resolutions"

    id = Column(Integer, primary_key=True, index=True)
    resolution_number = Column(String(50), unique=True, index=True) # e.g. S/RES/2728 (2024)
    code = Column(String(50))
    title = Column(String(255), nullable=False)
    date_adopted = Column(DateTime, nullable=False)
    agenda_item = Column(String(255), nullable=False)
    chapter_vii = Column(Boolean, default=False)
    operative_summary = Column(Text, nullable=False)
    full_text_url = Column(String(255), nullable=True)
    yes_votes = Column(Integer, default=0)
    no_votes = Column(Integer, default=0)
    abstentions = Column(Integer, default=0)
    outcome = Column(String(50), default="ADOPTED") # ADOPTED, VETOED, REJECTED
    france_vote = Column(String(10), default="YES") # YES, NO, ABSTAIN
    source_url = Column(String(255), nullable=False)

    votes = relationship("UNSCVote", back_populates="resolution")

class UNSCVote(Base):
    __tablename__ = "unsc_votes"

    id = Column(Integer, primary_key=True, index=True)
    resolution_id = Column(Integer, ForeignKey("unsc_resolutions.id"), nullable=True)
    draft_symbol = Column(String(50), index=True) # e.g. S/2024/254
    meeting_number = Column(String(50))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    agenda_item = Column(String(255))
    country_code = Column(String(3), nullable=False)
    vote = Column(String(15), nullable=False) # YES, NO, ABSTAIN, ABSENT
    is_veto = Column(Boolean, default=False)
    explanation_of_vote = Column(Text, nullable=True)
    source = Column(String(255), nullable=False)

    resolution = relationship("UNSCResolution", back_populates="votes")

class UNSCMeetingRecord(Base):
    __tablename__ = "unsc_meeting_records"

    id = Column(Integer, primary_key=True, index=True)
    meeting_symbol = Column(String(50), unique=True, index=True) # e.g. S/PV.9580
    date = Column(DateTime, nullable=False)
    topic = Column(String(255), nullable=False)
    official_record_url = Column(String(255))
    summary = Column(Text)
    france_statement_summary = Column(Text)

class PeacekeepingMission(Base):
    __tablename__ = "peacekeeping_missions"

    id = Column(Integer, primary_key=True, index=True)
    acronym = Column(String(30), unique=True) # e.g. UNIFIL, MINUSCA, MONUSCO
    name = Column(String(255), nullable=False)
    country_or_region = Column(String(100), nullable=False)
    mandate_summary = Column(Text, nullable=False)
    current_personnel = Column(Integer, default=0)
    france_contribution = Column(Text)
    unsc_resolution_basis = Column(String(100))
    status = Column(String(30), default="ACTIVE")
