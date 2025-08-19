from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FriendBase(BaseModel):
    friend_id: int


class FriendRequest(BaseModel):
    """Schema for sending a friend request"""
    username: str


class FriendCreate(FriendBase):
    pass


class FriendUpdate(BaseModel):
    is_accepted: bool


class FriendInDB(FriendBase):
    id: int
    user_id: int
    is_accepted: bool
    created_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Friend(FriendInDB):
    pass





class FriendResponse(BaseModel):
    """Schema for responding to a friend request"""
    friend_request_id: int
    accept: bool


class FriendWithUser(BaseModel):
    """Schema for friend data with user information"""
    id: int
    user_id: int
    friend_id: int
    is_accepted: bool
    created_at: datetime
    friend_username: str
    friend_full_name: str

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
