from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.core.api_service import outdoor_api
from app.crud.campground import create_campground_if_not_exists, get_campground, search_campgrounds
from app.schemas.campground import Campground, CampgroundCreate, CampgroundSearch
from app.schemas.user import User

router = APIRouter()


@router.get("/search", response_model=List[Campground])
async def search_campgrounds_api(
    q: str = Query(..., description="Search query for campgrounds"),
    limit: int = Query(10, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """Search for campgrounds using the external API."""
    # First search in our database
    db_results = search_campgrounds(db, q, limit=limit)
    
    # If we don't have enough results, search external API
    if len(db_results) < limit:
        api_results = await outdoor_api.search_campgrounds(q, limit - len(db_results))
        
        # Save new campgrounds to database
        for api_campground in api_results:
            campground_create = CampgroundCreate(**api_campground)
            create_campground_if_not_exists(db, campground_create)
        
        # Get updated database results
        db_results = search_campgrounds(db, q, limit=limit)
    
    return db_results


@router.get("/", response_model=List[Campground])
def get_campgrounds(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all campgrounds with pagination."""
    from app.crud.campground import get_campgrounds
    return get_campgrounds(db, skip=skip, limit=limit)


@router.get("/{campground_id}", response_model=Campground)
def get_campground_by_id(
    campground_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific campground by ID."""
    campground = get_campground(db, campground_id)
    if campground is None:
        raise HTTPException(status_code=404, detail="Campground not found")
    return campground
