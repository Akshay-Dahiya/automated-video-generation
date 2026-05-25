"""
Voice Generation API Routes
Handles text-to-speech conversion with multiple voice providers.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()


class VoiceGenerateRequest(BaseModel):
    """Request for voice generation."""
    text: str
    voice_id: str = "default"
    provider: str = "elevenlabs"  # elevenlabs, xtts, openai
    speed: float = 1.0
    pitch: float = 1.0
    language: str = "en"


class VoiceStyle(BaseModel):
    """Available voice style."""
    id: str
    name: str
    provider: str
    language: str
    gender: str
    preview_url: Optional[str]
    description: str


@router.post("/generate")
async def generate_voice(request: VoiceGenerateRequest):
    """
    Generate voiceover audio from text.
    
    Returns audio file URL and word-level timestamps for subtitle sync.
    """
    from app.services.voice_generator import VoiceGeneratorService
    
    service = VoiceGeneratorService()
    try:
        result = await service.generate(
            text=request.text,
            voice_id=request.voice_id,
            provider=request.provider,
            speed=request.speed,
            pitch=request.pitch,
            language=request.language,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice generation failed: {str(e)}")


@router.get("/styles", response_model=List[VoiceStyle])
async def list_voice_styles():
    """List all available voice styles across providers."""
    from app.services.voice_generator import VoiceGeneratorService
    
    service = VoiceGeneratorService()
    return await service.list_voices()


@router.post("/clone")
async def clone_voice(
    name: str,
    audio_file: UploadFile = File(...),
    description: Optional[str] = None,
):
    """Clone a voice from an audio sample (ElevenLabs)."""
    from app.services.voice_generator import VoiceGeneratorService
    
    service = VoiceGeneratorService()
    try:
        result = await service.clone_voice(
            name=name,
            audio_data=await audio_file.read(),
            description=description,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice cloning failed: {str(e)}")
