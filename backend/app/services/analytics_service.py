"""
Analytics Service
Tracks video generation metrics, platform performance, and system stats.
"""

from typing import Optional
from datetime import datetime, timedelta

from app.core.config import settings


class AnalyticsService:
    """Service for tracking and reporting analytics."""

    async def get_dashboard_stats(self) -> dict:
        """Get overview dashboard statistics."""
        if settings.DEMO_MODE:
            from app.services.demo_data import demo_service
            return await demo_service.get_dashboard_stats()
        return {
            "total_videos": 0,
            "videos_published": 0,
            "total_views": 0,
            "success_rate": 0.0,
            "avg_generation_time_seconds": 0,
            "videos_this_week": 0,
            "platforms_connected": 0,
            "storage_used_mb": 0,
        }

    async def get_video_performance(self, video_id: str) -> Optional[dict]:
        """Get performance metrics for a specific video."""
        if settings.DEMO_MODE:
            from app.services.demo_data import demo_service
            return await demo_service.get_video_performance(video_id)
        return None

    async def get_trends(self, days: int = 30) -> dict:
        """Get generation and performance trends."""
        if settings.DEMO_MODE:
            from app.services.demo_data import demo_service
            return await demo_service.get_trends(days=days)
        return {
            "period_days": days,
            "daily_generations": [],
            "daily_views": [],
            "top_topics": [],
            "platform_breakdown": {},
        }

    async def get_logs(
        self, limit: int = 50, offset: int = 0, status: Optional[str] = None
    ) -> dict:
        """Get video generation logs."""
        if settings.DEMO_MODE:
            from app.services.demo_data import demo_service
            return await demo_service.get_logs(limit=limit, offset=offset, status=status)
        return {"logs": [], "total": 0}
