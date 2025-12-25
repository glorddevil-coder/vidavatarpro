-- AuraStudio AI Database Schema
-- Supabase/PostgreSQL

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- User Profiles Table
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    password_hash VARCHAR(255),
    subscription_tier VARCHAR(50) DEFAULT 'free' CHECK (subscription_tier IN ('free', 'pro', 'enterprise')),
    credits_remaining INTEGER DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_user_profiles_email ON user_profiles(email);

-- Projects Table (Project Master)
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    script_text TEXT NOT NULL,
    actor_id UUID NOT NULL,
    status VARCHAR(50) DEFAULT 'draft' CHECK (status IN ('draft', 'processing', 'completed', 'failed')),
    duration_seconds INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_synced TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_status ON projects(status);

-- Asset Vault Table
CREATE TABLE asset_vault (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL CHECK (type IN ('image', 'voice', 'audio')),
    name VARCHAR(255) NOT NULL,
    s3_url TEXT NOT NULL,
    is_custom_avatar BOOLEAN DEFAULT FALSE,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_asset_vault_user_id ON asset_vault(user_id);
CREATE INDEX idx_asset_vault_type ON asset_vault(type);

-- Actor DNA Table (AI Parameters)
CREATE TABLE actor_dna (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) DEFAULT 'stock' CHECK (type IN ('stock', 'custom')),
    user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    base_voice VARCHAR(255) NOT NULL,
    default_mood VARCHAR(100),
    mesh_path TEXT,
    blend_shapes JSONB,
    thumbnail_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_actor_dna_user_id ON actor_dna(user_id);
CREATE INDEX idx_actor_dna_type ON actor_dna(type);

-- Effect Library Table (Voice Presets)
CREATE TABLE effect_library (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) DEFAULT 'custom' CHECK (type IN ('trickster', 'deepbass', 'custom')),
    pitch_multiplier FLOAT DEFAULT 1.0,
    formant_shift FLOAT DEFAULT 1.0,
    tempo_rate FLOAT DEFAULT 1.0,
    description TEXT,
    user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_effect_library_user_id ON effect_library(user_id);
CREATE INDEX idx_effect_library_type ON effect_library(type);

-- Export Jobs Table
CREATE TABLE export_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
    format VARCHAR(50) NOT NULL CHECK (format IN ('mp4', 'mov', 'fbx')),
    resolution VARCHAR(50) DEFAULT '1080p' CHECK (resolution IN ('1080p', '2k', '4k')),
    status VARCHAR(50) DEFAULT 'queued' CHECK (status IN ('queued', 'processing', 'completed', 'failed')),
    output_url TEXT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_export_jobs_project_id ON export_jobs(project_id);
CREATE INDEX idx_export_jobs_user_id ON export_jobs(user_id);
CREATE INDEX idx_export_jobs_status ON export_jobs(status);

-- Script Analysis Table
CREATE TABLE script_analysis (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    emotion_tags JSONB,
    lip_sync_points JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_script_analysis_project_id ON script_analysis(project_id);

-- User Memory Table (Diary Keeper / Long-Term Memory)
CREATE TABLE user_memory (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
    summary TEXT NOT NULL,
    full_text TEXT,
    emotion_detected VARCHAR(50),
    emotion_confidence FLOAT DEFAULT 0.0,
    memory_type VARCHAR(50) DEFAULT 'note' CHECK (memory_type IN ('note', 'reminder', 'birthday', 'event', 'preference')),
    memory_vector VECTOR(1536),
    is_archived BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    recalled_count INTEGER DEFAULT 0,
    last_recalled TIMESTAMP NULL
);

CREATE INDEX idx_user_memory_user_id ON user_memory(user_id);
CREATE INDEX idx_user_memory_type ON user_memory(memory_type);
CREATE INDEX idx_user_memory_emotion ON user_memory(emotion_detected);

-- Persona Sync Table (Friendship Bonding)
CREATE TABLE persona_sync (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE REFERENCES user_profiles(id) ON DELETE CASCADE,
    relationship_level INTEGER DEFAULT 1 CHECK (relationship_level >= 1 AND relationship_level <= 10),
    preferred_tone VARCHAR(100) DEFAULT 'friendly' CHECK (preferred_tone IN ('professional', 'friendly', 'humorous', 'supportive', 'energetic')),
    interaction_count INTEGER DEFAULT 0,
    total_conversation_minutes INTEGER DEFAULT 0,
    avatar_personality_traits JSONB,
    user_preferences JSONB,
    last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_persona_sync_user_id ON persona_sync(user_id);
CREATE INDEX idx_persona_sync_relationship ON persona_sync(relationship_level);

-- Conversation History Table (For Dialog Memory)
CREATE TABLE conversation_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
    user_message TEXT NOT NULL,
    avatar_response TEXT NOT NULL,
    mode VARCHAR(50) NOT NULL CHECK (mode IN ('studio', 'companion', 'assistant')),
    language_detected VARCHAR(10),
    sentiment_score FLOAT,
    context_vectors VECTOR(1536),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_conversation_history_user_id ON conversation_history(user_id);
CREATE INDEX idx_conversation_history_mode ON conversation_history(mode);
CREATE INDEX idx_conversation_history_created ON conversation_history(created_at);

-- Translation Cache Table (For Performance)
CREATE TABLE translation_cache (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_text TEXT NOT NULL,
    source_language VARCHAR(10) NOT NULL,
    target_language VARCHAR(10) NOT NULL,
    translated_text TEXT NOT NULL,
    confidence_score FLOAT,
    translation_time_ms INTEGER,
    cache_hits INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_translation_cache_unique ON translation_cache(source_text, source_language, target_language);
CREATE INDEX idx_translation_cache_languages ON translation_cache(source_language, target_language);

-- Enable Realtime for specific tables (Supabase-specific)
-- This allows real-time sync across devices
ALTER PUBLICATION supabase_realtime ADD TABLE projects;
ALTER PUBLICATION supabase_realtime ADD TABLE export_jobs;
ALTER PUBLICATION supabase_realtime ADD TABLE user_memory;
ALTER PUBLICATION supabase_realtime ADD TABLE persona_sync;
ALTER PUBLICATION supabase_realtime ADD TABLE conversation_history;
