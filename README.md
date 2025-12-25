# AuraStudio AI – Cross-Platform Virtual Actor SaaS

A sophisticated SaaS platform for creating high-fidelity AI virtual actor videos across Web, Desktop, and Mobile.

## Project Structure

```
auraStudio-ai/
├── web/                 # Next.js Web Application
├── api/                 # FastAPI Python Backend
├── db/                  # Database migrations and schemas
├── config/              # Configuration files
└── docs/                # Documentation
```

## Core Features

- **Actor & Avatar Engine**: 50+ stock avatars + custom avatar creation from photos
- **Trickster Audio Engine**: Advanced voice processing (pitch, formant, tempo adjustment)
- **Real-time Sync**: Supabase-powered state synchronization across devices
- **3D Viewport**: Three.js-based cinematic preview
- **Cloud GPU Rendering**: Modal.com or Replicate serverless rendering
- **Multi-format Export**: MP4, MOV with alpha, FBX motion data

## Tech Stack

### Frontend
- **Web**: Next.js 14+
- **Desktop**: Electron (wrapper around Next.js)
- **Mobile**: Flutter

### Backend
- **API Framework**: FastAPI (Python 3.10+)
- **Database**: Supabase (PostgreSQL)
- **Real-time**: Supabase RealtimeDB
- **Storage**: AWS S3 (cloud assets)
- **GPU Compute**: Modal.com or Replicate

### AI/ML
- **Text Analysis**: GPT-4o
- **Lip-Sync**: Sync Labs API / Wav2Lip
- **TTS**: ElevenLabs
- **Avatar Mesh**: MediaPipe + custom reconstruction

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+
- pnpm (Node package manager)
- Supabase account

### Installation

1. **Clone and setup root**
   ```bash
   cd auraStudio-ai
   pnpm install  # Install all workspace dependencies
   ```

2. **Web app setup**
   ```bash
   cd web
   pnpm install
   pnpm dev  # Start dev server on http://localhost:3000
   ```

3. **API setup**
   ```bash
   cd api
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python -m uvicorn main:app --reload
   ```

## Environment Variables

Create `.env.local` in project root:

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_key

# API Services
ELEVENLABS_API_KEY=your_elevenlabs_key
OPENAI_API_KEY=your_openai_key
SYNC_LABS_API_KEY=your_sync_labs_key
MODAL_API_KEY=your_modal_key

# AWS S3
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_S3_BUCKET=your_bucket_name
AWS_REGION=us-east-1
```

## API Endpoints

- `POST /api/audio/trickster` – Apply Trickster effect to audio
- `POST /api/projects` – Create new project
- `GET /api/projects/{id}` – Fetch project
- `POST /api/avatars/custom` – Upload custom avatar
- `GET /api/avatars/stock` – List stock avatars
- `POST /api/export` – Trigger cloud rendering job

## Database Schema

See [db/schema.sql](db/schema.sql) for full schema definition.

**Key Tables:**
- `user_profiles` – Auth & billing
- `projects` – Script & setup
- `asset_vault` – Custom uploads
- `actor_dna` – AI parameters
- `effect_library` – Voice presets

## License

Proprietary – AuraStudio Inc.
