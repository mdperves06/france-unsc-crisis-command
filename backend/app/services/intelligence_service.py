import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.intelligence import IntelligenceSource, NewsCluster, GlobalAlert, RegionCommandProfile

class IntelligenceService:
    @staticmethod
    def get_sources(db: Session, region: Optional[str] = None, limit: int = 50) -> List[IntelligenceSource]:
        query = db.query(IntelligenceSource)
        if region and region != "Global":
            query = query.filter(IntelligenceSource.region == region)
        return query.order_by(IntelligenceSource.publication_date.desc()).limit(limit).all()

    @staticmethod
    def get_news_clusters(db: Session, region: Optional[str] = None) -> List[NewsCluster]:
        query = db.query(NewsCluster)
        if region and region != "Global":
            query = query.filter(NewsCluster.region == region)
        return query.order_by(NewsCluster.updated_at.desc()).all()

    @staticmethod
    def get_global_alerts(db: Session, active_only: bool = True) -> List[GlobalAlert]:
        query = db.query(GlobalAlert)
        if active_only:
            query = query.filter(GlobalAlert.active == True)
        return query.order_by(GlobalAlert.timestamp.desc()).all()

    @staticmethod
    def get_region_profile(db: Session, region_id: str) -> Optional[RegionCommandProfile]:
        return db.query(RegionCommandProfile).filter(RegionCommandProfile.region_id == region_id).first()

    @staticmethod
    def get_all_regions(db: Session) -> List[RegionCommandProfile]:
        return db.query(RegionCommandProfile).all()
