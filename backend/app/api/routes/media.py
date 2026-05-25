"""
Media Collection API Routes
Handles stock video/image search and download.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()


class MediaSearchRequest(BaseModel):
    """Request for media search."""
    query: str
    media_type: str = "video"  # video, image
    orientation: str = "portrait"  # portrait, landscape, square
    min_duration: Optional[int] = 3
    max_duration: Optional[int] = 15
    per_page: int = 10
    provider: str = "pexels"  # pexels, pixabay


class MediaItem(BaseModel):
    """A media item from search results."""
    id: str
    provider: str
    type: str
    url: str
    preview_url: str
    thumbnail_url: str
    duration: Optional[float]
    width: int
    height: int
    tags: List[str]


@router.post("/search", response_model=List[MediaItem])
async def search_media(request: MediaSearchRequest):
    """
    Search for stock videos/images matching the query.
    
    Optimized for vertical short-form content (9:16 aspect ratio).
    """
    from app.services.media_collector import MediaCollectorService
    
    service = MediaCollectorService()
    try:
        results = await service.search(
            query=request.query,
            media_type=request.media_type,
            orientation=request.orientation,
            min_duration=request.min_duration,
            max_duration=request.max_duration,
            per_page=request.per_page,
            provider=request.provider,
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Media search failed: {str(e)}")


@router.post("/download")
async def download_media(media_url: str, media_type: str = "video"):
    """Download and store media asset for video rendering."""
    from app.services.media_collector import MediaCollectorService
    
    service = MediaCollectorService()
    try:
        result = await service.download(url=media_url, media_type=media_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Media download failed: {str(e)}")


@router.post("/auto-collect")
async def auto_collect_media(script_id: str, clips_needed: int = 5):
    """
    Automatically collect media based on script content.
    
    Analyzes the script, extracts visual keywords, and fetches
    matching stock footage for each scene.
    """
    from app.services.media_collector import MediaCollectorService
    
    service = MediaCollectorService()
    try:
        result = await service.auto_collect(
            script_id=script_id,
            clips_needed=clips_needed,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Auto-collection failed: {str(e)}")
