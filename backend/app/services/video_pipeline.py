"""
Video Pipeline Service
Orchestrates the full video generation pipeline from script to upload.
Manages job state, progress tracking, and error handling.
"""

import uuid
from datetime import datetime
from typing import Optional

from app.core.config import settings


class VideoPipelineService:
    """Orchestrates the complete video generation pipeline."""

    # In-memory job store (replace with DB in production)
    _jobs = {}

    async def create_job(self, params: dict) -> dict:
        """Create a new video generation job."""
        job_id = str(uuid.uuid4())
        job = {
            "id": job_id,
            "status": "pending",
            "topic": params.get("topic", ""),
            "progress": 0.0,
            "script_id": None,
            "video_url": None,
            "thumbnail_url": None,
            "duration": None,
            "created_at": datetime.utcnow().isoformat(),
            "completed_at": None,
            "params": params,
            "error": None,
        }
        self._jobs[job_id] = job
        return job

    async def execute_pipeline(self, job_id: str):
        """
        Execute the full video generation pipeline.
        
        Steps:
        1. Generate script (or use custom)
        2. Generate voiceover
        3. Collect media assets
        4. Generate subtitles
        5. Render video
        6. (Optional) Upload to platforms
        """
        job = self._jobs.get(job_id)
        if not job:
            return

        try:
            params = job["params"]


            # Step 1: Script Generation
            job["status"] = "generating_script"
            job["progress"] = 0.1
            
            if params.get("custom_script"):
                script = {"full_text": params["custom_script"], "id": "custom"}
            else:
                from app.services.script_generator import ScriptGeneratorService
                script_service = ScriptGeneratorService()
                script = await script_service.generate(
                    topic=params["topic"],
                    tone=params.get("tone", "informative"),
                    duration=params.get("duration_seconds", 60),
                )
            job["script_id"] = script["id"]
            job["progress"] = 0.2

            # Step 2: Voice Generation
            job["status"] = "generating_voice"
            from app.services.voice_generator import VoiceGeneratorService
            voice_service = VoiceGeneratorService()
            voice_result = await voice_service.generate(
                text=script["full_text"],
                voice_id=params.get("voice_id", "default"),
            )
            job["progress"] = 0.4

            # Step 3: Media Collection
            job["status"] = "collecting_media"
            from app.services.media_collector import MediaCollectorService
            media_service = MediaCollectorService()
            media_result = await media_service.auto_collect(
                script_id=script["id"],
                clips_needed=5,
            )
            job["progress"] = 0.6

            # Step 4: Subtitle Generation
            job["status"] = "generating_subtitles"
            from app.services.subtitle_engine import SubtitleEngineService
            subtitle_service = SubtitleEngineService()
            subtitle_result = await subtitle_service.generate_from_audio(
                audio_path=voice_result["audio_url"],
                style=params.get("subtitle_style", "word_highlight"),
            )
            job["progress"] = 0.75

            # Step 5: Video Rendering
            job["status"] = "rendering"
            from app.services.video_renderer import VideoRendererService
            renderer = VideoRendererService()
            
            clip_paths = [c["media"]["path"] for c in media_result["clips"]]
            render_result = await renderer.render(
                video_clips=clip_paths,
                audio_path=voice_result["audio_url"],
                subtitle_path=subtitle_result["path"],
                output_name=job_id,
            )
            job["progress"] = 0.9

            # Step 6: Optional Upload
            if params.get("auto_upload") and params.get("upload_platforms"):
                job["status"] = "uploading"
                from app.services.social_uploader import SocialUploaderService
                uploader = SocialUploaderService()
                await uploader.publish(
                    video_id=job_id,
                    platforms=params["upload_platforms"],
                    title=script.get("title", params["topic"]),
                    description=script["full_text"][:200],
                    tags=script.get("hashtags", []),
                )

            # Complete
            job["status"] = "completed"
            job["progress"] = 1.0
            job["video_url"] = render_result["path"]
            job["duration"] = render_result["duration"]
            job["completed_at"] = datetime.utcnow().isoformat()

        except Exception as e:
            job["status"] = "failed"
            job["error"] = str(e)

    async def get_job(self, job_id: str) -> Optional[dict]:
        """Get job by ID."""
        return self._jobs.get(job_id)

    async def list_jobs(
        self, status: Optional[str] = None, limit: int = 20, offset: int = 0
    ) -> dict:
        """List all jobs with optional filtering."""
        jobs = list(self._jobs.values())
        if status:
            jobs = [j for j in jobs if j["status"] == status]
        jobs.sort(key=lambda x: x["created_at"], reverse=True)
        return {"videos": jobs[offset:offset + limit], "total": len(jobs)}

    async def delete_job(self, job_id: str) -> bool:
        """Delete a job."""
        if job_id in self._jobs:
            del self._jobs[job_id]
            return True
        return False

    async def retry_job(self, job_id: str) -> Optional[dict]:
        """Retry a failed job."""
        job = self._jobs.get(job_id)
        if not job:
            return None
        job["status"] = "pending"
        job["progress"] = 0.0
        job["error"] = None
        return job
