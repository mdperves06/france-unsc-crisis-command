from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.intelligence_service import IntelligenceService
from app.schemas.intelligence import (
    IntelligenceSourceSchema,
    NewsClusterSchema,
    GlobalAlertSchema,
    RegionCommandProfileSchema
)

router = APIRouter(prefix="/intelligence", tags=["World Intelligence"])

@router.get("/sources", response_model=List[IntelligenceSourceSchema])
def get_sources(region: Optional[str] = Query(None), limit: int = 50, db: Session = Depends(get_db)):
    return IntelligenceService.get_sources(db, region=region, limit=limit)

@router.get("/clusters", response_model=List[NewsClusterSchema])
def get_news_clusters(region: Optional[str] = Query(None), db: Session = Depends(get_db)):
    return IntelligenceService.get_news_clusters(db, region=region)

@router.get("/alerts", response_model=List[GlobalAlertSchema])
def get_global_alerts(active_only: bool = True, db: Session = Depends(get_db)):
    return IntelligenceService.get_global_alerts(db, active_only=active_only)

@router.get("/regions", response_model=List[RegionCommandProfileSchema])
def get_regions(db: Session = Depends(get_db)):
    return IntelligenceService.get_all_regions(db)

@router.get("/regions/{region_id}", response_model=RegionCommandProfileSchema)
def get_region_profile(region_id: str, db: Session = Depends(get_db)):
    profile = IntelligenceService.get_region_profile(db, region_id=region_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Region profile not found")
    return profile
