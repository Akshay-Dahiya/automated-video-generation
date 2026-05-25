"""
Video Generation & Management API Routes
Handles the full video generation pipeline and video management.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

router = APIRouter()


class VideoStatus(str, Enum):
    pending = "pending"
    generating_script = "generating_script"
    generating_voice = "generating_voice"
    collecting_media = "collecting_media"
    generating_subtitles = "generating_subtitles"
    rendering = "rendering"
    completed = "completed"
    failed = "failed"
    uploading = "uploading"
    published = "published"


class VideoGenerateRequest(BaseModel):
    """Request to generate a complete video."""
    topic: str
    tone: str = "informative"
    duration_seconds: int = 60
    voice_id: Optional[str] = None
    background_music: Optional[str] = "energetic"
    subtitle_style: str = "word_highlight"
    auto_upload: bool = False
    upload_platforms: List[str] = []
    custom_script: Optional[str] = None


class VideoResponse(BaseModel):
    """Video generation response."""
    id: str
    status: VideoStatus
    topic: str
    progress: float
    script_id: Optional[str]
    video_url: Optional[str]
    thumbnail_url: Optional[str]
    duration: Optional[float]
    created_at: str
    completed_at: Optional[str]


@router.post("/generate", response_model=VideoResponse)
async def generate_video(request: VideoGenerateRequest, background_tasks: BackgroundTasks):
    """
    Trigger full video generation pipeline.
    
    Pipeline steps:
    1. Generate/use script
    2. Generate voiceover
    3. Collect media assets
    4. Generate subtitles
    5. Render final video
    6. (Optional) Upload to platforms
    """
    from app.services.video_pipeline import VideoPipelineService
    
    service = VideoPipelineService()
    try:
        job = await service.create_job(request.model_dump())
        background_tasks.add_task(service.execute_pipeline, job["id"])
        return job
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")


@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(video_id: str):
    """Get video status and details."""
    from app.services.video_pipeline import VideoPipelineService
    
    service = VideoPipelineService()
    result = await service.get_job(video_id)
    if not result:
        raise HTTPException(status_code=404, detail="Video not found")
    return result


@router.get("/")
async def list_videos(
    status: Optional[VideoStatus] = None,
    limit: int = 20,
    offset: int = 0,
):
    """List all videos with optional status filter."""
    from app.services.video_pipeline import VideoPipelineService
    
    service = VideoPipelineService()
    return await service.list_jobs(status=status, limit=limit, offset=offset)


@router.delete("/{video_id}")
async def delete_video(video_id: str):
    """Delete a video and its associated assets."""
    from app.services.video_pipeline import VideoPipelineService
    
    service = VideoPipelineService()
    success = await service.delete_job(video_id)
    if not success:
        raise HTTPException(status_code=404, detail="Video not found")
    return {"message": "Video deleted successfully"}


@router.post("/{video_id}/retry")
async def retry_video(video_id: str, background_tasks: BackgroundTasks):
    """Retry a failed video generation."""
    from app.services.video_pipeline import VideoPipelineService
    
    service = VideoPipelineService()
    job = await service.retry_job(video_id)
    if not job:
        raise HTTPException(status_code=404, detail="Video not found")
    background_tasks.add_task(service.execute_pipeline, video_id)
    return job
