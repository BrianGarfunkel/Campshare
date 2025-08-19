from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.camping_trip import CampingTrip
from app.models.campground import Campground
from app.models.user import User
from app.crud.friend import get_friends
from app.schemas.camping_trip import CampingTripCreate, CampingTripUpdate
from typing import List, Optional


def get_camping_trip(db: Session, trip_id: int) -> Optional[CampingTrip]:
    """Get a camping trip by ID."""
    return db.query(CampingTrip).filter(CampingTrip.id == trip_id).first()


def get_camping_trips_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[CampingTrip]:
    """Get camping trips for a specific user."""
    return db.query(CampingTrip).filter(CampingTrip.user_id == user_id).offset(skip).limit(limit).all()


def get_all_camping_trips(db: Session, skip: int = 0, limit: int = 100) -> List[CampingTrip]:
    """Get all camping trips with pagination."""
    return db.query(CampingTrip).offset(skip).limit(limit).all()


def create_camping_trip(db: Session, camping_trip: CampingTripCreate, user_id: int) -> CampingTrip:
    """Create a new camping trip."""
    db_camping_trip = CampingTrip(**camping_trip.dict(), user_id=user_id)
    db.add(db_camping_trip)
    db.commit()
    db.refresh(db_camping_trip)
    return db_camping_trip


def update_camping_trip(db: Session, trip_id: int, camping_trip_update: CampingTripUpdate) -> Optional[CampingTrip]:
    """Update a camping trip."""
    db_camping_trip = get_camping_trip(db, trip_id)
    if not db_camping_trip:
        return None
    
    update_data = camping_trip_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_camping_trip, field, value)
    
    db.commit()
    db.refresh(db_camping_trip)
    return db_camping_trip


def delete_camping_trip(db: Session, trip_id: int) -> bool:
    """Delete a camping trip."""
    db_camping_trip = get_camping_trip(db, trip_id)
    if not db_camping_trip:
        return False
    
    db.delete(db_camping_trip)
    db.commit()
    return True


def get_friend_camping_feed(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[CampingTrip]:
    """Get camping trips from friends for the social feed"""
    # Get user's friends
    friends = get_friends(db, user_id)
    friend_ids = []
    for friend in friends:
        if friend.user_id == user_id:
            friend_ids.append(friend.friend_id)
        else:
            friend_ids.append(friend.user_id)
    
    if not friend_ids:
        return []
    
    # Get camping trips from friends
    return db.query(CampingTrip).filter(
        CampingTrip.user_id.in_(friend_ids)
    ).offset(skip).limit(limit).all()


def get_camping_trips_for_map(db: Session, user_id: int, include_own: bool = True, include_friends: bool = True) -> List[dict]:
    """Get camping trips for map display with user and campground info"""
    trips = []
    
    # Get user's friends
    friends = get_friends(db, user_id)
    friend_ids = []
    for friend in friends:
        if friend.user_id == user_id:
            friend_ids.append(friend.friend_id)
        else:
            friend_ids.append(friend.user_id)
    
    # Build query based on filters
    query = db.query(CampingTrip).join(Campground).join(User)
    
    if include_own and include_friends:
        # Include own trips and friends' trips
        query = query.filter(
            or_(
                CampingTrip.user_id == user_id,
                CampingTrip.user_id.in_(friend_ids)
            )
        )
    elif include_own:
        # Only own trips
        query = query.filter(CampingTrip.user_id == user_id)
    elif include_friends:
        # Only friends' trips
        query = query.filter(CampingTrip.user_id.in_(friend_ids))
    else:
        # No trips (shouldn't happen, but handle gracefully)
        return []
    
    camping_trips = query.all()
    
    for trip in camping_trips:
        # Determine if this is the user's own trip or a friend's trip
        is_own_trip = trip.user_id == user_id
        
        trips.append({
            "id": trip.id,
            "title": trip.title,
            "description": trip.description,
            "start_date": trip.start_date,
            "end_date": trip.end_date,
            "notes": trip.notes,
            "weather_conditions": trip.weather_conditions,
            "group_size": trip.group_size,
            "created_at": trip.created_at,
            "updated_at": trip.updated_at,
            "is_own_trip": is_own_trip,
            "user": {
                "id": trip.user.id,
                "username": trip.user.username,
                "full_name": trip.user.full_name
            },
            "campground": {
                "id": trip.campground.id,
                "name": trip.campground.name,
                "location": trip.campground.location,
                "description": trip.campground.description,
                "latitude": trip.campground.latitude,
                "longitude": trip.campground.longitude,
                "amenities": trip.campground.amenities
            }
        })
    
    return trips
