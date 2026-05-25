"""
Video Renderer Service
FFmpeg-based video compositing pipeline for vertical short-form content.
Combines clips, audio, subtitles, and effects into final 9:16 video.
"""

import uuid
import os
import subprocess
import json
from typing import Optional, List

from app.core.config import settings


class VideoRendererService:
    """Service for rendering final videos using FFmpeg."""

    # Output specifications for short-form vertical video
    OUTPUT_WIDTH = 1080
    OUTPUT_HEIGHT = 1920
    OUTPUT_FPS = 30
    OUTPUT_CODEC = "libx264"
    OUTPUT_PRESET = "medium"
    OUTPUT_CRF = 23
    AUDIO_CODEC = "aac"
    AUDIO_BITRATE = "192k"


    async def render(
        self,
        video_clips: List[str],
        audio_path: str,
        subtitle_path: Optional[str] = None,
        background_music_path: Optional[str] = None,
        music_volume: float = 0.15,
        output_name: Optional[str] = None,
    ) -> dict:
        """
        Render final video from components.
        
        Args:
            video_clips: List of video clip file paths
            audio_path: Path to voiceover audio
            subtitle_path: Path to ASS subtitle file
            background_music_path: Path to background music
            music_volume: Background music volume (0-1)
            output_name: Custom output filename
            
        Returns:
            Rendered video path and metadata
        """
        render_id = output_name or str(uuid.uuid4())
        output_path = os.path.join(
            settings.OUTPUT_DIR, f"video_{render_id}.mp4"
        )
        os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
        os.makedirs(settings.TEMP_DIR, exist_ok=True)

        # Step 1: Prepare video clips (scale, crop to 9:16)
        prepared_clips = await self._prepare_clips(video_clips)
        
        # Step 2: Concatenate clips
        concat_path = await self._concat_clips(prepared_clips, render_id)
        
        # Step 3: Add audio and mix
        mixed_path = await self._mix_audio(
            concat_path, audio_path, background_music_path,
            music_volume, render_id
        )
        
        # Step 4: Add subtitles
        if subtitle_path:
            final_path = await self._add_subtitles(
                mixed_path, subtitle_path, output_path
            )
        else:
            final_path = mixed_path
            os.rename(mixed_path, output_path)
            final_path = output_path

        # Get video metadata
        metadata = await self._get_metadata(output_path)

        return {
            "id": render_id,
            "path": output_path,
            "duration": metadata.get("duration", 0),
            "size_bytes": os.path.getsize(output_path),
            "resolution": f"{self.OUTPUT_WIDTH}x{self.OUTPUT_HEIGHT}",
            "fps": self.OUTPUT_FPS,
            "codec": self.OUTPUT_CODEC,
        }


    async def _prepare_clips(self, clips: List[str]) -> List[str]:
        """Scale and crop clips to 9:16 aspect ratio."""
        prepared = []
        for i, clip in enumerate(clips):
            output = os.path.join(settings.TEMP_DIR, f"prep_{i}.mp4")
            cmd = [
                settings.FFMPEG_PATH, "-y", "-i", clip,
                "-vf", (
                    f"scale={self.OUTPUT_WIDTH}:{self.OUTPUT_HEIGHT}:"
                    f"force_original_aspect_ratio=increase,"
                    f"crop={self.OUTPUT_WIDTH}:{self.OUTPUT_HEIGHT},"
                    f"setsar=1"
                ),
                "-c:v", self.OUTPUT_CODEC,
                "-preset", "fast",
                "-crf", "20",
                "-an",  # Remove audio from clips
                "-r", str(self.OUTPUT_FPS),
                output,
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            prepared.append(output)
        return prepared

    async def _concat_clips(self, clips: List[str], render_id: str) -> str:
        """Concatenate prepared clips into one video."""
        concat_list = os.path.join(settings.TEMP_DIR, f"concat_{render_id}.txt")
        with open(concat_list, "w") as f:
            for clip in clips:
                f.write(f"file '{os.path.abspath(clip)}'\n")

        output = os.path.join(settings.TEMP_DIR, f"concat_{render_id}.mp4")
        cmd = [
            settings.FFMPEG_PATH, "-y",
            "-f", "concat", "-safe", "0",
            "-i", concat_list,
            "-c", "copy",
            output,
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return output


    async def _mix_audio(
        self, video_path: str, voice_path: str,
        music_path: Optional[str], music_volume: float, render_id: str
    ) -> str:
        """Mix voiceover and background music with video."""
        output = os.path.join(settings.TEMP_DIR, f"mixed_{render_id}.mp4")
        
        if music_path:
            # Mix voice + background music
            cmd = [
                settings.FFMPEG_PATH, "-y",
                "-i", video_path,
                "-i", voice_path,
                "-i", music_path,
                "-filter_complex", (
                    f"[1:a]volume=1.0[voice];"
                    f"[2:a]volume={music_volume}[music];"
                    f"[voice][music]amix=inputs=2:duration=shortest[aout]"
                ),
                "-map", "0:v",
                "-map", "[aout]",
                "-c:v", "copy",
                "-c:a", self.AUDIO_CODEC,
                "-b:a", self.AUDIO_BITRATE,
                "-shortest",
                output,
            ]
        else:
            # Voice only
            cmd = [
                settings.FFMPEG_PATH, "-y",
                "-i", video_path,
                "-i", voice_path,
                "-map", "0:v",
                "-map", "1:a",
                "-c:v", "copy",
                "-c:a", self.AUDIO_CODEC,
                "-b:a", self.AUDIO_BITRATE,
                "-shortest",
                output,
            ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return output

    async def _add_subtitles(
        self, video_path: str, subtitle_path: str, output_path: str
    ) -> str:
        """Burn subtitles into video."""
        cmd = [
            settings.FFMPEG_PATH, "-y",
            "-i", video_path,
            "-vf", f"ass={subtitle_path}",
            "-c:v", self.OUTPUT_CODEC,
            "-preset", self.OUTPUT_PRESET,
            "-crf", str(self.OUTPUT_CRF),
            "-c:a", "copy",
            output_path,
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path

    async def _get_metadata(self, video_path: str) -> dict:
        """Get video file metadata using ffprobe."""
        cmd = [
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_format", "-show_streams",
            video_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return {
                "duration": float(data["format"].get("duration", 0)),
                "size": int(data["format"].get("size", 0)),
                "bitrate": int(data["format"].get("bit_rate", 0)),
            }
        return {}
