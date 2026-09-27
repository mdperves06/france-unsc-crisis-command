from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.unsc_service import UNSCService
from app.schemas.unsc import UNSCMemberSchema, UNSCPresidencySchema, UNSCResolutionSchema, UNSCVoteSchema

router = APIRouter(prefix="/unsc", tags=["UNSC Database"])

@router.get("/members", response_model=List[UNSCMemberSchema])
def get_members(year: Optional[int] = Query(2026, description="UNSC membership year"), db: Session = Depends(get_db)):
    return UNSCService.get_members(db, year=year)

@router.get("/presidencies", response_model=List[UNSCPresidencySchema])
def get_presidencies(year: Optional[int] = Query(2026), db: Session = Depends(get_db)):
    return UNSCService.get_presidencies(db, year=year)

@router.get("/resolutions", response_model=List[UNSCResolutionSchema])
def get_resolutions(topic: Optional[str] = None, limit: int = 50, db: Session = Depends(get_db)):
    return UNSCService.get_resolutions(db, limit=limit, topic=topic)

@router.get("/votes", response_model=List[UNSCVoteSchema])
def get_votes(resolution_id: Optional[int] = None, country_code: Optional[str] = None, db: Session = Depends(get_db)):
    return UNSCService.get_votes(db, resolution_id=resolution_id, country_code=country_code)

@router.get("/vetoes", response_model=List[UNSCVoteSchema])
def get_vetoes(db: Session = Depends(get_db)):
    return UNSCService.get_vetoes(db)
