"""
Media Collector Service
Fetches stock videos and images from Pexels, Pixabay, and other providers.
Intelligently matches visual content to script scenes.
"""

import uuid
import os
import aiohttp
from typing import Optional, List

from app.core.config import settings


class MediaCollectorService:
    """Service for collecting stock media assets."""

    PEXELS_BASE_URL = "https://api.pexels.com"
    PIXABAY_BASE_URL = "https://pixabay.com/api"

    async def search(
        self,
        query: str,
        media_type: str = "video",
        orientation: str = "portrait",
        min_duration: Optional[int] = 3,
        max_duration: Optional[int] = 15,
        per_page: int = 10,
        provider: str = "pexels",
    ) -> List[dict]:
        """
        Search for stock media matching the query.
        
        Args:
            query: Search keywords
            media_type: video or image
            orientation: portrait, landscape, or square
            min_duration: Minimum clip duration (videos only)
            max_duration: Maximum clip duration (videos only)
            per_page: Number of results to return
            provider: Media provider to use
            
        Returns:
            List of media items with download URLs
        """
        # DEMO MODE: Return mock media results
        if settings.DEMO_MODE:
            from app.services.demo_data import demo_service
            return await demo_service.search_media(query=query, per_page=per_page)

        if provider == "pexels":
            return await self._search_pexels(
                query, media_type, orientation, min_duration, max_duration, per_page
            )
        elif provider == "pixabay":
            return await self._search_pixabay(
                query, media_type, orientation, per_page
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    async def _search_pexels(
        self, query, media_type, orientation, min_duration, max_duration, per_page
    ) -> List[dict]:
        """Search Pexels API for videos or photos."""
        headers = {"Authorization": settings.PEXELS_API_KEY}

        if media_type == "video":
            url = f"{self.PEXELS_BASE_URL}/videos/search"
            params = {
                "query": query,
                "orientation": orientation,
                "per_page": per_page,
                "size": "medium",
            }
        else:
            url = f"{self.PEXELS_BASE_URL}/v1/search"
            params = {
                "query": query,
                "orientation": orientation,
                "per_page": per_page,
            }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status != 200:
                    raise Exception(f"Pexels API error: {response.status}")
                data = await response.json()

        results = []
        items = data.get("videos" if media_type == "video" else "photos", [])
        
        for item in items:
            if media_type == "video":
                duration = item.get("duration", 0)
                if min_duration and duration < min_duration:
                    continue
                if max_duration and duration > max_duration:
                    continue
                    
                # Get best quality video file
                video_files = item.get("video_files", [])
                hd_file = next(
                    (f for f in video_files if f.get("quality") == "hd"),
                    video_files[0] if video_files else None,
                )
                
                results.append({
                    "id": str(item["id"]),
                    "provider": "pexels",
                    "type": "video",
                    "url": hd_file["link"] if hd_file else "",
                    "preview_url": item.get("video_pictures", [{}])[0].get("picture", ""),
                    "thumbnail_url": item.get("image", ""),
                    "duration": duration,
                    "width": hd_file.get("width", 1080) if hd_file else 1080,
                    "height": hd_file.get("height", 1920) if hd_file else 1920,
                    "tags": [],
                })
            else:
                results.append({
                    "id": str(item["id"]),
                    "provider": "pexels",
                    "type": "image",
                    "url": item["src"]["original"],
                    "preview_url": item["src"]["large"],
                    "thumbnail_url": item["src"]["small"],
                    "duration": None,
                    "width": item["width"],
                    "height": item["height"],
                    "tags": [],
                })

        return results

    async def _search_pixabay(self, query, media_type, orientation, per_page) -> List[dict]:
        """Search Pixabay API for videos or images."""
        if media_type == "video":
            url = f"{self.PIXABAY_BASE_URL}/videos/"
        else:
            url = f"{self.PIXABAY_BASE_URL}/"

        params = {
            "key": settings.PIXABAY_API_KEY,
            "q": query,
            "orientation": "vertical" if orientation == "portrait" else orientation,
            "per_page": per_page,
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    raise Exception(f"Pixabay API error: {response.status}")
                data = await response.json()

        results = []
        for item in data.get("hits", []):
            if media_type == "video":
                videos = item.get("videos", {})
                large = videos.get("large", {})
                results.append({
                    "id": str(item["id"]),
                    "provider": "pixabay",
                    "type": "video",
                    "url": large.get("url", ""),
                    "preview_url": item.get("picture_id", ""),
                    "thumbnail_url": item.get("picture_id", ""),
                    "duration": item.get("duration", 0),
                    "width": large.get("width", 1080),
                    "height": large.get("height", 1920),
                    "tags": item.get("tags", "").split(", "),
                })
            else:
                results.append({
                    "id": str(item["id"]),
                    "provider": "pixabay",
                    "type": "image",
                    "url": item["largeImageURL"],
                    "preview_url": item["webformatURL"],
                    "thumbnail_url": item["previewURL"],
                    "duration": None,
                    "width": item["imageWidth"],
                    "height": item["imageHeight"],
                    "tags": item.get("tags", "").split(", "),
                })

        return results

    async def download(self, url: str, media_type: str = "video") -> dict:
        """Download a media file and store it locally."""
        media_id = str(uuid.uuid4())
        ext = "mp4" if media_type == "video" else "jpg"
        output_path = os.path.join(settings.TEMP_DIR, f"media_{media_id}.{ext}")
        os.makedirs(settings.TEMP_DIR, exist_ok=True)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"Download failed: {response.status}")
                with open(output_path, "wb") as f:
                    async for chunk in response.content.iter_chunked(8192):
                        f.write(chunk)

        return {
            "id": media_id,
            "path": output_path,
            "type": media_type,
            "size": os.path.getsize(output_path),
        }

    async def auto_collect(self, script_id: str, clips_needed: int = 5) -> dict:
        """
        Automatically collect media based on script content.
        
        Analyzes the script sections, extracts visual keywords,
        and fetches matching stock footage for each scene.
        """
        # DEMO MODE: Return mock auto-collected media
        if settings.DEMO_MODE:
            from app.services.demo_data import demo_service
            return await demo_service.auto_collect_media(script_id=script_id, clips_needed=clips_needed)

        import openai
        
        # Get script from database
        from app.services.script_generator import ScriptGeneratorService
        script_service = ScriptGeneratorService()
        script = await script_service.get_by_id(script_id)
        
        if not script:
            raise Exception("Script not found")

        # Use AI to extract visual search queries from script
        client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Extract visual search keywords for stock footage. Return a JSON array of search queries.",
                },
                {
                    "role": "user",
                    "content": f"Extract {clips_needed} visual search queries for stock video footage based on this script:\n\n{script.get('full_text', '')}",
                },
            ],
            response_format={"type": "json_object"},
        )

        import json
        queries = json.loads(response.choices[0].message.content)
        search_terms = queries.get("queries", queries.get("keywords", []))[:clips_needed]

        # Search and download media for each query
        collected = []
        for query in search_terms:
            results = await self.search(
                query=query if isinstance(query, str) else query.get("query", ""),
                media_type="video",
                orientation="portrait",
                per_page=2,
            )
            if results:
                downloaded = await self.download(results[0]["url"], "video")
                collected.append({
                    "query": query,
                    "media": downloaded,
                    "source": results[0],
                })

        return {
            "script_id": script_id,
            "clips_collected": len(collected),
            "clips": collected,
        }
