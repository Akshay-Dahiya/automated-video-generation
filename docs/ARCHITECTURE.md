# System Architecture - Automated Video Shorts Generation

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Next.js)                            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │Dashboard │ │Generator │ │ Library  │ │ Upload   │ │Analytics │ │
│  │  Page    │ │  Page    │ │  Page    │ │  Page    │ │  Page    │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
└────────────────────────────────┬────────────────────────────────────┘
                                 │ REST API / WebSocket
┌────────────────────────────────▼────────────────────────────────────┐
│                     API GATEWAY (FastAPI)                            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │  Auth    │ │  Video   │ │  Script  │ │  Upload  │ │Analytics │ │
│  │ Routes   │ │ Routes   │ │ Routes   │ │ Routes   │ │ Routes   │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────────┐
│                      SERVICE LAYER                                   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐  │
│  │   Script    │ │    Voice    │ │   Media     │ │  Subtitle   │  │
│  │  Generator  │ │  Generator  │ │  Collector  │ │   Engine    │  │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐  │
│  │   Video     │ │   Social    │ │   Queue     │ │  Analytics  │  │
│  │  Renderer   │ │  Uploader   │ │   Manager   │ │   Service   │  │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘  │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │Supabase  │ │Cloudinary│ │  Redis   │ │  FFmpeg  │ │   n8n    │ │
│  │(Postgres)│ │ (Media)  │ │ (Queue)  │ │(Render)  │ │(Workflow)│ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
└─────────────────────────────────────────────────────────────────────┘

## External AI Services
┌─────────────────────────────────────────────────────────────────────┐
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ OpenAI / │ │ElevenLabs│ │  Pexels  │ │ Whisper  │ │ YouTube  │ │
│  │  Claude  │ │  / XTTS  │ │  / Pixab │ │  (STT)   │ │ /Insta   │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

## Module Breakdown

### 1. Script Generation Module
- **Input**: Topic, tone, duration, style
- **Process**: AI generates hook → body → CTA script
- **Output**: Structured script with timing markers
- **AI Provider**: OpenAI GPT-4 / Claude API

### 2. Voice Generation Module
- **Input**: Script text, voice style selection
- **Process**: TTS synthesis with prosody control
- **Output**: Audio file (.mp3/.wav) with word timestamps
- **Provider**: ElevenLabs API / XTTS (local)

### 3. Media Collection Module
- **Input**: Script keywords, scene descriptions
- **Process**: Search and download relevant stock media
- **Output**: Collection of video clips/images
- **Provider**: Pexels / Pixabay / Unsplash APIs

### 4. Subtitle Engine
- **Input**: Audio file or script text
- **Process**: Generate word-level timestamps, style captions
- **Output**: ASS/SRT subtitle file with animations
- **Provider**: OpenAI Whisper (local or API)

### 5. Video Rendering Pipeline
- **Input**: Media clips, audio, subtitles, config
- **Process**: FFmpeg compositing pipeline
- **Output**: Final 9:16 vertical video (1080x1920)
- **Engine**: FFmpeg with custom filter chains

### 6. Social Upload Module
- **Input**: Rendered video, metadata, schedule
- **Process**: OAuth-authenticated upload to platforms
- **Output**: Published video with tracking URLs
- **Platforms**: YouTube, Instagram, TikTok

### 7. Automation Orchestration
- **Input**: Trigger events (schedule, webhook, manual)
- **Process**: Full pipeline execution with error handling
- **Output**: Completed video generation job
- **Engine**: n8n workflows + Redis queue

## Data Flow

```
User Input (Topic)
    │
    ▼
[Script Generation] ──→ Script JSON
    │
    ▼
[Voice Generation] ──→ Audio File + Timestamps
    │
    ▼
[Media Collection] ──→ Video Clips / Images
    │
    ▼
[Subtitle Engine] ──→ Animated Captions (ASS)
    │
    ▼
[Video Renderer] ──→ Final MP4 (9:16, 1080x1920)
    │
    ▼
[Social Uploader] ──→ Published to Platforms
    │
    ▼
[Analytics] ──→ Track Performance
```

## Technology Decisions

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Frontend | Next.js 14 + Tailwind | SSR, fast, modern |
| Backend | FastAPI (Python) | Async, fast, ML-friendly |
| Database | Supabase (PostgreSQL) | Real-time, auth built-in |
| Queue | Redis + Celery | Reliable job processing |
| Media CDN | Cloudinary | Transform + deliver |
| Video | FFmpeg | Industry standard |
| Orchestration | n8n | Visual, extensible |
| Container | Docker | Portable, reproducible |
| Deploy | Vercel + Railway | Modern cloud deploy |
