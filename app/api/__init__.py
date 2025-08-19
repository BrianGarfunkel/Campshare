from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .campgrounds import router as campgrounds_router
from .camping_trips import router as camping_trips_router
from .friends import router as friends_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(campgrounds_router, prefix="/campgrounds", tags=["campgrounds"])
api_router.include_router(camping_trips_router, prefix="/camping-trips", tags=["camping-trips"])
api_router.include_router(friends_router, prefix="/friends", tags=["friends"])
