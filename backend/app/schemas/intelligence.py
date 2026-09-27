from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class IntelligenceSourceSchema(BaseModel):
    id: int
    source_id: str
    title: str
    publisher: str
    source_type: str
    url: str
    publication_date: datetime
    region: str
    country: Optional[str]
    topic: str
    verification_status: str
    confidence_score: float
    summary: str

    class Config:
        from_attributes = True

class NewsClusterSchema(BaseModel):
    id: int
    cluster_title: str
    region: str
    primary_event_summary: str
    primary_source_id: str
    associated_source_ids: List[str]
    conflicting_reporting: Optional[str]
    unsc_relevance_notes: Optional[str]
    france_relevance_notes: Optional[str]
    updated_at: datetime

    class Config:
        from_attributes = True

class GlobalAlertSchema(BaseModel):
    id: int
    alert_type: str
    severity: str
    headline: str
    details: str
    region: str
    country_code: Optional[str]
    source_url: str
    timestamp: datetime
    active: bool

    class Config:
        from_attributes = True

class RegionCommandProfileSchema(BaseModel):
    id: int
    region_id: str
    name: str
    current_situation: str
    france_historical_role: str
    france_current_relevance: str
    unsc_involvement_summary: str
    escalation_risks: List[str]
    deescalation_opportunities: List[str]
    humanitarian_status: Optional[str]
    economic_dimension: Optional[str]
    legal_dimension: Optional[str]
    major_actors: List[Dict[str, Any]]
    key_resolutions: List[str]
    coordinates: Dict[str, float]

    class Config:
        from_attributes = True
