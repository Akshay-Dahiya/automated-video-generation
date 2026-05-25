"""
API Route Registration - All endpoints are organized by domain.
"""

from fastapi import APIRouter

from app.api.routes.scripts import router as scripts_router
from app.api.routes.videos import router as videos_router
from app.api.routes.voices import router as voices_router
from app.api.routes.media import router as media_router
from app.api.routes.uploads import router as uploads_router
from app.api.routes.analytics import router as analytics_router

router = APIRouter()

router.include_router(scripts_router, prefix="/scripts", tags=["Scripts"])
router.include_router(videos_router, prefix="/videos", tags=["Videos"])
router.include_router(voices_router, prefix="/voices", tags=["Voices"])
router.include_router(media_router, prefix="/media", tags=["Media"])
router.include_router(uploads_router, prefix="/uploads", tags=["Uploads"])
router.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
