-- ==============================================
-- Automated Video Shorts Generation System
-- PostgreSQL Database Schema (Supabase-compatible)
-- ==============================================

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ==============================================
-- USERS TABLE
-- ==============================================
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    avatar_url TEXT,
    plan VARCHAR(50) DEFAULT 'free', -- free, pro, enterprise
    credits_remaining INTEGER DEFAULT 10,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==============================================
-- SCRIPTS TABLE
-- ==============================================
CREATE TABLE scripts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    topic VARCHAR(500) NOT NULL,
    title VARCHAR(255),
    tone VARCHAR(50) DEFAULT 'informative',
    style VARCHAR(50) DEFAULT 'viral',
    language VARCHAR(10) DEFAULT 'en',
    duration_target INTEGER DEFAULT 60,
    full_text TEXT,
    sections JSONB DEFAULT '[]'::jsonb,
    hashtags TEXT[] DEFAULT '{}',
    metadata JSONB DEFAULT '{}'::jsonb,
    word_count INTEGER DEFAULT 0,
    estimated_duration FLOAT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_scripts_user_id ON scripts(user_id);
CREATE INDEX idx_scripts_topic ON scripts USING gin(topic gin_trgm_ops);

-- ==============================================
-- VOICE GENERATIONS TABLE
-- ==============================================
CREATE TABLE voice_generations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    script_id UUID REFERENCES scripts(id) ON DELETE SET NULL,
    voice_id VARCHAR(100) NOT NULL,
    provider VARCHAR(50) DEFAULT 'elevenlabs',
    audio_url TEXT,
    audio_duration FLOAT,
    word_timestamps JSONB DEFAULT '[]'::jsonb,
    speed FLOAT DEFAULT 1.0,
    language VARCHAR(10) DEFAULT 'en',
    file_size_bytes BIGINT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_voice_user_id ON voice_generations(user_id);

-- ==============================================
-- MEDIA ASSETS TABLE
-- ==============================================
CREATE TABLE media_assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(20) NOT NULL, -- video, image, music
    provider VARCHAR(50), -- pexels, pixabay, upload
    source_url TEXT,
    stored_url TEXT,
    thumbnail_url TEXT,
    filename VARCHAR(255),
    mime_type VARCHAR(100),
    file_size_bytes BIGINT DEFAULT 0,
    duration FLOAT, -- for video/audio
    width INTEGER,
    height INTEGER,
    tags TEXT[] DEFAULT '{}',
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_media_user_id ON media_assets(user_id);
CREATE INDEX idx_media_type ON media_assets(type);
CREATE INDEX idx_media_tags ON media_assets USING gin(tags);

-- ==============================================
-- VIDEOS TABLE (Generated Videos)
-- ==============================================
CREATE TABLE videos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    script_id UUID REFERENCES scripts(id) ON DELETE SET NULL,
    voice_id UUID REFERENCES voice_generations(id) ON DELETE SET NULL,
    
    -- Video metadata
    title VARCHAR(255),
    description TEXT,
    topic VARCHAR(500),
    
    -- Status tracking
    status VARCHAR(50) DEFAULT 'pending',
    -- pending, generating_script, generating_voice, collecting_media,
    -- generating_subtitles, rendering, completed, failed, uploading, published
    progress FLOAT DEFAULT 0,
    error_message TEXT,
    
    -- Output
    video_url TEXT,
    thumbnail_url TEXT,
    subtitle_url TEXT,
    duration FLOAT,
    file_size_bytes BIGINT,
    resolution VARCHAR(20) DEFAULT '1080x1920',
    fps INTEGER DEFAULT 30,
    
    -- Configuration
    config JSONB DEFAULT '{}'::jsonb,
    -- Stores: tone, style, voice_id, subtitle_style, background_music, etc.
    
    -- Timing
    generation_started_at TIMESTAMP WITH TIME ZONE,
    generation_completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_videos_user_id ON videos(user_id);
CREATE INDEX idx_videos_status ON videos(status);
CREATE INDEX idx_videos_created_at ON videos(created_at DESC);

-- ==============================================
-- VIDEO MEDIA JUNCTION (clips used in a video)
-- ==============================================
CREATE TABLE video_media (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
    media_id UUID REFERENCES media_assets(id) ON DELETE SET NULL,
    sequence_order INTEGER DEFAULT 0,
    start_time FLOAT DEFAULT 0,
    end_time FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_video_media_video_id ON video_media(video_id);

-- ==============================================
-- SOCIAL UPLOADS TABLE
-- ==============================================
CREATE TABLE social_uploads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL, -- youtube, instagram, tiktok
    
    -- Upload details
    platform_video_id VARCHAR(255),
    platform_url TEXT,
    title VARCHAR(255),
    description TEXT,
    tags TEXT[] DEFAULT '{}',
    visibility VARCHAR(50) DEFAULT 'public',
    
    -- Status
    status VARCHAR(50) DEFAULT 'pending',
    -- pending, uploading, published, failed, scheduled
    scheduled_at TIMESTAMP WITH TIME ZONE,
    published_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    
    -- Performance metrics (synced periodically)
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_uploads_user_id ON social_uploads(user_id);
CREATE INDEX idx_uploads_video_id ON social_uploads(video_id);
CREATE INDEX idx_uploads_platform ON social_uploads(platform);
CREATE INDEX idx_uploads_status ON social_uploads(status);

-- ==============================================
-- GENERATION LOGS TABLE
-- ==============================================
CREATE TABLE generation_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    video_id UUID REFERENCES videos(id) ON DELETE SET NULL,
    
    step VARCHAR(100) NOT NULL,
    -- script_generation, voice_generation, media_collection,
    -- subtitle_generation, video_rendering, social_upload
    
    status VARCHAR(50) NOT NULL, -- started, completed, failed
    duration_ms INTEGER,
    error_message TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_logs_video_id ON generation_logs(video_id);
CREATE INDEX idx_logs_created_at ON generation_logs(created_at DESC);

-- ==============================================
-- API KEYS TABLE (for user-provided keys)
-- ==============================================
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    service VARCHAR(50) NOT NULL,
    -- openai, anthropic, elevenlabs, pexels, youtube, instagram, tiktok
    encrypted_key TEXT NOT NULL,
    is_valid BOOLEAN DEFAULT true,
    last_validated_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id, service)
);

CREATE INDEX idx_api_keys_user_id ON api_keys(user_id);

-- ==============================================
-- AUTOMATION SCHEDULES TABLE
-- ==============================================
CREATE TABLE automation_schedules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    
    -- Schedule config
    cron_expression VARCHAR(100), -- e.g., "0 9 * * 1-5" (weekdays at 9am)
    timezone VARCHAR(50) DEFAULT 'UTC',
    
    -- Generation config
    topics TEXT[] DEFAULT '{}', -- Pool of topics to rotate through
    tone VARCHAR(50) DEFAULT 'informative',
    voice_id VARCHAR(100),
    auto_upload BOOLEAN DEFAULT true,
    upload_platforms TEXT[] DEFAULT '{}',
    
    -- Stats
    total_runs INTEGER DEFAULT 0,
    successful_runs INTEGER DEFAULT 0,
    last_run_at TIMESTAMP WITH TIME ZONE,
    next_run_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_schedules_user_id ON automation_schedules(user_id);
CREATE INDEX idx_schedules_active ON automation_schedules(is_active);

-- ==============================================
-- ROW LEVEL SECURITY POLICIES (Supabase)
-- ==============================================
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE scripts ENABLE ROW LEVEL SECURITY;
ALTER TABLE voice_generations ENABLE ROW LEVEL SECURITY;
ALTER TABLE media_assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE videos ENABLE ROW LEVEL SECURITY;
ALTER TABLE social_uploads ENABLE ROW LEVEL SECURITY;
ALTER TABLE generation_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;
ALTER TABLE automation_schedules ENABLE ROW LEVEL SECURITY;

-- Users can only access their own data
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can view own scripts" ON scripts
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can view own voices" ON voice_generations
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can view own media" ON media_assets
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can view own videos" ON videos
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can view own uploads" ON social_uploads
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can view own logs" ON generation_logs
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can view own keys" ON api_keys
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can view own schedules" ON automation_schedules
    FOR ALL USING (auth.uid() = user_id);

-- ==============================================
-- FUNCTIONS & TRIGGERS
-- ==============================================

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER tr_scripts_updated_at
    BEFORE UPDATE ON scripts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER tr_videos_updated_at
    BEFORE UPDATE ON videos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER tr_uploads_updated_at
    BEFORE UPDATE ON social_uploads
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER tr_api_keys_updated_at
    BEFORE UPDATE ON api_keys
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER tr_schedules_updated_at
    BEFORE UPDATE ON automation_schedules
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
