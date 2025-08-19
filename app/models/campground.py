from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Campground(Base):
    __tablename__ = "campgrounds"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    description = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    amenities = Column(Text)  # JSON string of amenities
    max_capacity = Column(Integer)
    has_electricity = Column(Boolean, default=False)
    has_water = Column(Boolean, default=False)
    has_showers = Column(Boolean, default=False)
    has_wifi = Column(Boolean, default=False)
    pet_friendly = Column(Boolean, default=False)
    rv_friendly = Column(Boolean, default=False)
    tent_friendly = Column(Boolean, default=False)
    external_id = Column(String)  # ID from the API
    source_api = Column(String, default="rapidapi_outdoor")  # Which API this came from
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    camping_trips = relationship("CampingTrip", back_populates="campground")
