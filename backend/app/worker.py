"""
Celery Worker Configuration
Handles background video generation tasks with Redis as broker.
"""

from celery import Celery

from app.core.config import settings

# Initialize Celery
celery_app = Celery(
    "videogen",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

# Celery Configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=600,  # 10 minutes max per task
    task_soft_time_limit=540,  # Soft limit at 9 minutes
    worker_prefetch_multiplier=1,  # Process one task at a time
    worker_max_tasks_per_child=50,  # Restart worker after 50 tasks
)


@celery_app.task(bind=True, name="generate_video")
def generate_video_task(self, job_params: dict):
    """
    Background task for video generation pipeline.
    
    This task is triggered by the API and runs the full pipeline:
    1. Script generation
    2. Voice generation
    3. Media collection
    4. Subtitle generation
    5. Video rendering
    6. Optional social upload
    """
    import asyncio
    from app.services.video_pipeline import VideoPipelineService

    async def run():
        service = VideoPipelineService()
        job = await service.create_job(job_params)
        self.update_state(state="STARTED", meta={"job_id": job["id"]})
        await service.execute_pipeline(job["id"])
        return job["id"]

    return asyncio.run(run())


@celery_app.task(name="batch_generate")
def batch_generate_task(topics: list, config: dict):
    """Generate multiple videos from a list of topics."""
    import asyncio
    from app.services.video_pipeline import VideoPipelineService

    async def run():
        service = VideoPipelineService()
        results = []
        for topic in topics:
            params = {**config, "topic": topic}
            job = await service.create_job(params)
            await service.execute_pipeline(job["id"])
            results.append(job["id"])
        return results

    return asyncio.run(run())


@celery_app.task(name="scheduled_generation")
def scheduled_generation_task(schedule_id: str):
    """Execute a scheduled video generation."""
    import asyncio

    async def run():
        # Fetch schedule config from database
        # Generate trending topic
        # Run pipeline
        pass

    return asyncio.run(run())
