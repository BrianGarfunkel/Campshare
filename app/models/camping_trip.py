from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class CampingTrip(Base):
    __tablename__ = "camping_trips"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    notes = Column(Text)
    weather_conditions = Column(String)
    group_size = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    campground_id = Column(Integer, ForeignKey("campgrounds.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="camping_trips")
    campground = relationship("Campground", back_populates="camping_trips")
