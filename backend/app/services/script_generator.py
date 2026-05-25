"""
Script Generator Service
AI-powered script generation for short-form video content.
Uses OpenAI GPT-4 or Claude for intelligent content creation.
"""

import json
import uuid
from typing import Optional
from datetime import datetime

from app.core.config import settings


class ScriptGeneratorService:
    """Service for generating video scripts using AI."""

    SYSTEM_PROMPT = """You are an expert short-form video scriptwriter specializing in 
viral content for YouTube Shorts, Instagram Reels, and TikTok. 

Your scripts follow this structure:
1. HOOK (first 3 seconds): A compelling opening that stops scrolling
2. BODY (main content): Engaging, concise information delivery
3. CTA (call to action): Clear next step for viewers

Guidelines:
- Write conversationally, as if speaking directly to one person
- Use short sentences and punchy language
- Include natural pauses and emphasis markers
- Suggest visual elements for each section
- Optimize for the target duration
- Include trending hooks and viral patterns"""

    async def generate(
        self,
        topic: str,
        tone: str = "informative",
        duration: int = 60,
        style: Optional[str] = "viral",
        target_audience: Optional[str] = "general",
        include_hook: bool = True,
        include_cta: bool = True,
        language: str = "en",
    ) -> dict:
        """
        Generate a script using AI.
        
        Args:
            topic: The main topic/subject of the video
            tone: informative, entertaining, motivational, etc.
            duration: Target duration in seconds
            style: viral, educational, storytelling, etc.
            target_audience: Who the video is for
            include_hook: Whether to include an opening hook
            include_cta: Whether to include a call to action
            language: Output language code
            
        Returns:
            Complete script with sections, timing, and visual suggestions
        """
        import openai

        client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        # Calculate word budget (average speaking rate ~150 words/minute)
        word_budget = int((duration / 60) * 150)

        user_prompt = f"""Create a short-form video script about: "{topic}"

Requirements:
- Tone: {tone}
- Style: {style}
- Target audience: {target_audience}
- Duration: ~{duration} seconds ({word_budget} words max)
- Language: {language}
- Include hook: {include_hook}
- Include CTA: {include_cta}

Return a JSON object with this exact structure:
{{
    "title": "Video title (catchy, SEO-friendly)",
    "sections": [
        {{
            "type": "hook",
            "text": "The hook text...",
            "estimated_duration": 3.0,
            "visual_suggestion": "What visuals to show"
        }},
        {{
            "type": "body",
            "text": "Main content...",
            "estimated_duration": 50.0,
            "visual_suggestion": "Visual suggestions..."
        }},
        {{
            "type": "cta",
            "text": "Call to action...",
            "estimated_duration": 7.0,
            "visual_suggestion": "Visual suggestions..."
        }}
    ],
    "hashtags": ["#tag1", "#tag2", "#tag3"],
    "metadata": {{
        "target_platform": "youtube_shorts",
        "content_category": "educational",
        "engagement_hooks": ["curiosity gap", "pattern interrupt"]
    }}
}}"""

        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.8,
            max_tokens=2000,
            response_format={"type": "json_object"},
        )

        script_data = json.loads(response.choices[0].message.content)
        
        # Build full text from sections
        full_text = " ".join(s["text"] for s in script_data["sections"])
        word_count = len(full_text.split())
        total_duration = sum(s["estimated_duration"] for s in script_data["sections"])

        return {
            "id": str(uuid.uuid4()),
            "topic": topic,
            "title": script_data["title"],
            "sections": script_data["sections"],
            "full_text": full_text,
            "word_count": word_count,
            "estimated_duration": total_duration,
            "hashtags": script_data.get("hashtags", []),
            "metadata": {
                **script_data.get("metadata", {}),
                "tone": tone,
                "style": style,
                "language": language,
                "generated_at": datetime.utcnow().isoformat(),
            },
        }

    async def get_by_id(self, script_id: str) -> Optional[dict]:
        """Retrieve a script by ID from the database."""
        from app.core.database import get_supabase
        
        db = get_supabase()
        if db:
            response = db.table("scripts").select("*").eq("id", script_id).execute()
            return response.data[0] if response.data else None
        return None

    async def list_all(self, limit: int = 20, offset: int = 0) -> dict:
        """List all scripts with pagination."""
        from app.core.database import get_supabase
        
        db = get_supabase()
        if db:
            response = (
                db.table("scripts")
                .select("*")
                .order("created_at", desc=True)
                .range(offset, offset + limit - 1)
                .execute()
            )
            return {"scripts": response.data, "total": len(response.data)}
        return {"scripts": [], "total": 0}

    async def regenerate(self, script_id: str) -> Optional[dict]:
        """Regenerate a script with same parameters."""
        original = await self.get_by_id(script_id)
        if not original:
            return None
        return await self.generate(
            topic=original["topic"],
            tone=original["metadata"].get("tone", "informative"),
            duration=int(original["estimated_duration"]),
            style=original["metadata"].get("style", "viral"),
        )
