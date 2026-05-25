"""
Subtitle Engine Service
Generates word-level animated subtitles using Whisper transcription.
Supports ASS format with karaoke-style word highlighting.
"""

import uuid
import os
import subprocess
import json
from typing import Optional, List

from app.core.config import settings


class SubtitleEngineService:
    """Service for generating animated subtitles."""

    # ASS subtitle style templates
    STYLES = {
        "word_highlight": {
            "font": "Montserrat Bold",
            "font_size": 24,
            "primary_color": "&H00FFFFFF",
            "highlight_color": "&H0000FFFF",
            "outline_color": "&H00000000",
            "outline_width": 3,
            "shadow": 2,
            "alignment": 2,  # Bottom center
            "margin_v": 120,
        },
        "minimal": {
            "font": "Inter",
            "font_size": 20,
            "primary_color": "&H00FFFFFF",
            "highlight_color": "&H00FFFFFF",
            "outline_color": "&H00000000",
            "outline_width": 2,
            "shadow": 0,
            "alignment": 2,
            "margin_v": 100,
        },
        "bold_center": {
            "font": "Impact",
            "font_size": 32,
            "primary_color": "&H00FFFFFF",
            "highlight_color": "&H0000FF00",
            "outline_color": "&H00000000",
            "outline_width": 4,
            "shadow": 3,
            "alignment": 5,  # Center
            "margin_v": 0,
        },
    }


    async def generate_from_audio(
        self,
        audio_path: str,
        style: str = "word_highlight",
        language: str = "en",
    ) -> dict:
        """
        Generate subtitles from an audio file using Whisper.
        
        Args:
            audio_path: Path to the audio file
            style: Subtitle style template name
            language: Language code for transcription
            
        Returns:
            Subtitle file path and word timestamps
        """
        # Transcribe audio with Whisper (word-level timestamps)
        timestamps = await self._transcribe_whisper(audio_path, language)
        
        # Generate ASS subtitle file
        subtitle_id = str(uuid.uuid4())
        output_path = os.path.join(
            settings.TEMP_DIR, f"subtitles_{subtitle_id}.ass"
        )
        os.makedirs(settings.TEMP_DIR, exist_ok=True)
        
        ass_content = self._generate_ass(timestamps, style)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(ass_content)

        return {
            "id": subtitle_id,
            "path": output_path,
            "format": "ass",
            "style": style,
            "word_count": len(timestamps.get("words", [])),
            "duration": timestamps.get("duration", 0),
        }

    async def generate_from_text(
        self,
        text: str,
        word_timestamps: List[dict],
        style: str = "word_highlight",
    ) -> dict:
        """Generate subtitles from text with pre-computed timestamps."""
        subtitle_id = str(uuid.uuid4())
        output_path = os.path.join(
            settings.TEMP_DIR, f"subtitles_{subtitle_id}.ass"
        )
        os.makedirs(settings.TEMP_DIR, exist_ok=True)

        timestamps_data = {"words": word_timestamps}
        ass_content = self._generate_ass(timestamps_data, style)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(ass_content)

        return {
            "id": subtitle_id,
            "path": output_path,
            "format": "ass",
            "style": style,
            "word_count": len(word_timestamps),
        }


    async def _transcribe_whisper(self, audio_path: str, language: str) -> dict:
        """Transcribe audio using OpenAI Whisper API."""
        import openai

        client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        
        with open(audio_path, "rb") as audio_file:
            response = await client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=language,
                response_format="verbose_json",
                timestamp_granularities=["word"],
            )

        return {
            "text": response.text,
            "words": [
                {
                    "word": w.word,
                    "start": w.start,
                    "end": w.end,
                }
                for w in response.words
            ],
            "duration": response.duration,
        }

    def _generate_ass(self, timestamps: dict, style: str) -> str:
        """Generate ASS subtitle file with animated word highlighting."""
        style_config = self.STYLES.get(style, self.STYLES["word_highlight"])
        words = timestamps.get("words", [])
        
        # ASS header
        header = f"""[Script Info]
Title: Auto-Generated Subtitles
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{style_config['font']},{style_config['font_size']},{style_config['primary_color']},&H000000FF,{style_config['outline_color']},&H00000000,-1,0,0,0,100,100,0,0,1,{style_config['outline_width']},{style_config['shadow']},{style_config['alignment']},40,40,{style_config['margin_v']},1
Style: Highlight,{style_config['font']},{style_config['font_size']},{style_config['highlight_color']},&H000000FF,{style_config['outline_color']},&H00000000,-1,0,0,0,100,100,0,0,1,{style_config['outline_width']},{style_config['shadow']},{style_config['alignment']},40,40,{style_config['margin_v']},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        # Generate dialogue events with word-by-word karaoke
        events = []
        # Group words into lines (max 4-5 words per line)
        line_size = 4
        for i in range(0, len(words), line_size):
            line_words = words[i:i + line_size]
            if not line_words:
                continue
                
            start = line_words[0]["start"]
            end = line_words[-1]["end"]
            
            # Build karaoke text with highlighting
            text_parts = []
            for w in line_words:
                duration_cs = int((w["end"] - w["start"]) * 100)
                text_parts.append(f"{{\\kf{duration_cs}}}{w['word']}")
            
            text = " ".join(text_parts) if not text_parts else "".join(text_parts)
            
            start_str = self._seconds_to_ass_time(start)
            end_str = self._seconds_to_ass_time(end)
            
            events.append(
                f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{text}"
            )

        return header + "\n".join(events)

    def _seconds_to_ass_time(self, seconds: float) -> str:
        """Convert seconds to ASS time format (H:MM:SS.CC)."""
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        cs = int((seconds % 1) * 100)
        return f"{h}:{m:02d}:{s:02d}.{cs:02d}"
