from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import api_router
from app.core.database import engine
from app.core.database import Base
from app.models import User, Friend, Campground, CampingTrip  # Import models to register them

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    docs_url=None,  # Disable OpenAPI docs
    redoc_url=None,  # Disable ReDoc
    openapi_url=None  # Disable OpenAPI schema
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    """Root endpoint."""
    return {"message": "Welcome to Hiking App API!"}


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
