"""
Application configuration using Pydantic Settings.
All environment variables are loaded and validated here.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    PROJECT_NAME: str = "Automated Video Shorts Generator"
    DEBUG: bool = False
    API_VERSION: str = "v1"
    SECRET_KEY: str = "your-secret-key-change-in-production"

    # Demo Mode - runs without real API keys (free, no cost)
    DEMO_MODE: bool = True

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://your-frontend.vercel.app",
    ]

    # Database (Supabase)
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    DATABASE_URL: str = ""

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # AI Services
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    ELEVENLABS_API_KEY: str = ""

    # Media APIs
    PEXELS_API_KEY: str = ""
    PIXABAY_API_KEY: str = ""

    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    # Social Media
    YOUTUBE_CLIENT_ID: str = ""
    YOUTUBE_CLIENT_SECRET: str = ""
    INSTAGRAM_ACCESS_TOKEN: str = ""
    TIKTOK_ACCESS_TOKEN: str = ""

    # FFmpeg
    FFMPEG_PATH: str = "ffmpeg"
    OUTPUT_DIR: str = "./output"
    TEMP_DIR: str = "./temp"

    # n8n
    N8N_WEBHOOK_URL: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
