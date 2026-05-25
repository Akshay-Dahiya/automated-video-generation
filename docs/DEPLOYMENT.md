# Deployment Guide

## Table of Contents
- [Quick Deploy (Docker)](#quick-deploy-docker)
- [Production Deploy (Cloud)](#production-deploy-cloud)
- [Vercel (Frontend)](#vercel-frontend)
- [Railway (Backend)](#railway-backend)
- [Supabase (Database)](#supabase-database)
- [Environment Variables](#environment-variables)
- [SSL & Domain Setup](#ssl--domain-setup)
- [Monitoring](#monitoring)

---

## Quick Deploy (Docker)

### Single Server (VPS)

```bash
# SSH into your server
ssh user@your-server.com

# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Clone and deploy
git clone https://github.com/Akshay-Dahiya/automated-video-generation.git
cd automated-video-generation

# Configure
cp backend/.env.example backend/.env
nano backend/.env  # Add your API keys

# Deploy
docker-compose -f docker-compose.yml up -d

# Verify
docker-compose ps
curl http://localhost:8000/health
```

### Recommended VPS Specs
| Tier | vCPUs | RAM | Storage | Use Case |
|------|-------|-----|---------|----------|
| Minimum | 2 | 4GB | 50GB | Testing/Demo |
| Recommended | 4 | 8GB | 100GB | Production (10 videos/day) |
| Performance | 8 | 16GB | 200GB | Production (50+ videos/day) |

---

## Production Deploy (Cloud)

### Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Vercel    │────▶│   Railway   │────▶│  Supabase   │
│  (Frontend) │     │  (Backend)  │     │ (Database)  │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           │
                    ┌──────┼──────┐
                    │      │      │
               ┌────▼──┐ ┌▼────┐ ┌▼─────┐
               │ Redis │ │ n8n │ │Celery │
               └───────┘ └─────┘ └──────┘
```

---

## Vercel (Frontend)

### Step 1: Connect Repository

1. Go to [vercel.com](https://vercel.com) → New Project
2. Import your GitHub repository
3. Set **Root Directory** to `frontend`
4. Framework: Next.js (auto-detected)

### Step 2: Environment Variables

```
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

### Step 3: Deploy

```bash
cd frontend
npx vercel --prod
```

### Custom Domain
- Add domain in Vercel Dashboard → Settings → Domains
- Configure DNS: CNAME to `cname.vercel-dns.com`

---

## Railway (Backend)

### Step 1: Create Project

1. Go to [railway.app](https://railway.app) → New Project
2. Deploy from GitHub repo
3. Set **Root Directory** to `backend`
4. Railway auto-detects the Dockerfile

### Step 2: Add Services

Add these services to your Railway project:
- **Redis** (Railway add-on) - for task queue
- **Worker** (same repo, different start command)
  - Start command: `celery -A app.worker worker --loglevel=info`

### Step 3: Environment Variables

Add all variables from `backend/.env.example` to Railway.

### Step 4: Custom Domain
- Railway Dashboard → Settings → Networking → Custom Domain

---

## Supabase (Database)

### Step 1: Create Project

1. Go to [supabase.com](https://supabase.com) → New Project
2. Choose region closest to your users
3. Set a strong database password

### Step 2: Run Schema

1. Go to SQL Editor in Supabase Dashboard
2. Paste contents of `database/schema.sql`
3. Execute

### Step 3: Get Connection Details

- **URL**: Settings → API → Project URL
- **Anon Key**: Settings → API → anon public key
- **Database URL**: Settings → Database → Connection string

---

## Environment Variables

### Backend (All Required)

```env
# Core
DEBUG=false
SECRET_KEY=<generate-random-64-char-string>

# Database
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...
DATABASE_URL=postgresql+asyncpg://postgres:password@db.xxx.supabase.co:5432/postgres

# Redis (Railway provides this)
REDIS_URL=redis://default:password@host:port

# AI (Required)
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=...

# Media (Required)
PEXELS_API_KEY=...

# Cloudinary (Required for social upload)
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...

# Social (Optional)
YOUTUBE_CLIENT_ID=...
YOUTUBE_CLIENT_SECRET=...
INSTAGRAM_ACCESS_TOKEN=...
```

### Frontend

```env
NEXT_PUBLIC_API_URL=https://your-api.railway.app
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
```

---

## SSL & Domain Setup

### Vercel (Automatic)
- SSL is automatic for all Vercel deployments
- Custom domains get SSL within minutes

### Railway (Automatic)
- SSL is automatic for Railway domains
- Custom domains require DNS verification first

### Self-hosted (Let's Encrypt)
```bash
# Using Caddy (recommended reverse proxy)
sudo apt install caddy

# Caddyfile
cat > /etc/caddy/Caddyfile << EOF
your-domain.com {
    reverse_proxy localhost:3000
}

api.your-domain.com {
    reverse_proxy localhost:8000
}
EOF

sudo systemctl restart caddy
```

---

## Monitoring

### Health Checks

```bash
# Backend health
curl https://your-api.railway.app/health

# Expected response:
# {"status": "healthy", "service": "automated-video-generation", "version": "1.0.0"}
```

### Recommended Monitoring Stack

| Tool | Purpose | Free Tier |
|------|---------|-----------|
| UptimeRobot | Uptime monitoring | 50 monitors |
| Sentry | Error tracking | 5K events/mo |
| Vercel Analytics | Frontend performance | Built-in |
| Railway Metrics | Backend resources | Built-in |

### Log Access

```bash
# Railway logs
railway logs --service backend

# Docker logs
docker-compose logs -f backend
docker-compose logs -f celery-worker
```

---

## Scaling Considerations

### Horizontal Scaling

For high-volume production (100+ videos/day):

1. **Multiple Celery Workers**: Scale render workers independently
2. **Redis Cluster**: For queue reliability
3. **CDN**: Cloudinary/Cloudflare for media delivery
4. **Database Pooling**: PgBouncer for connection management
5. **GPU Workers**: Dedicated render servers with NVIDIA GPUs

### Cost Estimates (Monthly)

| Scale | Infra Cost | API Costs | Total |
|-------|-----------|-----------|-------|
| Hobby (5 videos/day) | $0-20 | $30-50 | ~$50-70 |
| Startup (20 videos/day) | $50-100 | $100-200 | ~$150-300 |
| Business (100 videos/day) | $200-500 | $500-1000 | ~$700-1500 |
