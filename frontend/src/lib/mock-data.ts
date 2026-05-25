/**
 * Mock Data for Frontend Demo Mode
 * Used when backend is not available or for standalone demo.
 * This allows the entire frontend to work without any backend running.
 */

export const mockDashboardStats = {
  total_videos: 47,
  videos_published: 38,
  total_views: 124500,
  success_rate: 94.5,
  avg_generation_time_seconds: 145,
  videos_this_week: 12,
  platforms_connected: 2,
  storage_used_mb: 2340,
};

export const mockVideos = [
  {
    id: "demo-vid-001",
    topic: "5 AI Tools That Will Change Your Life",
    status: "completed",
    progress: 1.0,
    script_id: "script-001",
    video_url: "/output/demo_video_001.mp4",
    thumbnail_url: "https://images.pexels.com/photos/8386440/pexels-photo-8386440.jpeg?auto=compress&cs=tinysrgb&w=400",
    duration: 57.0,
    created_at: new Date(Date.now() - 2 * 3600000).toISOString(),
    completed_at: new Date(Date.now() - 1.5 * 3600000).toISOString(),
  },
  {
    id: "demo-vid-002",
    topic: "Why Python is Taking Over in 2024",
    status: "completed",
    progress: 1.0,
    script_id: "script-002",
    video_url: "/output/demo_video_002.mp4",
    thumbnail_url: "https://images.pexels.com/photos/1181671/pexels-photo-1181671.jpeg?auto=compress&cs=tinysrgb&w=400",
    duration: 58.0,
    created_at: new Date(Date.now() - 4 * 3600000).toISOString(),
    completed_at: new Date(Date.now() - 3.5 * 3600000).toISOString(),
  },
  {
    id: "demo-vid-003",
    topic: "Morning Routine That Changed My Life",
    status: "completed",
    progress: 1.0,
    script_id: "script-003",
    video_url: "/output/demo_video_003.mp4",
    thumbnail_url: "https://images.pexels.com/photos/3760607/pexels-photo-3760607.jpeg?auto=compress&cs=tinysrgb&w=400",
    duration: 55.0,
    created_at: new Date(Date.now() - 24 * 3600000).toISOString(),
    completed_at: new Date(Date.now() - 23 * 3600000).toISOString(),
  },
  {
    id: "demo-vid-004",
    topic: "Web Development in 60 Seconds",
    status: "rendering",
    progress: 0.75,
    script_id: "script-004",
    video_url: null,
    thumbnail_url: null,
    duration: null,
    created_at: new Date(Date.now() - 0.5 * 3600000).toISOString(),
    completed_at: null,
  },
  {
    id: "demo-vid-005",
    topic: "The Future of Remote Work",
    status: "completed",
    progress: 1.0,
    script_id: "script-005",
    video_url: "/output/demo_video_005.mp4",
    thumbnail_url: "https://images.pexels.com/photos/4050315/pexels-photo-4050315.jpeg?auto=compress&cs=tinysrgb&w=400",
    duration: 50.0,
    created_at: new Date(Date.now() - 48 * 3600000).toISOString(),
    completed_at: new Date(Date.now() - 47 * 3600000).toISOString(),
  },
];

export const mockScriptGeneration = {
  id: "script-new-001",
  topic: "5 AI tools that will blow your mind",
  title: "5 AI Tools You NEED to Try Right Now",
  sections: [
    {
      type: "hook",
      text: "Stop scrolling! These 5 AI tools are about to make your life 10x easier, and most people don't even know they exist.",
      estimated_duration: 5.0,
      visual_suggestion: "Fast-paced montage of AI interfaces with glowing effects",
    },
    {
      type: "body",
      text: "Number one: Perplexity AI. It's like Google, but it actually gives you answers instead of links. Number two: Gamma. Create stunning presentations in 30 seconds. Number three: ElevenLabs. Clone any voice with just a 30-second sample. Number four: Runway ML. Generate Hollywood-quality video effects from text. Number five: Cursor AI. It writes code faster than you can think.",
      estimated_duration: 48.0,
      visual_suggestion: "Screen recordings of each tool with smooth transitions",
    },
    {
      type: "cta",
      text: "Follow for more AI tools that actually work. Which one are you trying first? Comment below!",
      estimated_duration: 7.0,
      visual_suggestion: "Subscribe animation with arrow pointing to follow button",
    },
  ],
  full_text: "Stop scrolling! These 5 AI tools are about to make your life 10x easier. Number one: Perplexity AI. Number two: Gamma. Number three: ElevenLabs. Number four: Runway ML. Number five: Cursor AI. Follow for more AI tools that actually work!",
  word_count: 142,
  estimated_duration: 60.0,
  hashtags: ["#AI", "#AITools", "#Productivity", "#TechTips", "#ArtificialIntelligence"],
  metadata: {
    tone: "informative",
    style: "viral",
    language: "en",
    generated_at: new Date().toISOString(),
    demo_mode: true,
  },
};

export const mockVoices = [
  { id: "rachel", name: "Rachel", provider: "elevenlabs", language: "en", gender: "female", preview_url: null, description: "Calm and professional female voice" },
  { id: "domi", name: "Domi", provider: "elevenlabs", language: "en", gender: "female", preview_url: null, description: "Energetic and young female voice" },
  { id: "bella", name: "Bella", provider: "elevenlabs", language: "en", gender: "female", preview_url: null, description: "Soft and friendly female voice" },
  { id: "antoni", name: "Antoni", provider: "elevenlabs", language: "en", gender: "male", preview_url: null, description: "Clear and confident male voice" },
  { id: "arnold", name: "Arnold", provider: "elevenlabs", language: "en", gender: "male", preview_url: null, description: "Deep and authoritative male voice" },
  { id: "alloy", name: "Alloy", provider: "openai", language: "en", gender: "neutral", preview_url: null, description: "OpenAI alloy voice" },
  { id: "echo", name: "Echo", provider: "openai", language: "en", gender: "neutral", preview_url: null, description: "OpenAI echo voice" },
  { id: "nova", name: "Nova", provider: "openai", language: "en", gender: "neutral", preview_url: null, description: "OpenAI nova voice" },
];

export const mockTrends = {
  period_days: 30,
  daily_generations: Array.from({ length: 30 }, (_, i) => ({
    date: new Date(Date.now() - (29 - i) * 86400000).toISOString().split("T")[0],
    count: Math.floor(Math.random() * 4) + 1,
  })),
  daily_views: Array.from({ length: 30 }, (_, i) => ({
    date: new Date(Date.now() - (29 - i) * 86400000).toISOString().split("T")[0],
    views: Math.floor(Math.random() * 5000) + 500,
  })),
  top_topics: ["AI Tools", "Python", "Productivity", "Tech Career", "Side Hustles"],
  platform_breakdown: { youtube: 45, instagram: 35, tiktok: 20 },
};

export const mockMediaResults = [
  { id: "pexels-001", provider: "pexels", type: "video", url: "https://www.pexels.com/video/5926382/", preview_url: "https://images.pexels.com/photos/5926382/pexels-photo-5926382.jpeg?auto=compress&w=400", thumbnail_url: "https://images.pexels.com/photos/5926382/pexels-photo-5926382.jpeg?auto=compress&w=200", duration: 8.0, width: 1080, height: 1920, tags: ["technology", "laptop"] },
  { id: "pexels-002", provider: "pexels", type: "video", url: "https://www.pexels.com/video/5377684/", preview_url: "https://images.pexels.com/photos/5377684/pexels-photo-5377684.jpeg?auto=compress&w=400", thumbnail_url: "https://images.pexels.com/photos/5377684/pexels-photo-5377684.jpeg?auto=compress&w=200", duration: 12.0, width: 1080, height: 1920, tags: ["abstract", "data"] },
  { id: "pexels-003", provider: "pexels", type: "video", url: "https://www.pexels.com/video/5496463/", preview_url: "https://images.pexels.com/photos/5496463/pexels-photo-5496463.jpeg?auto=compress&w=400", thumbnail_url: "https://images.pexels.com/photos/5496463/pexels-photo-5496463.jpeg?auto=compress&w=200", duration: 6.0, width: 1080, height: 1920, tags: ["typing", "work"] },
];
