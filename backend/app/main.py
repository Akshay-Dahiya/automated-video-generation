"""
Automated Video Shorts Generation System - FastAPI Backend
Main application entry point with CORS, routing, and lifecycle management.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.routes import router as api_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management."""
    # Startup
    print("🚀 Starting Automated Video Generation API...")
    yield
    # Shutdown
    print("👋 Shutting down API...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-powered automated short-form video generation platform",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "automated-video-generation",
        "version": "1.0.0",
    }
