"""
Voice Generator Service
Text-to-Speech conversion using ElevenLabs, OpenAI TTS, or XTTS.
Returns audio files with word-level timestamps for subtitle sync.
"""

import uuid
import os
import aiohttp
from typing import Optional, List

from app.core.config import settings


class VoiceGeneratorService:
    """Service for generating voiceovers from text."""

    ELEVENLABS_BASE_URL = "https://api.elevenlabs.io/v1"
    
    DEFAULT_VOICES = [
        {
            "id": "21m00Tcm4TlvDq8ikWAM",
            "name": "Rachel",
            "provider": "elevenlabs",
            "language": "en",
            "gender": "female",
            "preview_url": None,
            "description": "Calm and professional female voice",
        },
        {
            "id": "AZnzlk1XvdvUeBnXmlld",
            "name": "Domi",
            "provider": "elevenlabs",
            "language": "en",
            "gender": "female",
            "preview_url": None,
            "description": "Energetic and young female voice",
        },
        {
            "id": "EXAVITQu4vr4xnSDxMaL",
            "name": "Bella",
            "provider": "elevenlabs",
            "language": "en",
            "gender": "female",
            "preview_url": None,
            "description": "Soft and friendly female voice",
        },
        {
            "id": "ErXwobaYiN019PkySvjV",
            "name": "Antoni",
            "provider": "elevenlabs",
            "language": "en",
            "gender": "male",
            "preview_url": None,
            "description": "Clear and confident male voice",
        },
        {
            "id": "VR6AewLTigWG4xSOukaG",
            "name": "Arnold",
            "provider": "elevenlabs",
            "language": "en",
            "gender": "male",
            "preview_url": None,
            "description": "Deep and authoritative male voice",
        },
    ]

    async def generate(
        self,
        text: str,
        voice_id: str = "default",
        provider: str = "elevenlabs",
        speed: float = 1.0,
        pitch: float = 1.0,
        language: str = "en",
    ) -> dict:
        """
        Generate voiceover audio from text.
        
        Args:
            text: The text to convert to speech
            voice_id: ID of the voice to use
            provider: TTS provider (elevenlabs, openai, xtts)
            speed: Speaking speed multiplier
            pitch: Voice pitch adjustment
            language: Language code
            
        Returns:
            Audio file URL, duration, and word timestamps
        """
        if provider == "elevenlabs":
            return await self._generate_elevenlabs(text, voice_id, speed)
        elif provider == "openai":
            return await self._generate_openai(text, voice_id, speed)
        else:
            raise ValueError(f"Unsupported TTS provider: {provider}")

    async def _generate_elevenlabs(self, text: str, voice_id: str, speed: float) -> dict:
        """Generate audio using ElevenLabs API."""
        if voice_id == "default":
            voice_id = self.DEFAULT_VOICES[0]["id"]

        url = f"{self.ELEVENLABS_BASE_URL}/text-to-speech/{voice_id}/with-timestamps"
        
        headers = {
            "Accept": "application/json",
            "xi-api-key": settings.ELEVENLABS_API_KEY,
            "Content-Type": "application/json",
        }
        
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.8,
                "speed": speed,
            },
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"ElevenLabs API error: {error_text}")
                
                result = await response.json()
                
                # Save audio file
                audio_id = str(uuid.uuid4())
                output_path = os.path.join(settings.TEMP_DIR, f"voice_{audio_id}.mp3")
                os.makedirs(settings.TEMP_DIR, exist_ok=True)
                
                import base64
                audio_bytes = base64.b64decode(result["audio_base64"])
                with open(output_path, "wb") as f:
                    f.write(audio_bytes)

                return {
                    "id": audio_id,
                    "audio_url": output_path,
                    "duration": result.get("duration", 0),
                    "timestamps": result.get("alignment", {}),
                    "provider": "elevenlabs",
                    "voice_id": voice_id,
                }

    async def _generate_openai(self, text: str, voice_id: str, speed: float) -> dict:
        """Generate audio using OpenAI TTS API."""
        import openai
        
        client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        
        if voice_id == "default":
            voice_id = "alloy"
        
        response = await client.audio.speech.create(
            model="tts-1-hd",
            voice=voice_id,
            input=text,
            speed=speed,
        )
        
        audio_id = str(uuid.uuid4())
        output_path = os.path.join(settings.TEMP_DIR, f"voice_{audio_id}.mp3")
        os.makedirs(settings.TEMP_DIR, exist_ok=True)
        
        with open(output_path, "wb") as f:
            f.write(response.content)

        return {
            "id": audio_id,
            "audio_url": output_path,
            "duration": None,  # Calculated during rendering
            "timestamps": None,  # Use Whisper for timestamps
            "provider": "openai",
            "voice_id": voice_id,
        }

    async def list_voices(self) -> List[dict]:
        """List all available voices across providers."""
        voices = self.DEFAULT_VOICES.copy()
        
        # Add OpenAI voices
        openai_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
        for voice in openai_voices:
            voices.append({
                "id": voice,
                "name": voice.capitalize(),
                "provider": "openai",
                "language": "en",
                "gender": "neutral",
                "preview_url": None,
                "description": f"OpenAI {voice} voice",
            })
        
        return voices

    async def clone_voice(self, name: str, audio_data: bytes, description: Optional[str] = None) -> dict:
        """Clone a voice from an audio sample using ElevenLabs."""
        url = f"{self.ELEVENLABS_BASE_URL}/voices/add"
        
        headers = {
            "xi-api-key": settings.ELEVENLABS_API_KEY,
        }
        
        import aiohttp
        from aiohttp import FormData
        
        data = FormData()
        data.add_field("name", name)
        data.add_field("files", audio_data, filename="sample.mp3", content_type="audio/mpeg")
        if description:
            data.add_field("description", description)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Voice cloning failed: {error_text}")
                result = await response.json()
                return {
                    "voice_id": result["voice_id"],
                    "name": name,
                    "message": "Voice cloned successfully",
                }
