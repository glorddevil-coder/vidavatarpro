# AuraStudio AI - Architecture Documentation

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    AuraStudio AI Ecosystem                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │   Web App    │    │ Desktop App  │    │  Mobile App  │     │
│  │ (Next.js)    │    │ (Electron)   │    │ (Flutter)    │     │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘     │
│         │                   │                   │              │
│         └───────────────────┼───────────────────┘              │
│                             │                                  │
│                     ┌───────▼────────┐                        │
│                     │  Supabase RT   │                        │
│                     │  (Realtime)    │                        │
│                     └───────┬────────┘                        │
│                             │                                  │
│         ┌───────────────────┼───────────────────┐             │
│         │                   │                   │             │
│    ┌────▼─────┐    ┌────────▼────────┐   ┌────▼─────┐       │
│    │FastAPI   │    │  PostgreSQL DB  │   │  AWS S3  │       │
│    │ Backend  │    │ (Supabase)      │   │ (Assets) │       │
│    └────┬─────┘    └────────────────┘   └──────────┘       │
│         │                                                     │
│    ┌────▼─────────────────────┐                             │
│    │  AI Services             │                             │
│    │  • GPT-4o (script)       │                             │
│    │  • ElevenLabs (TTS)       │                             │
│    │  • Sync Labs (lip-sync)   │                             │
│    │  • Modal.com (GPU render) │                             │
│    └──────────────────────────┘                             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Frontend Layer (Web/Desktop/Mobile)

**Web App (Next.js 14+)**
- Project dashboard and management
- Script editor with emotion tagging
- Real-time preview with Three.js viewport
- Asset library browser
- Social media export handler

**Desktop App (Electron)**
- Wraps Next.js web app
- 4K/8K export capabilities
- Local caching layer
- Deep timeline editor
- Batch processing

**Mobile App (Flutter)**
- Quick script-to-video
- Voice recording (voice-to-performance)
- Mobile sharing (TikTok, Instagram, YouTube Shorts)
- Director's remote control

### 2. Backend API Layer (FastAPI)

**Core Endpoints:**
- `/api/projects` – CRUD operations
- `/api/audio/trickster` – Trickster effect processing
- `/api/avatars` – Avatar management
- `/api/export` – Cloud rendering jobs
- `/api/scripts/analyze` – Emotion tagging & lip-sync

**Key Services:**
- **Audio Processing** – Librosa-based pitch, formant, tempo shifts
- **Avatar Mesh** – MediaPipe 3D reconstruction
- **Batch Processing** – Queue management for exports

### 3. Database (Supabase PostgreSQL)

**Tables:**
- `user_profiles` – Auth & billing
- `projects` – Script, metadata, status
- `asset_vault` – User uploads (images, voices)
- `actor_dna` – Avatar parameters & blend shapes
- `effect_library` – Preset audio effects
- `export_jobs` – Rendering queue & status

**Real-time Sync:**
- Supabase ListenBroadcast on `projects` & `export_jobs`
- Enables instant cross-device sync

### 4. Cloud Services

**AI Models:**
- **Text Analysis**: GPT-4o for emotion extraction
- **TTS**: ElevenLabs for natural voice synthesis
- **Lip-Sync**: Sync Labs API or Wav2Lip for mouth animation
- **GPU Rendering**: Modal.com (A100/H100) for final export

**Storage:**
- **AWS S3**: Stock avatars, SFX library, user assets
- **CDN**: CloudFront for fast asset delivery

## Data Flow Example: Script to Video

```
1. User uploads script (Web)
   ↓
2. Script → GPT-4o → Emotion tags (API)
   ↓
3. Emotion tags + Script → Avatar (lookup actor_dna)
   ↓
4. Generate voice (ElevenLabs TTS)
   ↓
5. Voice + Emotion → Lip-sync points (Sync Labs)
   ↓
6. Avatar + Motion + Audio → Final render (Modal GPU)
   ↓
7. Upload MP4 to S3, update project status
   ↓
8. Real-time notification to user (Supabase)
```

## Authentication & Authorization

- **Auth**: Supabase Auth (OAuth + email/password)
- **JWT Tokens**: Verified per API request
- **Row-Level Security**: Supabase RLS on user data
- **Rate Limiting**: 100 requests/min per user

## Scalability Considerations

1. **API**: Horizontal scaling with load balancer
2. **Database**: Supabase handles auto-scaling
3. **Rendering**: Modal.com serverless GPU autoscaling
4. **Storage**: S3 buckets with lifecycle policies
5. **Cache**: Redis for frequently accessed avatars/effects

## Deployment

**Production Stack:**
- Web: Vercel (Next.js)
- API: AWS ECS or Railway (FastAPI containers)
- Database: Supabase managed PostgreSQL
- CDN: Cloudflare or CloudFront
- GPU: Modal.com serverless

**CI/CD:**
- GitHub Actions for automated tests & deploys
- Staging environment for testing
- Zero-downtime deployments
