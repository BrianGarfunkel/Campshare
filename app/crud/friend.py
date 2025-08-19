from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.friend import Friend
from app.models.user import User
from app.schemas.friend import FriendCreate, FriendUpdate
from typing import List, Optional


def create_friend_request(db: Session, user_id: int, friend_id: int) -> Friend:
    """Create a new friend request"""
    db_friend = Friend(user_id=user_id, friend_id=friend_id, is_accepted=False)
    db.add(db_friend)
    db.commit()
    db.refresh(db_friend)
    return db_friend


def get_friend_request(db: Session, user_id: int, friend_id: int) -> Optional[Friend]:
    """Get a specific friend request between two users"""
    return db.query(Friend).filter(
        and_(
            or_(
                and_(Friend.user_id == user_id, Friend.friend_id == friend_id),
                and_(Friend.user_id == friend_id, Friend.friend_id == user_id)
            )
        )
    ).first()


def get_pending_friend_requests(db: Session, user_id: int) -> List[Friend]:
    """Get all pending friend requests for a user"""
    return db.query(Friend).filter(
        and_(Friend.friend_id == user_id, Friend.is_accepted == False)
    ).all()


def get_friends(db: Session, user_id: int) -> List[Friend]:
    """Get all accepted friends for a user"""
    return db.query(Friend).filter(
        and_(
            or_(
                and_(Friend.user_id == user_id, Friend.is_accepted == True),
                and_(Friend.friend_id == user_id, Friend.is_accepted == True)
            )
        )
    ).all()


def accept_friend_request(db: Session, friend_request_id: int, user_id: int) -> Optional[Friend]:
    """Accept a friend request"""
    friend_request = db.query(Friend).filter(
        and_(Friend.id == friend_request_id, Friend.friend_id == user_id)
    ).first()
    
    if friend_request:
        friend_request.is_accepted = True
        db.commit()
        db.refresh(friend_request)
    
    return friend_request


def reject_friend_request(db: Session, friend_request_id: int, user_id: int) -> bool:
    """Reject/delete a friend request"""
    friend_request = db.query(Friend).filter(
        and_(Friend.id == friend_request_id, Friend.friend_id == user_id)
    ).first()
    
    if friend_request:
        db.delete(friend_request)
        db.commit()
        return True
    
    return False


def remove_friend(db: Session, user_id: int, friend_id: int) -> bool:
    """Remove a friend relationship"""
    friend_relationship = get_friend_request(db, user_id, friend_id)
    
    if friend_relationship and friend_relationship.is_accepted:
        db.delete(friend_relationship)
        db.commit()
        return True
    
    return False


def get_friends_with_user_info(db: Session, user_id: int) -> List[dict]:
    """Get friends with user information for display"""
    friends = get_friends(db, user_id)
    friends_with_info = []
    
    for friend in friends:
        # Determine which user is the friend (not the current user)
        if friend.user_id == user_id:
            friend_user_id = friend.friend_id
        else:
            friend_user_id = friend.user_id
        
        # Get friend's user info
        friend_user = db.query(User).filter(User.id == friend_user_id).first()
        
        if friend_user:
            friends_with_info.append({
                "id": friend.id,
                "user_id": user_id,
                "friend_id": friend_user_id,
                "is_accepted": friend.is_accepted,
                "created_at": friend.created_at,
                "friend_username": friend_user.username,
                "friend_full_name": friend_user.full_name
            })
    
    return friends_with_info


def get_pending_requests_with_user_info(db: Session, user_id: int) -> List[dict]:
    """Get pending friend requests with user information"""
    pending_requests = get_pending_friend_requests(db, user_id)
    requests_with_info = []
    
    for request in pending_requests:
        # Get the user who sent the request
        sender_user = db.query(User).filter(User.id == request.user_id).first()
        
        if sender_user:
            requests_with_info.append({
                "id": request.id,
                "user_id": request.user_id,
                "friend_id": request.friend_id,
                "is_accepted": request.is_accepted,
                "created_at": request.created_at,
                "sender_username": sender_user.username,
                "sender_full_name": sender_user.full_name
            })
    
    return requests_with_info
