from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.unsc import UNSCMember, UNSCPresidency, UNSCResolution, UNSCVote, UNSCMeetingRecord, PeacekeepingMission

class UNSCService:
    @staticmethod
    def get_members(db: Session, year: Optional[int] = 2026) -> List[UNSCMember]:
        query = db.query(UNSCMember)
        if year:
            # P5 has term_end None; Elected members must have year between term_start and term_end
            query = query.filter(
                (UNSCMember.status == "PERMANENT") |
                ((UNSCMember.term_start <= year) & ((UNSCMember.term_end >= year) | (UNSCMember.term_end == None)))
            )
        return query.all()

    @staticmethod
    def get_presidencies(db: Session, year: Optional[int] = 2026) -> List[UNSCPresidency]:
        query = db.query(UNSCPresidency)
        if year:
            query = query.filter(UNSCPresidency.year == year)
        return query.order_by(UNSCPresidency.month.asc()).all()

    @staticmethod
    def get_resolutions(db: Session, limit: int = 50, topic: Optional[str] = None) -> List[UNSCResolution]:
        query = db.query(UNSCResolution)
        if topic:
            query = query.filter(UNSCResolution.agenda_item.ilike(f"%{topic}%"))
        return query.order_by(UNSCResolution.date_adopted.desc()).limit(limit).all()

    @staticmethod
    def get_votes(db: Session, resolution_id: Optional[int] = None, country_code: Optional[str] = None) -> List[UNSCVote]:
        query = db.query(UNSCVote)
        if resolution_id:
            query = query.filter(UNSCVote.resolution_id == resolution_id)
        if country_code:
            query = query.filter(UNSCVote.country_code == country_code)
        return query.order_by(UNSCVote.date.desc()).all()

    @staticmethod
    def get_vetoes(db: Session) -> List[UNSCVote]:
        return db.query(UNSCVote).filter(UNSCVote.is_veto == True).order_by(UNSCVote.date.desc()).all()

    @staticmethod
    def get_peacekeeping_missions(db: Session) -> List[PeacekeepingMission]:
        return db.query(PeacekeepingMission).all()
