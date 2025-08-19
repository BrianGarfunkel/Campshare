from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://Uri@localhost/hiking_app"
    
    # JWT Settings
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # App Settings
    app_name: str = "Hiking App"
    debug: bool = True
    
    class Config:
        env_file = ".env"


settings = Settings()
