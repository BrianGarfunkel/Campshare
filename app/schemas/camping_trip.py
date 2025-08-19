from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CampingTripBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    notes: Optional[str] = None
    weather_conditions: Optional[str] = None
    group_size: Optional[int] = None


class CampingTripCreate(CampingTripBase):
    campground_id: int


class CampingTripUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    notes: Optional[str] = None
    weather_conditions: Optional[str] = None
    group_size: Optional[int] = None


class CampingTripInDB(CampingTripBase):
    id: int
    user_id: int
    campground_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class CampingTrip(CampingTripInDB):
    pass


class CampingTripWithCampground(CampingTrip):
    campground: "CampgroundBase"
