# AuraStudio AI - Setup & Quick Start Guide

## Prerequisites

- **Node.js 18+** – Download from nodejs.org
- **Python 3.10+** – Download from python.org
- **Git** – For version control
- **Supabase Account** – Free tier at supabase.com
- **AWS Account** (optional) – For S3 storage

## Project Structure

```
auraStudio-ai/
├── web/                    # Next.js Web Application
│   ├── src/
│   │   ├── app/           # App Router pages
│   │   ├── components/    # React components
│   │   ├── lib/           # Utilities & API clients
│   │   ├── hooks/         # Custom React hooks
│   │   └── types/         # TypeScript types
│   ├── public/
│   │   └── assets/        # Stock avatars & SFX
│   └── package.json
│
├── api/                    # FastAPI Backend
│   ├── app/
│   │   ├── routes/        # API endpoints
│   │   ├── models/        # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   └── config/        # Settings
│   ├── main.py            # FastAPI app
│   └── requirements.txt
│
├── db/                     # Database
│   ├── migrations/         # SQL migration files
│   └── README.md          # Database setup guide
│
├── docs/                   # Documentation
│   ├── ARCHITECTURE.md    # System design
│   └── API.md             # API reference
│
├── README.md              # Project overview
├── .gitignore
└── .env.example           # Environment template
```

## Installation Steps

### 1. Clone & Navigate
```bash
cd auraStudio-ai
```

### 2. Install Root Dependencies
```bash
npm install  # or pnpm install if preferred
```

### 3. Web App Setup

```bash
cd web

# Install dependencies
npm install

# Copy environment template
cp ../.env.example .env.local

# Start development server
npm run dev
```

The web app will be available at `http://localhost:3000`

### 4. API Setup

```bash
cd ../api

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Start API server
python -m uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

Visit `http://localhost:8000/docs` for interactive Swagger documentation.

## Configuration

### 1. Supabase Setup

1. Create account at https://supabase.com
2. Create new project
3. Go to Settings → API
4. Copy `Project URL` and `Anon Key`
5. Add to `.env.local`:
   ```env
   NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
   ```

### 2. Database Migrations

1. Open Supabase SQL Editor
2. Copy contents of `db/migrations/001_initial_schema.sql`
3. Paste and execute
4. Repeat with `db/migrations/002_seed_data.sql`

### 3. API Keys (Optional for Full Features)

Add to `api/.env`:
```env
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=...
SYNC_LABS_API_KEY=...
MODAL_API_KEY=...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET=your-bucket
```

## Development Workflow

### Terminal 1: Web App
```bash
cd web
npm run dev
```

### Terminal 2: API Server
```bash
cd api
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn main:app --reload
```

### Terminal 3: (Optional) Database Monitor
```bash
# Watch database changes in Supabase dashboard
# https://app.supabase.com/project/[project]/editor/
```

## Testing the System

### 1. Test Web App
- Open http://localhost:3000
- You should see the AuraStudio dashboard

### 2. Test API Health
```bash
curl http://localhost:8000/health
# Should return: {"status": "healthy"}
```

### 3. Test Trickster Effect (requires audio file)
```bash
curl -X POST http://localhost:8000/api/audio/trickster \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "/path/to/audio.wav",
    "pitch_shift": 4.0,
    "formant_shift": 0.65,
    "tempo_rate": 1.1
  }'
```

### 4. Test Database Connection
- Open Supabase dashboard
- Go to Table Editor
- Verify all 7 tables exist:
  - user_profiles
  - projects
  - asset_vault
  - actor_dna
  - effect_library
  - export_jobs
  - script_analysis

## Common Issues & Solutions

### Issue: "Module not found: 'librosa'"
```bash
# Make sure you're in virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall requirements
pip install -r requirements.txt
```

### Issue: "Cannot connect to Supabase"
- Check `.env.local` has correct URL and key
- Verify Supabase project is active
- Check internet connection

### Issue: "Port 8000 already in use"
```bash
# Use different port
python -m uvicorn main:app --reload --port 8001
```

### Issue: "CORS error from web to API"
- Verify `CORS_ORIGINS` in `api/app/config/settings.py`
- Should include `http://localhost:3000`

## Next Steps

1. **Create Supabase Tables** – See `db/README.md`
2. **Configure AI Services** – Add API keys for GPT-4o, ElevenLabs, etc.
3. **Build Avatar Components** – Implement 3D viewer with Three.js
4. **Connect Real-time Sync** – Add Supabase listeners for project updates
5. **Deploy to Production** – Use Vercel (web) + Railway/ECS (API)

## Documentation

- [Architecture Overview](./docs/ARCHITECTURE.md)
- [API Reference](./docs/API.md)
- [Database Guide](./db/README.md)

## Support

For issues or questions:
1. Check documentation first
2. Review API docs at http://localhost:8000/docs
3. Check Supabase status dashboard

---

Happy creating! 🚀
