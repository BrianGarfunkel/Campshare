from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.crud.camping_trip import (
    create_camping_trip, get_camping_trips_by_user, get_friend_camping_feed,
    get_camping_trip, update_camping_trip, delete_camping_trip,
    get_camping_trips_for_map
)
from app.schemas.camping_trip import CampingTrip, CampingTripCreate, CampingTripUpdate, CampingTripWithCampground
from app.schemas.user import User

router = APIRouter()


@router.post("/", response_model=CampingTrip)
def log_camping_trip(
    camping_trip: CampingTripCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Log a new camping trip."""
    return create_camping_trip(db=db, camping_trip=camping_trip, user_id=current_user.id)


@router.get("/my-trips", response_model=List[CampingTrip])
def get_my_camping_trips(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's camping trips."""
    return get_camping_trips_by_user(db=db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/feed", response_model=List[CampingTrip])
def get_friend_camping_feed_trips(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get friend camping feed (camping trips from other users)."""
    return get_friend_camping_feed(db=db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/map", response_model=List[dict])
def get_camping_trips_for_map_view(
    include_own: bool = Query(True, description="Include user's own trips"),
    include_friends: bool = Query(True, description="Include friends' trips"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get camping trips for interactive map display with filtering options."""
    trips = get_camping_trips_for_map(
        db, 
        current_user.id, 
        include_own=include_own, 
        include_friends=include_friends
    )
    return trips


@router.get("/{trip_id}", response_model=CampingTrip)
def get_camping_trip_by_id(
    trip_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific camping trip by ID."""
    camping_trip = get_camping_trip(db=db, trip_id=trip_id)
    if camping_trip is None:
        raise HTTPException(status_code=404, detail="Camping trip not found")
    return camping_trip


@router.put("/{trip_id}", response_model=CampingTrip)
def update_camping_trip_by_id(
    trip_id: int,
    camping_trip_update: CampingTripUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a camping trip (only if it belongs to the current user)."""
    camping_trip = get_camping_trip(db=db, trip_id=trip_id)
    if camping_trip is None:
        raise HTTPException(status_code=404, detail="Camping trip not found")
    
    if camping_trip.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this camping trip")
    
    return update_camping_trip(db=db, trip_id=trip_id, camping_trip_update=camping_trip_update)


@router.delete("/{trip_id}")
def delete_camping_trip_by_id(
    trip_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a camping trip (only if it belongs to the current user)."""
    camping_trip = get_camping_trip(db=db, trip_id=trip_id)
    if camping_trip is None:
        raise HTTPException(status_code=404, detail="Camping trip not found")
    
    if camping_trip.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this camping trip")
    
    success = delete_camping_trip(db=db, trip_id=trip_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete camping trip")
    
    return {"message": "Camping trip deleted successfully"}
