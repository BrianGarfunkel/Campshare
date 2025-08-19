from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.models.user import User
from app.crud.friend import (
    create_friend_request,
    get_friend_request,
    get_pending_friend_requests,
    get_friends,
    accept_friend_request,
    reject_friend_request,
    remove_friend,
    get_friends_with_user_info,
    get_pending_requests_with_user_info
)
from app.crud.user import get_user_by_username
from app.schemas.friend import FriendRequest, FriendResponse, FriendWithUser
from app.models.friend import Friend

router = APIRouter()


@router.post("/send-request", response_model=dict)
def send_friend_request(
    friend_request: FriendRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Send a friend request to another user by username"""
    # Get the user to send request to
    target_user = get_user_by_username(db, username=friend_request.username)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if target_user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot send friend request to yourself")
    
    # Check if friend request already exists
    existing_request = get_friend_request(db, current_user.id, target_user.id)
    if existing_request:
        if existing_request.is_accepted:
            raise HTTPException(status_code=400, detail="Already friends")
        else:
            raise HTTPException(status_code=400, detail="Friend request already sent")
    
    # Create the friend request
    new_request = create_friend_request(db, current_user.id, target_user.id)
    
    return {
        "message": f"Friend request sent to {target_user.username}",
        "friend_request_id": new_request.id
    }


@router.get("/pending-requests", response_model=List[dict])
def get_my_pending_requests(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all pending friend requests for the current user"""
    return get_pending_requests_with_user_info(db, current_user.id)


@router.post("/respond", response_model=dict)
def respond_to_friend_request(
    response: FriendResponse,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Accept or reject a friend request"""
    if response.accept:
        friend_request = accept_friend_request(db, response.friend_request_id, current_user.id)
        if not friend_request:
            raise HTTPException(status_code=404, detail="Friend request not found")
        return {"message": "Friend request accepted"}
    else:
        success = reject_friend_request(db, response.friend_request_id, current_user.id)
        if not success:
            raise HTTPException(status_code=404, detail="Friend request not found")
        return {"message": "Friend request rejected"}


@router.get("/my-friends", response_model=List[dict])
def get_my_friends(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all accepted friends for the current user"""
    return get_friends_with_user_info(db, current_user.id)


@router.delete("/remove/{friend_id}")
def remove_friend_relationship(
    friend_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove a friend relationship"""
    success = remove_friend(db, current_user.id, friend_id)
    if not success:
        raise HTTPException(status_code=404, detail="Friend relationship not found")
    
    return {"message": "Friend removed"}


@router.get("/search", response_model=List[dict])
def search_users(
    q: str = Query(..., description="Search query for usernames"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Search for users to add as friends"""
    # Simple search by username (case insensitive)
    users = db.query(User).filter(
        User.username.ilike(f"%{q}%"),
        User.id != current_user.id
    ).limit(10).all()
    
    # Get current user's friends to show relationship status
    friends = get_friends(db, current_user.id)
    friend_ids = set()
    for friend in friends:
        if friend.user_id == current_user.id:
            friend_ids.add(friend.friend_id)
        else:
            friend_ids.add(friend.user_id)
    
    # Get pending requests
    pending_requests = get_pending_friend_requests(db, current_user.id)
    pending_sent_ids = {req.user_id for req in pending_requests}
    
    pending_received = db.query(Friend).filter(
        Friend.user_id == current_user.id,
        Friend.is_accepted == False
    ).all()
    pending_received_ids = {req.friend_id for req in pending_received}
    
    results = []
    for user in users:
        relationship_status = "none"
        if user.id in friend_ids:
            relationship_status = "friends"
        elif user.id in pending_sent_ids:
            relationship_status = "request_sent"
        elif user.id in pending_received_ids:
            relationship_status = "request_received"
        
        results.append({
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "relationship_status": relationship_status
        })
    
    return results
