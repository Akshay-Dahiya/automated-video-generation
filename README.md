# 🎬 VideoGen AI - Automated Video Shorts Generation System

<div align="center">

![VideoGen AI](https://img.shields.io/badge/VideoGen-AI%20Powered-blueviolet?style=for-the-badge&logo=openai)
![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A full-stack AI-powered automation platform that creates and publishes short-form videos (YouTube Shorts, Instagram Reels, TikTok) with minimal human intervention.**

[Features](#-features) · [Architecture](#-architecture) · [Quick Start](#-quick-start) · [API Docs](#-api-documentation) · [Deployment](#-deployment) · [Roadmap](#-roadmap)

</div>

---

## 🌟 Features

### Core Pipeline
| Feature | Description | Technology |
|---------|-------------|------------|
| 🤖 **AI Script Generation** | Generates viral scripts with Hook → Body → CTA structure | OpenAI GPT-4 / Claude |
| 🎙️ **Voice Generation** | Converts scripts to realistic voiceovers | ElevenLabs / OpenAI TTS |
| 🎥 **Media Collection** | Auto-fetches contextual stock footage | Pexels / Pixabay APIs |
| 📝 **Animated Subtitles** | Word-by-word karaoke-style captions | Whisper + ASS format |
| 🎬 **Video Rendering** | Composites everything into 9:16 vertical video | FFmpeg pipeline |
| 📤 **Social Upload** | Auto-publishes to YouTube, Instagram, TikTok | Platform APIs |
| ⚡ **Workflow Automation** | Scheduled & trigger-based generation | n8n + Celery |
| 📊 **Analytics Dashboard** | Track views, engagement, generation stats | Real-time metrics |

### Platform Highlights
- **Modern AI Dashboard** - Dark futuristic UI with glassmorphism design
- **Multi-step Video Wizard** - Guided video creation experience
- **Batch Generation** - Generate multiple videos from topic lists
- **Scheduled Automation** - Cron-based daily content generation
- **Real-time Progress** - Track pipeline status live
- **Asset Library** - Manage scripts, voices, media, and music
- **Multi-platform Publishing** - One-click publish to all platforms

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Next.js 14)                      │
│           Tailwind CSS · Framer Motion · Zustand             │
└──────────────────────────┬──────────────────────────────────┘
                           │ REST API
┌──────────────────────────▼──────────────────────────────────┐
│                   BACKEND (FastAPI)                           │
│        Script · Voice · Media · Subtitle · Render            │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────┬───────────┼───────────┬──────────────────────┐
│  PostgreSQL  │   Redis   │  FFmpeg   │    n8n Workflows      │
│  (Supabase)  │  (Queue)  │ (Render)  │   (Orchestration)    │
└──────────────┴───────────┴───────────┴──────────────────────┘
```

> Full architecture diagram: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

---

## 📁 Project Structure

```
automated-video-generation/
├── frontend/                    # Next.js 14 Dashboard
│   ├── src/
│   │   ├── app/                 # App router pages
│   │   │   ├── page.tsx         # Dashboard
│   │   │   ├── generate/        # Video generation wizard
│   │   │   ├── videos/          # Video library
│   │   │   ├── analytics/       # Performance analytics
│   │   │   ├── upload/          # Social publishing
│   │   │   ├── library/         # Asset management
│   │   │   └── settings/        # Configuration
│   │   ├── components/          # Reusable UI components
│   │   │   ├── layout/          # Sidebar, TopBar
│   │   │   └── dashboard/       # Stats, Charts, Tables
│   │   └── lib/                 # API client, store, utils
│   ├── tailwind.config.ts       # Custom theme
│   ├── Dockerfile
│   └── package.json
├── backend/                     # FastAPI Backend
│   ├── app/
│   │   ├── main.py              # Application entry
│   │   ├── worker.py            # Celery background tasks
│   │   ├── core/                # Config, database
│   │   ├── api/routes/          # REST API endpoints
│   │   │   ├── scripts.py       # Script generation
│   │   │   ├── videos.py        # Video pipeline
│   │   │   ├── voices.py        # TTS generation
│   │   │   ├── media.py         # Media collection
│   │   │   ├── uploads.py       # Social publishing
│   │   │   └── analytics.py     # Metrics & logs
│   │   └── services/            # Business logic
│   │       ├── script_generator.py
│   │       ├── voice_generator.py
│   │       ├── media_collector.py
│   │       ├── subtitle_engine.py
│   │       ├── video_renderer.py
│   │       ├── video_pipeline.py
│   │       ├── social_uploader.py
│   │       └── analytics_service.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── database/
│   └── schema.sql               # PostgreSQL schema (Supabase)
├── n8n/
│   └── workflows/               # Automation workflows
│       ├── video-generation-pipeline.json
│       ├── scheduled-generation.json
│       └── batch-generation.json
├── docs/
│   ├── ARCHITECTURE.md          # System design
│   ├── FFMPEG_PIPELINE.md       # Rendering pipeline
│   └── DEPLOYMENT.md            # Deploy guide
├── docker-compose.yml           # Full stack orchestration
└── README.md                    # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 20+ (for local frontend dev)
- Python 3.11+ (for local backend dev)
- FFmpeg installed

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/Akshay-Dahiya/automated-video-generation.git
cd automated-video-generation

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# Add your API keys to backend/.env
# (OpenAI, ElevenLabs, Pexels required minimum)

# Start all services
docker-compose up -d

# Access:
# Frontend:  http://localhost:3000
# Backend:   http://localhost:8000
# API Docs:  http://localhost:8000/api/docs
# n8n:       http://localhost:5678
```

### Option 2: Local Development

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

### Minimum API Keys Required

| Service | Purpose | Get Key |
|---------|---------|---------|
| OpenAI | Script generation + Whisper | [platform.openai.com](https://platform.openai.com) |
| ElevenLabs | Voice generation | [elevenlabs.io](https://elevenlabs.io) |
| Pexels | Stock footage | [pexels.com/api](https://www.pexels.com/api/) |

---

## 📡 API Documentation

### Base URL: `http://localhost:8000/api/v1`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/scripts/generate` | POST | Generate AI script from topic |
| `/scripts/{id}` | GET | Get script by ID |
| `/videos/generate` | POST | Trigger full video pipeline |
| `/videos/{id}` | GET | Get video status & details |
| `/videos/` | GET | List all videos |
| `/voices/generate` | POST | Generate voiceover |
| `/voices/styles` | GET | List available voices |
| `/media/search` | POST | Search stock media |
| `/media/auto-collect` | POST | AI-powered media selection |
| `/uploads/publish` | POST | Publish to social platforms |
| `/analytics/dashboard` | GET | Dashboard statistics |

> Interactive API docs: `http://localhost:8000/api/docs` (Swagger UI)

### Example: Generate a Video

```bash
curl -X POST http://localhost:8000/api/v1/videos/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "5 AI tools that will change your life in 2024",
    "tone": "informative",
    "duration_seconds": 60,
    "auto_upload": false
  }'
```

---

## 🗄️ Database Schema

10 tables with full relational design:

- `users` - User accounts & plans
- `scripts` - Generated scripts with sections
- `voice_generations` - TTS audio files & timestamps
- `media_assets` - Stock footage & images
- `videos` - Generated videos with full status tracking
- `video_media` - Video-to-media junction table
- `social_uploads` - Platform upload records & metrics
- `generation_logs` - Pipeline execution logs
- `api_keys` - User API key storage (encrypted)
- `automation_schedules` - Cron-based generation schedules

> Full schema: [`database/schema.sql`](database/schema.sql)

---

## 🚢 Deployment

### Vercel + Railway (Recommended)

| Service | Platform | Notes |
|---------|----------|-------|
| Frontend | Vercel | Auto-deploys from `frontend/` |
| Backend | Railway | Docker container |
| Database | Supabase | Managed PostgreSQL |
| Redis | Railway | Add-on service |
| n8n | Railway | Separate service |

### Deploy Steps

1. **Frontend (Vercel)**
   ```bash
   cd frontend && npx vercel
   ```

2. **Backend (Railway)**
   - Connect GitHub repo
   - Set root directory: `backend/`
   - Add environment variables from `.env.example`

3. **Database (Supabase)**
   - Create project at [supabase.com](https://supabase.com)
   - Run `database/schema.sql` in SQL editor
   - Copy URL + anon key to env vars

> Full deployment guide: [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md)

---

## 🗺️ Roadmap

### ✅ MVP (Current)
- [x] AI script generation (OpenAI)
- [x] Voice generation (ElevenLabs)
- [x] Stock media collection (Pexels)
- [x] Animated subtitle engine (Whisper + ASS)
- [x] FFmpeg video rendering pipeline
- [x] Full dashboard UI
- [x] Docker setup
- [x] n8n workflow automation

### 🔜 Version 2.0
- [ ] Real-time WebSocket progress updates
- [ ] AI image generation (Stable Diffusion)
- [ ] Custom voice cloning
- [ ] A/B testing for thumbnails
- [ ] Batch scheduling UI
- [ ] Multi-language support
- [ ] Team collaboration features
- [ ] Usage billing & credits system

### 🔮 Version 3.0 (Enterprise)
- [ ] White-label SaaS platform
- [ ] Custom AI model fine-tuning
- [ ] Advanced analytics with ML insights
- [ ] Content approval workflows
- [ ] Enterprise SSO integration
- [ ] Horizontal scaling with Kubernetes
- [ ] CDN-optimized global delivery

---

## 🛠️ Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend | Next.js | 14.1 |
| Styling | Tailwind CSS | 3.4 |
| Animation | Framer Motion | 11.0 |
| State | Zustand | 4.5 |
| Backend | FastAPI | 0.109 |
| Language | Python | 3.11 |
| Database | PostgreSQL (Supabase) | 16 |
| Queue | Redis + Celery | 7 / 5.3 |
| Video | FFmpeg | 6.0 |
| AI | OpenAI GPT-4 | Latest |
| TTS | ElevenLabs | v2 |
| STT | Whisper | v3 |
| Automation | n8n | Latest |
| Container | Docker | 24 |
| Deploy | Vercel + Railway | - |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Akshay Dahiya**

- GitHub: [@Akshay-Dahiya](https://github.com/Akshay-Dahiya)

---

<div align="center">

**Built with AI, for creators who want to scale content production.**

⭐ Star this repo if you find it useful!

</div>
