"""
Script Generation API Routes
Handles AI-powered script creation for short-form videos.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

router = APIRouter()


class ToneEnum(str, Enum):
    informative = "informative"
    entertaining = "entertaining"
    motivational = "motivational"
    educational = "educational"
    humorous = "humorous"
    dramatic = "dramatic"


class ScriptGenerateRequest(BaseModel):
    """Request body for script generation."""
    topic: str
    tone: ToneEnum = ToneEnum.informative
    duration_seconds: int = 60
    style: Optional[str] = "viral"
    target_audience: Optional[str] = "general"
    include_hook: bool = True
    include_cta: bool = True
    language: str = "en"


class ScriptSection(BaseModel):
    """A section of the generated script."""
    type: str  # hook, body, cta
    text: str
    estimated_duration: float
    visual_suggestion: str


class ScriptResponse(BaseModel):
    """Response containing the generated script."""
    id: str
    topic: str
    title: str
    sections: List[ScriptSection]
    full_text: str
    word_count: int
    estimated_duration: float
    hashtags: List[str]
    metadata: dict


@router.post("/generate", response_model=ScriptResponse)
async def generate_script(request: ScriptGenerateRequest):
    """
    Generate an AI-powered script for a short-form video.
    
    The script follows the Hook → Body → CTA structure optimized
    for engagement on platforms like YouTube Shorts, Reels, and TikTok.
    """
    from app.services.script_generator import ScriptGeneratorService
    
    service = ScriptGeneratorService()
    try:
        result = await service.generate(
            topic=request.topic,
            tone=request.tone.value,
            duration=request.duration_seconds,
            style=request.style,
            target_audience=request.target_audience,
            include_hook=request.include_hook,
            include_cta=request.include_cta,
            language=request.language,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Script generation failed: {str(e)}")


@router.get("/{script_id}")
async def get_script(script_id: str):
    """Retrieve a previously generated script by ID."""
    from app.services.script_generator import ScriptGeneratorService
    
    service = ScriptGeneratorService()
    result = await service.get_by_id(script_id)
    if not result:
        raise HTTPException(status_code=404, detail="Script not found")
    return result


@router.get("/")
async def list_scripts(limit: int = 20, offset: int = 0):
    """List all generated scripts with pagination."""
    from app.services.script_generator import ScriptGeneratorService
    
    service = ScriptGeneratorService()
    return await service.list_all(limit=limit, offset=offset)


@router.post("/{script_id}/regenerate")
async def regenerate_script(script_id: str):
    """Regenerate a script with the same parameters but new content."""
    from app.services.script_generator import ScriptGeneratorService
    
    service = ScriptGeneratorService()
    result = await service.regenerate(script_id)
    if not result:
        raise HTTPException(status_code=404, detail="Original script not found")
    return result
