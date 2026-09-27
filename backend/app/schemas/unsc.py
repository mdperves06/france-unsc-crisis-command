from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class UNSCMemberSchema(BaseModel):
    id: int
    country_code: str
    name: str
    status: str
    term_start: int
    term_end: Optional[int]
    region_group: Optional[str]
    has_veto: bool
    strategic_profile: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

class UNSCPresidencySchema(BaseModel):
    year: int
    month: int
    country_code: str
    country_name: str
    signature_theme: Optional[str]

    class Config:
        from_attributes = True

class UNSCVoteSchema(BaseModel):
    id: int
    resolution_id: Optional[int]
    draft_symbol: Optional[str]
    meeting_number: Optional[str]
    date: datetime
    agenda_item: Optional[str]
    country_code: str
    vote: str
    is_veto: bool
    explanation_of_vote: Optional[str]
    source: str

    class Config:
        from_attributes = True

class UNSCResolutionSchema(BaseModel):
    id: int
    resolution_number: str
    code: Optional[str]
    title: str
    date_adopted: datetime
    agenda_item: str
    chapter_vii: bool
    operative_summary: str
    full_text_url: Optional[str]
    yes_votes: int
    no_votes: int
    abstentions: int
    outcome: str
    france_vote: str
    source_url: str

    class Config:
        from_attributes = True
