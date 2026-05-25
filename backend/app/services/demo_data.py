"""
Demo Data Service
Provides realistic mock data for all services when DEMO_MODE=true.
Allows the entire platform to run without spending money on API keys.
"""

import uuid
import os
import random
from datetime import datetime, timedelta
from typing import List, Optional

from app.core.config import settings


# ============================================================
# DEMO SCRIPTS
# ============================================================

DEMO_SCRIPTS = [
    {
        "topic": "5 AI Tools That Will Change Your Life",
        "title": "5 AI Tools You NEED to Try Right Now",
        "sections": [
            {
                "type": "hook",
                "text": "Stop what you're doing. These 5 AI tools are about to make your life 10x easier, and most people don't even know they exist.",
                "estimated_duration": 5.0,
                "visual_suggestion": "Fast-paced montage of AI interfaces with glowing effects"
            },
            {
                "type": "body",
                "text": "Number one: Perplexity AI. It's like Google, but it actually gives you answers instead of links. Number two: Gamma. Create stunning presentations in 30 seconds. Number three: ElevenLabs. Clone any voice with just a 30-second sample. Number four: Runway ML. Generate Hollywood-quality video effects from text. Number five: Cursor AI. It writes code faster than you can think.",
                "estimated_duration": 45.0,
                "visual_suggestion": "Screen recordings of each tool with smooth transitions"
            },
            {
                "type": "cta",
                "text": "Follow for more AI tools that actually work. Which one are you trying first? Comment below!",
                "estimated_duration": 7.0,
                "visual_suggestion": "Subscribe animation with arrow pointing to follow button"
            }
        ],
        "hashtags": ["#AI", "#AITools", "#Productivity", "#TechTips", "#ArtificialIntelligence"],
    },
    {
        "topic": "Why You Should Learn Python in 2024",
        "title": "Python in 2024: Here's Why It's Taking Over",
        "sections": [
            {
                "type": "hook",
                "text": "Python developers are getting paid 120K a year, and it only takes 3 months to learn. Here's why.",
                "estimated_duration": 4.0,
                "visual_suggestion": "Salary chart animation with Python logo"
            },
            {
                "type": "body",
                "text": "Python is the number one language for AI, data science, automation, and web development. Companies like Google, Netflix, and Instagram all run on Python. The syntax is so simple, it reads like English. You can automate your boring tasks, build AI models, create websites, or analyze data. And the best part? There are thousands of free resources to learn it.",
                "estimated_duration": 48.0,
                "visual_suggestion": "Code snippets appearing on screen with company logos"
            },
            {
                "type": "cta",
                "text": "Drop a fire emoji if you're starting Python this week. Follow for more tech career tips!",
                "estimated_duration": 6.0,
                "visual_suggestion": "Animated fire emojis with follow button highlight"
            }
        ],
        "hashtags": ["#Python", "#Coding", "#Programming", "#TechCareer", "#LearnToCode"],
    },
    {
        "topic": "Morning Routine That Changed My Life",
        "title": "The 5 AM Routine That Made Me Successful",
        "sections": [
            {
                "type": "hook",
                "text": "I woke up at 5 AM every day for 30 days, and it completely transformed my productivity.",
                "estimated_duration": 4.0,
                "visual_suggestion": "Alarm clock at 5 AM, dark room transitioning to sunrise"
            },
            {
                "type": "body",
                "text": "Here's my exact routine. Five AM: wake up, no snooze. First thing, I drink a full glass of water. Then 10 minutes of meditation using the Headspace app. Next, 20 minutes of exercise. Nothing crazy, just a walk or stretching. Then I journal for 5 minutes about my goals. By 6 AM, I've already accomplished more than most people do by noon.",
                "estimated_duration": 46.0,
                "visual_suggestion": "Aesthetic morning footage, person doing each activity"
            },
            {
                "type": "cta",
                "text": "Save this for tomorrow morning. Follow for more productivity hacks!",
                "estimated_duration": 5.0,
                "visual_suggestion": "Save icon animation with sunrise background"
            }
        ],
        "hashtags": ["#MorningRoutine", "#Productivity", "#SelfImprovement", "#5AMClub", "#Success"],
    },
]

DEMO_VIDEOS = [
    {
        "id": "demo-vid-001",
        "topic": "5 AI Tools That Will Change Your Life",
        "title": "5 AI Tools You NEED to Try Right Now",
        "status": "completed",
        "progress": 1.0,
        "duration": 57.0,
        "video_url": "/output/demo_video_001.mp4",
        "thumbnail_url": "https://images.pexels.com/photos/8386440/pexels-photo-8386440.jpeg?auto=compress&cs=tinysrgb&w=400",
        "views": 12400,
        "likes": 890,
        "platform": "YouTube Shorts",
    },
    {
        "id": "demo-vid-002",
        "topic": "Why You Should Learn Python in 2024",
        "title": "Python in 2024: Here's Why It's Taking Over",
        "status": "completed",
        "progress": 1.0,
        "duration": 58.0,
        "video_url": "/output/demo_video_002.mp4",
        "thumbnail_url": "https://images.pexels.com/photos/1181671/pexels-photo-1181671.jpeg?auto=compress&cs=tinysrgb&w=400",
        "views": 8200,
        "likes": 670,
        "platform": "Instagram Reels",
    },
    {
        "id": "demo-vid-003",
        "topic": "Morning Routine That Changed My Life",
        "title": "The 5 AM Routine That Made Me Successful",
        "status": "completed",
        "progress": 1.0,
        "duration": 55.0,
        "video_url": "/output/demo_video_003.mp4",
        "thumbnail_url": "https://images.pexels.com/photos/3760607/pexels-photo-3760607.jpeg?auto=compress&cs=tinysrgb&w=400",
        "views": 23100,
        "likes": 1800,
        "platform": "TikTok",
    },
    {
        "id": "demo-vid-004",
        "topic": "Web Development in 60 Seconds",
        "title": "Build a Website in Under a Minute",
        "status": "rendering",
        "progress": 0.75,
        "duration": None,
        "video_url": None,
        "thumbnail_url": None,
        "views": 0,
        "likes": 0,
        "platform": "YouTube Shorts",
    },
    {
        "id": "demo-vid-005",
        "topic": "The Future of Remote Work",
        "title": "Remote Work is Dead? Think Again.",
        "status": "completed",
        "progress": 1.0,
        "duration": 50.0,
        "video_url": "/output/demo_video_005.mp4",
        "thumbnail_url": "https://images.pexels.com/photos/4050315/pexels-photo-4050315.jpeg?auto=compress&cs=tinysrgb&w=400",
        "views": 15800,
        "likes": 1200,
        "platform": "Instagram Reels",
    },
]

DEMO_MEDIA_RESULTS = [
    {
        "id": "pexels-001",
        "provider": "pexels",
        "type": "video",
        "url": "https://www.pexels.com/video/person-using-laptop-5926382/",
        "preview_url": "https://images.pexels.com/videos/5926382/pexels-photo-5926382.jpeg?auto=compress&w=400",
        "thumbnail_url": "https://images.pexels.com/videos/5926382/pexels-photo-5926382.jpeg?auto=compress&w=200",
        "duration": 8.0,
        "width": 1080,
        "height": 1920,
        "tags": ["technology", "laptop", "coding"],
    },
    {
        "id": "pexels-002",
        "provider": "pexels",
        "type": "video",
        "url": "https://www.pexels.com/video/abstract-technology-5377684/",
        "preview_url": "https://images.pexels.com/videos/5377684/pexels-photo-5377684.jpeg?auto=compress&w=400",
        "thumbnail_url": "https://images.pexels.com/videos/5377684/pexels-photo-5377684.jpeg?auto=compress&w=200",
        "duration": 12.0,
        "width": 1080,
        "height": 1920,
        "tags": ["abstract", "technology", "data"],
    },
    {
        "id": "pexels-003",
        "provider": "pexels",
        "type": "video",
        "url": "https://www.pexels.com/video/person-typing-keyboard-5496463/",
        "preview_url": "https://images.pexels.com/videos/5496463/pexels-photo-5496463.jpeg?auto=compress&w=400",
        "thumbnail_url": "https://images.pexels.com/videos/5496463/pexels-photo-5496463.jpeg?auto=compress&w=200",
        "duration": 6.0,
        "width": 1080,
        "height": 1920,
        "tags": ["typing", "keyboard", "work"],
    },
    {
        "id": "pexels-004",
        "provider": "pexels",
        "type": "video",
        "url": "https://www.pexels.com/video/city-skyline-night-3571264/",
        "preview_url": "https://images.pexels.com/videos/3571264/pexels-photo-3571264.jpeg?auto=compress&w=400",
        "thumbnail_url": "https://images.pexels.com/videos/3571264/pexels-photo-3571264.jpeg?auto=compress&w=200",
        "duration": 10.0,
        "width": 1080,
        "height": 1920,
        "tags": ["city", "night", "skyline"],
    },
    {
        "id": "pexels-005",
        "provider": "pexels",
        "type": "video",
        "url": "https://www.pexels.com/video/sunrise-morning-nature-4793729/",
        "preview_url": "https://images.pexels.com/videos/4793729/pexels-photo-4793729.jpeg?auto=compress&w=400",
        "thumbnail_url": "https://images.pexels.com/videos/4793729/pexels-photo-4793729.jpeg?auto=compress&w=200",
        "duration": 7.0,
        "width": 1080,
        "height": 1920,
        "tags": ["sunrise", "morning", "nature"],
    },
]


class DemoService:
    """Provides demo/mock data for all services when running without API keys."""

    # ============================================================
    # SCRIPT GENERATION (Mock)
    # ============================================================
    
    async def generate_script(self, topic: str, tone: str = "informative", duration: int = 60, **kwargs) -> dict:
        """Generate a realistic demo script based on topic."""
        # Pick a template and customize it
        template = random.choice(DEMO_SCRIPTS)
        
        script_id = str(uuid.uuid4())
        
        # Use actual topic in the response
        sections = [
            {
                "type": "hook",
                "text": f"Stop scrolling! What I'm about to tell you about {topic} will blow your mind.",
                "estimated_duration": 4.0,
                "visual_suggestion": "Eye-catching visual with bold text overlay"
            },
            {
                "type": "body",
                "text": f"Here's the thing about {topic} that nobody talks about. The world is changing fast, and if you're not paying attention, you'll be left behind. Let me break this down for you in the simplest way possible. First, the technology behind this is evolving at an exponential rate. Second, early adopters are seeing massive results. Third, it's more accessible than ever before. The key is to start now, even if you start small.",
                "estimated_duration": float(duration - 12),
                "visual_suggestion": "Dynamic b-roll footage with text callouts for key points"
            },
            {
                "type": "cta",
                "text": "Follow for more insights like this, and comment which point resonated with you the most!",
                "estimated_duration": 6.0,
                "visual_suggestion": "Subscribe/follow animation with engagement prompts"
            }
        ]
        
        full_text = " ".join(s["text"] for s in sections)
        
        return {
            "id": script_id,
            "topic": topic,
            "title": f"{topic} - What Nobody Tells You",
            "sections": sections,
            "full_text": full_text,
            "word_count": len(full_text.split()),
            "estimated_duration": float(duration),
            "hashtags": [f"#{topic.split()[0]}", "#Viral", "#MustWatch", "#LifeHacks", "#Trending"],
            "metadata": {
                "tone": tone,
                "style": kwargs.get("style", "viral"),
                "language": "en",
                "generated_at": datetime.utcnow().isoformat(),
                "demo_mode": True,
            },
        }

    # ============================================================
    # VOICE GENERATION (Mock)
    # ============================================================
    
    async def generate_voice(self, text: str, voice_id: str = "default", **kwargs) -> dict:
        """Return a mock voice generation result."""
        audio_id = str(uuid.uuid4())
        
        # Calculate approximate duration (150 words per minute)
        word_count = len(text.split())
        duration = (word_count / 150) * 60
        
        # Generate fake word timestamps
        words = text.split()
        timestamps = []
        current_time = 0.0
        for word in words:
            word_duration = random.uniform(0.2, 0.5)
            timestamps.append({
                "word": word,
                "start": round(current_time, 2),
                "end": round(current_time + word_duration, 2),
            })
            current_time += word_duration + random.uniform(0.05, 0.15)
        
        return {
            "id": audio_id,
            "audio_url": f"./temp/voice_{audio_id}.mp3",
            "duration": round(duration, 1),
            "timestamps": {"words": timestamps},
            "provider": "demo",
            "voice_id": voice_id,
            "demo_mode": True,
            "message": "Demo mode: No actual audio generated. Enable real API keys for TTS.",
        }

    # ============================================================
    # MEDIA COLLECTION (Mock)
    # ============================================================
    
    async def search_media(self, query: str, **kwargs) -> List[dict]:
        """Return demo media search results."""
        # Return shuffled demo results
        results = DEMO_MEDIA_RESULTS.copy()
        random.shuffle(results)
        per_page = kwargs.get("per_page", 5)
        return results[:per_page]
    
    async def auto_collect_media(self, script_id: str, clips_needed: int = 5) -> dict:
        """Return demo auto-collected media."""
        clips = []
        for i in range(min(clips_needed, len(DEMO_MEDIA_RESULTS))):
            clips.append({
                "query": f"demo query {i+1}",
                "media": {
                    "id": str(uuid.uuid4()),
                    "path": f"./temp/media_demo_{i}.mp4",
                    "type": "video",
                    "size": random.randint(1000000, 5000000),
                },
                "source": DEMO_MEDIA_RESULTS[i],
            })
        
        return {
            "script_id": script_id,
            "clips_collected": len(clips),
            "clips": clips,
            "demo_mode": True,
        }

    # ============================================================
    # SUBTITLE GENERATION (Mock)
    # ============================================================
    
    async def generate_subtitles(self, text: str = "", audio_path: str = "", **kwargs) -> dict:
        """Return demo subtitle result."""
        subtitle_id = str(uuid.uuid4())
        return {
            "id": subtitle_id,
            "path": f"./temp/subtitles_{subtitle_id}.ass",
            "format": "ass",
            "style": kwargs.get("style", "word_highlight"),
            "word_count": len(text.split()) if text else 120,
            "duration": 60.0,
            "demo_mode": True,
        }

    # ============================================================
    # VIDEO RENDERING (Mock)
    # ============================================================
    
    async def render_video(self, **kwargs) -> dict:
        """Return demo render result."""
        render_id = str(uuid.uuid4())
        return {
            "id": render_id,
            "path": f"./output/video_{render_id}.mp4",
            "duration": random.uniform(45.0, 65.0),
            "size_bytes": random.randint(5000000, 15000000),
            "resolution": "1080x1920",
            "fps": 30,
            "codec": "libx264",
            "demo_mode": True,
            "message": "Demo mode: No actual video rendered. Enable real API keys + FFmpeg for rendering.",
        }

    # ============================================================
    # ANALYTICS (Mock)
    # ============================================================
    
    async def get_dashboard_stats(self) -> dict:
        """Return realistic demo dashboard stats."""
        return {
            "total_videos": 47,
            "videos_published": 38,
            "total_views": 124500,
            "success_rate": 94.5,
            "avg_generation_time_seconds": 145,
            "videos_this_week": 12,
            "platforms_connected": 2,
            "storage_used_mb": 2340,
        }

    async def get_video_performance(self, video_id: str) -> dict:
        """Return demo video performance."""
        return {
            "video_id": video_id,
            "platforms": [
                {"platform": "youtube", "views": random.randint(5000, 25000), "likes": random.randint(200, 2000)},
                {"platform": "instagram", "views": random.randint(3000, 15000), "likes": random.randint(100, 1500)},
            ],
            "total_views": random.randint(8000, 40000),
            "total_likes": random.randint(300, 3500),
            "total_comments": random.randint(20, 300),
            "total_shares": random.randint(10, 200),
        }

    async def get_trends(self, days: int = 30) -> dict:
        """Return demo trends data."""
        daily_generations = []
        daily_views = []
        for i in range(days):
            date = (datetime.utcnow() - timedelta(days=days - i)).strftime("%Y-%m-%d")
            daily_generations.append({"date": date, "count": random.randint(1, 5)})
            daily_views.append({"date": date, "views": random.randint(500, 5000)})
        
        return {
            "period_days": days,
            "daily_generations": daily_generations,
            "daily_views": daily_views,
            "top_topics": ["AI Tools", "Python", "Productivity", "Tech Career", "Side Hustles"],
            "platform_breakdown": {
                "youtube": 45,
                "instagram": 35,
                "tiktok": 20,
            },
        }

    async def get_logs(self, limit: int = 50, offset: int = 0, status: Optional[str] = None) -> dict:
        """Return demo generation logs."""
        statuses = ["completed", "completed", "completed", "failed", "completed"]
        logs = []
        for i in range(min(limit, 20)):
            log_status = random.choice(statuses) if not status else status
            logs.append({
                "id": str(uuid.uuid4()),
                "video_id": f"demo-vid-{i:03d}",
                "step": random.choice(["script_generation", "voice_generation", "media_collection", "video_rendering"]),
                "status": log_status,
                "duration_ms": random.randint(2000, 30000),
                "created_at": (datetime.utcnow() - timedelta(hours=random.randint(1, 168))).isoformat(),
            })
        return {"logs": logs, "total": len(logs)}

    # ============================================================
    # VIDEO LIST (Mock)
    # ============================================================
    
    async def list_videos(self, status: Optional[str] = None, limit: int = 20, offset: int = 0) -> dict:
        """Return demo video list."""
        videos = []
        for v in DEMO_VIDEOS:
            if status and v["status"] != status:
                continue
            videos.append({
                "id": v["id"],
                "status": v["status"],
                "topic": v["topic"],
                "progress": v["progress"],
                "script_id": f"script-{v['id']}",
                "video_url": v["video_url"],
                "thumbnail_url": v["thumbnail_url"],
                "duration": v["duration"],
                "created_at": (datetime.utcnow() - timedelta(hours=random.randint(1, 72))).isoformat(),
                "completed_at": (datetime.utcnow() - timedelta(hours=random.randint(0, 70))).isoformat() if v["status"] == "completed" else None,
            })
        return {"videos": videos[offset:offset+limit], "total": len(videos)}

    # ============================================================
    # SOCIAL UPLOAD (Mock)
    # ============================================================
    
    async def publish(self, video_id: str, platforms: List[str], **kwargs) -> dict:
        """Return demo publish result."""
        uploads = []
        for platform in platforms:
            uploads.append({
                "platform": platform,
                "status": "published",
                "url": f"https://{platform}.com/shorts/demo-{video_id[:8]}",
                "uploaded_at": datetime.utcnow().isoformat(),
                "demo_mode": True,
            })
        return {"video_id": video_id, "uploads": uploads}


# Global demo service instance
demo_service = DemoService()
