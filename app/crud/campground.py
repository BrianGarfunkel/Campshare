from sqlalchemy.orm import Session
from app.models.campground import Campground
from app.schemas.campground import CampgroundCreate
from typing import List, Optional


def get_campground(db: Session, campground_id: int) -> Optional[Campground]:
    """Get a campground by ID."""
    return db.query(Campground).filter(Campground.id == campground_id).first()


def get_campground_by_external_id(db: Session, external_id: str) -> Optional[Campground]:
    """Get a campground by external API ID."""
    return db.query(Campground).filter(Campground.external_id == external_id).first()


def get_campgrounds(db: Session, skip: int = 0, limit: int = 100) -> List[Campground]:
    """Get multiple campgrounds with pagination."""
    return db.query(Campground).offset(skip).limit(limit).all()


def search_campgrounds(db: Session, query: str, skip: int = 0, limit: int = 10) -> List[Campground]:
    """Search campgrounds by name or location."""
    return db.query(Campground).filter(
        (Campground.name.ilike(f"%{query}%")) | 
        (Campground.location.ilike(f"%{query}%"))
    ).offset(skip).limit(limit).all()


def create_campground(db: Session, campground: CampgroundCreate) -> Campground:
    """Create a new campground."""
    db_campground = Campground(**campground.dict())
    db.add(db_campground)
    db.commit()
    db.refresh(db_campground)
    return db_campground


def create_campground_if_not_exists(db: Session, campground: CampgroundCreate) -> Campground:
    """Create a campground only if it doesn't already exist (by external_id)."""
    if campground.external_id:
        existing = get_campground_by_external_id(db, campground.external_id)
        if existing:
            return existing
    
    return create_campground(db, campground)
