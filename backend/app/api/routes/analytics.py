"""
Analytics API Routes
Track video performance, generation stats, and system metrics.
"""

from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard_stats():
    """
    Get overview dashboard statistics.
    
    Returns:
    - Total videos generated
    - Videos published
    - Total views across platforms
    - Generation success rate
    - Average generation time
    """
    from app.services.analytics_service import AnalyticsService
    
    service = AnalyticsService()
    return await service.get_dashboard_stats()


@router.get("/videos/{video_id}/performance")
async def get_video_performance(video_id: str):
    """Get performance metrics for a specific video across all platforms."""
    from app.services.analytics_service import AnalyticsService
    
    service = AnalyticsService()
    result = await service.get_video_performance(video_id)
    if not result:
        raise HTTPException(status_code=404, detail="Video not found")
    return result


@router.get("/trends")
async def get_trends(days: int = 30):
    """Get video generation and performance trends over time."""
    from app.services.analytics_service import AnalyticsService
    
    service = AnalyticsService()
    return await service.get_trends(days=days)


@router.get("/generation-logs")
async def get_generation_logs(
    limit: int = 50,
    offset: int = 0,
    status: Optional[str] = None,
):
    """Get video generation logs with filtering."""
    from app.services.analytics_service import AnalyticsService
    
    service = AnalyticsService()
    return await service.get_logs(limit=limit, offset=offset, status=status)
