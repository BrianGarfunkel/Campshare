from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CampgroundBase(BaseModel):
    name: str
    location: str
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    amenities: Optional[str] = None
    max_capacity: Optional[int] = None
    has_electricity: Optional[bool] = False
    has_water: Optional[bool] = False
    has_showers: Optional[bool] = False
    has_wifi: Optional[bool] = False
    pet_friendly: Optional[bool] = False
    rv_friendly: Optional[bool] = False
    tent_friendly: Optional[bool] = False


class CampgroundCreate(CampgroundBase):
    external_id: Optional[str] = None
    source_api: str = "rapidapi_outdoor"


class CampgroundInDB(CampgroundBase):
    id: int
    external_id: Optional[str] = None
    source_api: str
    created_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Campground(CampgroundInDB):
    pass


class CampgroundSearch(BaseModel):
    query: str
    limit: int = 10
