"""
Social Media Upload API Routes
Handles video publishing to YouTube, Instagram, and TikTok.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter()


class UploadRequest(BaseModel):
    """Request to upload a video to social platforms."""
    video_id: str
    platforms: List[str]  # youtube, instagram, tiktok
    title: str
    description: str
    tags: List[str] = []
    schedule_at: Optional[datetime] = None
    visibility: str = "public"  # public, private, unlisted


class UploadStatus(BaseModel):
    """Upload status for a specific platform."""
    platform: str
    status: str  # pending, uploading, published, failed
    url: Optional[str]
    error: Optional[str]
    uploaded_at: Optional[str]


@router.post("/publish")
async def publish_video(request: UploadRequest):
    """
    Publish a rendered video to one or more social platforms.
    
    Supports scheduled publishing and multi-platform simultaneous upload.
    """
    from app.services.social_uploader import SocialUploaderService
    
    service = SocialUploaderService()
    try:
        result = await service.publish(
            video_id=request.video_id,
            platforms=request.platforms,
            title=request.title,
            description=request.description,
            tags=request.tags,
            schedule_at=request.schedule_at,
            visibility=request.visibility,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/{video_id}/status", response_model=List[UploadStatus])
async def get_upload_status(video_id: str):
    """Get upload status for all platforms for a specific video."""
    from app.services.social_uploader import SocialUploaderService
    
    service = SocialUploaderService()
    return await service.get_status(video_id)


@router.post("/auth/{platform}")
async def authenticate_platform(platform: str, code: str):
    """Complete OAuth flow for a social media platform."""
    from app.services.social_uploader import SocialUploaderService
    
    service = SocialUploaderService()
    try:
        result = await service.authenticate(platform=platform, code=code)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")


@router.get("/auth/{platform}/url")
async def get_auth_url(platform: str):
    """Get OAuth URL for a social media platform."""
    from app.services.social_uploader import SocialUploaderService
    
    service = SocialUploaderService()
    return await service.get_auth_url(platform)
