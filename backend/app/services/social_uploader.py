"""
Social Uploader Service
Handles video publishing to YouTube, Instagram, and TikTok.
Manages OAuth flows and upload scheduling.
"""

import os
from typing import Optional, List
from datetime import datetime

from app.core.config import settings


class SocialUploaderService:
    """Service for uploading videos to social media platforms."""

    async def publish(
        self,
        video_id: str,
        platforms: List[str],
        title: str,
        description: str,
        tags: List[str] = [],
        schedule_at: Optional[datetime] = None,
        visibility: str = "public",
    ) -> dict:
        """
        Publish video to specified platforms.
        
        Supports YouTube Shorts, Instagram Reels, and TikTok.
        """
        # DEMO MODE: Return mock publish results
        if settings.DEMO_MODE:
            from app.services.demo_data import demo_service
            return await demo_service.publish(
                video_id=video_id, platforms=platforms, title=title, description=description
            )

        results = []
        
        for platform in platforms:
            try:
                if platform == "youtube":
                    result = await self._upload_youtube(
                        video_id, title, description, tags, visibility
                    )
                elif platform == "instagram":
                    result = await self._upload_instagram(
                        video_id, title, description, tags
                    )
                elif platform == "tiktok":
                    result = await self._upload_tiktok(
                        video_id, title, description, tags
                    )
                else:
                    result = {"platform": platform, "status": "unsupported"}
                results.append(result)
            except Exception as e:
                results.append({
                    "platform": platform,
                    "status": "failed",
                    "error": str(e),
                })

        return {"video_id": video_id, "uploads": results}


    async def _upload_youtube(
        self, video_id: str, title: str, description: str,
        tags: List[str], visibility: str
    ) -> dict:
        """Upload to YouTube Shorts via YouTube Data API v3."""
        # YouTube upload using google-api-python-client
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        
        video_path = os.path.join(settings.OUTPUT_DIR, f"video_{video_id}.mp4")
        
        # Build YouTube service (requires OAuth2 credentials)
        youtube = build("youtube", "v3", credentials=None)  # TODO: OAuth flow
        
        body = {
            "snippet": {
                "title": title[:100],
                "description": f"{description}\n\n{' '.join(tags)}",
                "tags": [t.replace('#', '') for t in tags],
                "categoryId": "22",  # People & Blogs
            },
            "status": {
                "privacyStatus": visibility,
                "selfDeclaredMadeForKids": False,
                "shorts": {"isShort": True},
            },
        }
        
        media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)
        request = youtube.videos().insert(
            part="snippet,status", body=body, media_body=media
        )
        
        response = request.execute()
        
        return {
            "platform": "youtube",
            "status": "published",
            "url": f"https://youtube.com/shorts/{response['id']}",
            "video_id": response["id"],
            "uploaded_at": datetime.utcnow().isoformat(),
        }

    async def _upload_instagram(
        self, video_id: str, title: str, description: str, tags: List[str]
    ) -> dict:
        """Upload to Instagram Reels via Graph API."""
        import aiohttp
        
        video_path = os.path.join(settings.OUTPUT_DIR, f"video_{video_id}.mp4")
        caption = f"{title}\n\n{description}\n\n{' '.join(tags)}"
        
        # Instagram Graph API requires video URL (not local file)
        # Upload to Cloudinary first, then use the URL
        video_url = await self._upload_to_cdn(video_path)
        
        async with aiohttp.ClientSession() as session:
            # Step 1: Create media container
            create_url = "https://graph.instagram.com/v18.0/me/media"
            create_params = {
                "media_type": "REELS",
                "video_url": video_url,
                "caption": caption[:2200],
                "access_token": settings.INSTAGRAM_ACCESS_TOKEN,
            }
            async with session.post(create_url, params=create_params) as resp:
                data = await resp.json()
                container_id = data["id"]
            
            # Step 2: Publish
            publish_url = "https://graph.instagram.com/v18.0/me/media_publish"
            publish_params = {
                "creation_id": container_id,
                "access_token": settings.INSTAGRAM_ACCESS_TOKEN,
            }
            async with session.post(publish_url, params=publish_params) as resp:
                result = await resp.json()

        return {
            "platform": "instagram",
            "status": "published",
            "url": f"https://instagram.com/reel/{result['id']}",
            "uploaded_at": datetime.utcnow().isoformat(),
        }

    async def _upload_tiktok(
        self, video_id: str, title: str, description: str, tags: List[str]
    ) -> dict:
        """Upload to TikTok via TikTok API."""
        # TikTok Content Posting API
        return {
            "platform": "tiktok",
            "status": "pending",
            "message": "TikTok upload requires manual OAuth approval",
        }

    async def _upload_to_cdn(self, file_path: str) -> str:
        """Upload file to Cloudinary CDN and return URL."""
        import cloudinary.uploader
        
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
        )
        
        result = cloudinary.uploader.upload(
            file_path, resource_type="video", folder="shorts"
        )
        return result["secure_url"]

    async def get_status(self, video_id: str) -> List[dict]:
        """Get upload status for all platforms."""
        # TODO: Query database for upload records
        return []

    async def authenticate(self, platform: str, code: str) -> dict:
        """Complete OAuth flow for a platform."""
        # TODO: Implement OAuth token exchange
        return {"platform": platform, "status": "authenticated"}

    async def get_auth_url(self, platform: str) -> dict:
        """Get OAuth authorization URL."""
        urls = {
            "youtube": "https://accounts.google.com/o/oauth2/v2/auth",
            "instagram": "https://api.instagram.com/oauth/authorize",
            "tiktok": "https://www.tiktok.com/v2/auth/authorize/",
        }
        return {"platform": platform, "auth_url": urls.get(platform, "")}
