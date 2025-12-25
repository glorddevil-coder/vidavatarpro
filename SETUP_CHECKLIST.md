# ✅ AuraStudio AI - Setup Checklist

## 📋 Pre-Setup Requirements

- [ ] Node.js 18+ installed (`node --version`)
- [ ] Python 3.10+ installed (`python --version`)
- [ ] Git installed (`git --version`)
- [ ] Text editor/IDE ready (VSCode recommended)
- [ ] Internet connection for package downloads

## 🏗️ Project Structure Verification

- [x] **Root folder created**: `g:\softwere\develop\avator 2`
- [x] **Directory structure**: `web/`, `api/`, `db/`, `docs/`
- [x] **Root files**: README.md, QUICKSTART.md, .gitignore
- [x] **Web app**: Next.js initialized in `web/`
- [x] **API**: FastAPI structure in `api/`
- [x] **Database**: Migrations in `db/migrations/`
- [x] **Documentation**: Files in `docs/`

## 💻 Local Development Setup

### Terminal 1: Web App Setup
```bash
cd web
npm install
npm run dev  # Starts on http://localhost:3000
```
- [ ] Dependency installation completes
- [ ] Dev server starts without errors
- [ ] Browser shows default Next.js page

### Terminal 2: API Setup
```bash
cd api
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload  # Starts on http://localhost:8000
```
- [ ] Virtual environment created
- [ ] Dependencies installed (expect ~2-3 min)
- [ ] API server starts without errors
- [ ] Swagger UI available at http://localhost:8000/docs

## 🔐 Configuration Setup

### Step 1: Copy Environment Templates
```bash
cd web
cp ../.env.example .env.local

cd ../api
cp .env.example .env
```
- [ ] `.env.local` created in `web/`
- [ ] `.env` created in `api/`

### Step 2: Add Required Values
Edit `web/.env.local`:
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_key_here
NEXT_PUBLIC_API_URL=http://localhost:8000
```
- [ ] Supabase URL placeholder updated
- [ ] Supabase key placeholder updated
- [ ] API URL points to localhost:8000

Edit `api/.env`:
```env
DATABASE_URL=postgresql://...
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_key_here
```
- [ ] Database URL configured (or keep default)
- [ ] API configuration complete

## 🗄️ Database Setup

### Option A: Supabase (Recommended)
1. [ ] Create account at https://supabase.com
2. [ ] Create new project
3. [ ] Go to SQL Editor
4. [ ] Copy contents of `db/migrations/001_initial_schema.sql`
5. [ ] Paste and execute
6. [ ] Copy contents of `db/migrations/002_seed_data.sql`
7. [ ] Paste and execute
8. [ ] Verify tables in Table Editor:
   - [ ] user_profiles
   - [ ] projects
   - [ ] asset_vault
   - [ ] actor_dna
   - [ ] effect_library
   - [ ] export_jobs
   - [ ] script_analysis

### Option B: Local PostgreSQL
```bash
createdb aurastudio
psql aurastudio < db/migrations/001_initial_schema.sql
psql aurastudio < db/migrations/002_seed_data.sql
```
- [ ] Database created
- [ ] Migrations executed
- [ ] All 7 tables present

## ✅ Verification Tests

### Test 1: Web App
```bash
curl http://localhost:3000
# Should return HTML (status 200)
```
- [ ] Web app responds
- [ ] No CORS errors in console

### Test 2: API Health
```bash
curl http://localhost:8000/health
# Should return: {"status": "healthy"}
```
- [ ] API responds
- [ ] Health check passes

### Test 3: Swagger Documentation
- [ ] Open http://localhost:8000/docs
- [ ] See all endpoints listed
- [ ] Can expand each endpoint

### Test 4: Database Connection
- [ ] Open Supabase/PostgreSQL dashboard
- [ ] Verify tables exist
- [ ] Verify seed data (5 avatars, 4 effects)

### Test 5: Trickster Audio Engine
```bash
# Test audio processing endpoint
curl -X POST http://localhost:8000/api/audio/trickster \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "test.wav",
    "pitch_shift": 4.0,
    "formant_shift": 0.65,
    "tempo_rate": 1.1
  }'
```
- [ ] Endpoint accessible
- [ ] Returns proper JSON response

## 📚 Documentation Review

- [ ] Read [README.md](README.md) – Project overview
- [ ] Read [QUICKSTART.md](QUICKSTART.md) – Setup guide
- [ ] Skim [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) – System design
- [ ] Bookmark [docs/API.md](docs/API.md) – API reference
- [ ] Review [INDEX.md](INDEX.md) – Navigation guide

## 🔧 Development Environment

### VSCode Extensions (Recommended)
- [ ] Pylance (Python type checking)
- [ ] ESLint (JavaScript linting)
- [ ] Prettier (Code formatter)
- [ ] Thunder Client (API testing)
- [ ] PostgreSQL (DB management)

### Project Settings
- [ ] VSCode workspace opened: root folder
- [ ] Python interpreter selected (from venv)
- [ ] Node.js version verified (18+)
- [ ] Port 3000 not in use (web)
- [ ] Port 8000 not in use (API)

## 🔑 API Keys (Optional, for Full Features)

When ready to integrate AI services:
- [ ] OpenAI API key → `NEXT_PUBLIC_OPENAI_API_KEY`
- [ ] ElevenLabs key → `NEXT_PUBLIC_ELEVENLABS_API_KEY`
- [ ] Sync Labs key → `NEXT_PUBLIC_SYNC_LABS_API_KEY`
- [ ] Modal.com key → `NEXT_PUBLIC_MODAL_API_KEY`
- [ ] AWS S3 credentials → `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`

## 🚀 First Code Changes

- [ ] Create new branch: `git checkout -b feature/first-feature`
- [ ] Make a test change to `web/src/page.tsx`
- [ ] Verify hot-reload works
- [ ] Commit change: `git add . && git commit -m "test: verify dev setup"`
- [ ] Push to GitHub: `git push origin feature/first-feature`

## 📊 Status Checklist

### Foundation ✅
- [x] Folder structure created
- [x] Next.js app initialized
- [x] FastAPI app created
- [x] Database schema designed
- [x] Type definitions created
- [x] Documentation written

### Development Ready ⏳ (In Progress)
- [ ] Local environment configured
- [ ] Database tables created
- [ ] API running locally
- [ ] Web app running locally
- [ ] All tests passing
- [ ] Ready to code features

### Ready to Deploy 📋 (Future)
- [ ] All features implemented
- [ ] Tests comprehensive
- [ ] Documentation updated
- [ ] Performance optimized
- [ ] Security reviewed
- [ ] Ready for production

## 🎯 Quick Start Commands

### One-time setup
```bash
# Navigate to project
cd "g:\softwere\develop\avator 2"

# Web app initial setup
cd web && npm install && cd ..

# API initial setup
cd api && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && cd ..
```

### Daily development
```bash
# Terminal 1: Web app
cd web && npm run dev

# Terminal 2: API
cd api && source venv/bin/activate && python -m uvicorn main:app --reload

# Terminal 3: (optional) Watch database
# Open Supabase dashboard
```

## 🐛 Troubleshooting

### Issue: Port 3000 or 8000 already in use
**Solution:**
```bash
# Change port in next.js
npm run dev -- -p 3001

# Change port in FastAPI
python -m uvicorn main:app --port 8001
```
- [ ] Alternative ports configured

### Issue: "Module not found" in Python
**Solution:**
```bash
# Verify virtual environment active
which python  # or: where python (Windows)
# Should show path inside venv/

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```
- [ ] Virtual environment activated
- [ ] Dependencies reinstalled

### Issue: npm install fails
**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Remove node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```
- [ ] Cache cleared
- [ ] Fresh install completed

### Issue: Cannot connect to Supabase
**Solution:**
- [ ] Verify URL format: `https://xxxxx.supabase.co`
- [ ] Verify API key is correct (not truncated)
- [ ] Check Supabase project is active (not paused)
- [ ] Test connection string in .env files

## 📞 Support Resources

When stuck:
1. [ ] Check [QUICKSTART.md](QUICKSTART.md) troubleshooting section
2. [ ] Review [docs/API.md](docs/API.md) for endpoint details
3. [ ] Check Supabase status: https://status.supabase.com
4. [ ] Search error message on Stack Overflow
5. [ ] Review FastAPI docs: https://fastapi.tiangolo.com

## ✨ You're Ready!

Once all checks are complete:

1. **You can start developing** – Components, features, integrations
2. **You understand the system** – Architecture is clear
3. **You have working local environment** – Web + API + Database
4. **You have documentation** – Architecture, API, deployment guides

### Next Steps:
1. Start with [first feature](docs/ARCHITECTURE.md)
2. Use [docs/API.md](docs/API.md) for reference
3. Review [web/src/hooks/useProjects.ts](web/src/hooks/useProjects.ts) for patterns
4. Build components in `web/src/components/`
5. Commit regularly to git

---

**Estimated Setup Time:** 30 minutes to 1 hour  
**Ready Status:** Check completion percentage below

## Completion Tracker

**Foundation (Already Done):**
- [x] Project structure: 100%
- [x] Code scaffolding: 100%
- [x] Documentation: 100%

**Your Setup (In Progress):**
- [ ] Local environment: 0%
- [ ] Database configuration: 0%
- [ ] Verification tests: 0%

**Ready to Code:** 0% (will be 100% after completing above)

---

*Last Updated: December 2024*  
*Print this checklist and track your progress!* ✅
