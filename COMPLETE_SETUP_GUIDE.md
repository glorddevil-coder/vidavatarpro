# AuraStudio Omni - Complete Development Environment Setup Guide

## Quick Start (5 minutes)

### Prerequisites
- Python 3.11+ (or 3.14)
- Node.js 18+
- npm or yarn
- PostgreSQL 14+ (optional, can use Docker)
- Docker & Docker Compose (optional, recommended)

### Option 1: Automated Setup (Recommended)

```bash
# Navigate to project directory
cd auraudio

# Run setup script
python setup.py

# This will:
# ✓ Create virtual environment
# ✓ Install Python dependencies
# ✓ Install Node dependencies
# ✓ Create .env configuration files
# ✓ Validate environment
```

### Option 2: Manual Setup

#### 1. Backend Setup (FastAPI)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
cd api
pip install -r requirements.txt
cd ..
```

#### 2. Frontend Setup (Next.js)
```bash
# Install Node dependencies
cd web
npm install
cd ..
```

#### 3. Environment Configuration
```bash
# Copy development environment
cp .env.development .env

# Edit with your API keys
# Required:
# - OPENAI_API_KEY
# - SUPABASE_URL
# - SUPABASE_KEY
# 
# Optional (for advanced features):
# - PINECONE_API_KEY
# - GOOGLE_TRANSLATE_API_KEY
# - DEEPL_API_KEY
```

---

## Starting Development Servers

### Option 1: Using Startup Scripts

#### Windows (PowerShell)
```powershell
# Start API server
.\dev-start.ps1

# In another terminal, start frontend:
cd web
npm run dev
```

#### Linux/macOS (Bash)
```bash
# Start API server
./dev-start.sh

# In another terminal, start frontend:
cd web
npm run dev
```

### Option 2: Manual Start

#### Terminal 1 - FastAPI Backend
```bash
# Activate venv first
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1

# Start API server
cd api
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# API available at: http://localhost:8000
# Docs at: http://localhost:8000/api/docs
```

#### Terminal 2 - Next.js Frontend
```bash
cd web
npm run dev

# Frontend available at: http://localhost:3000
```

### Option 3: Docker Compose (Recommended for complete setup)

```bash
# Start all services (PostgreSQL, Redis, API, PgAdmin)
docker-compose up

# Services available at:
# API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
# PostgreSQL: localhost:5432
# Redis: localhost:6379
# PgAdmin: http://localhost:5050
```

---

## Verifying the Setup

### Check API Health
```bash
# In browser or terminal:
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "version": "3.0.0"}
```

### Check API Documentation
```
Visit: http://localhost:8000/api/docs
```

### Check Frontend
```
Visit: http://localhost:3000
```

### Check API Info
```bash
curl http://localhost:8000/api/info

# Shows feature flags and configuration
```

---

## Testing the System

### Run Backend Tests
```bash
# Activate venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1

# Run all tests
pytest api/tests -v

# Run specific test file
pytest api/tests/test_memory.py -v

# Run with coverage
pytest api/tests --cov=api/app
```

### Run Frontend Tests
```bash
cd web
npm test
```

---

## Database Setup (Optional)

### Option 1: PostgreSQL Locally

```bash
# Install PostgreSQL (macOS with Homebrew)
brew install postgresql

# Start PostgreSQL service
brew services start postgresql

# Create database
createdb auraudio_dev

# Run migrations
cd db
psql -U postgres -d auraudio_dev -f migrations/001_initial_schema.sql
psql -U postgres -d auraudio_dev -f migrations/002_seed_data.sql
cd ..
```

### Option 2: PostgreSQL with Docker
```bash
# Run PostgreSQL container
docker run --name postgres-auraudio \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=auraudio_dev \
  -p 5432:5432 \
  -d postgres:15

# Run migrations
cd db
psql -h localhost -U postgres -d auraudio_dev -f migrations/001_initial_schema.sql
psql -h localhost -U postgres -d auraudio_dev -f migrations/002_seed_data.sql
cd ..
```

### Connect Database to Application
```bash
# Update .env file:
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/auraudio_dev

# Restart API server
```

---

## API Key Setup

### 1. OpenAI API Key
```bash
# Get from: https://platform.openai.com/api-keys

# In .env file:
OPENAI_API_KEY=sk-YOUR_ACTUAL_KEY_HERE
OPENAI_MODEL_EMBEDDINGS=text-embedding-3-small
OPENAI_MODEL_CHAT=gpt-4-turbo
```

### 2. Supabase (Optional)
```bash
# Create account at: https://supabase.com

# In .env file:
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

### 3. Pinecone Vector DB (Optional)
```bash
# Get from: https://www.pinecone.io

# In .env file:
VECTOR_DB_TYPE=pinecone
PINECONE_API_KEY=your_api_key
PINECONE_ENVIRONMENT=your_environment
PINECONE_INDEX_NAME=auraudio-embeddings
```

### 4. Translation Services (Optional)
```bash
# Google Translate: https://cloud.google.com/translate
GOOGLE_TRANSLATE_API_KEY=your_key

# DeepL: https://www.deepl.com/pro-api
DEEPL_API_KEY=your_key
DEEPL_API_TYPE=free  # or 'pro'
```

---

## Troubleshooting

### Python venv not activating
```bash
# Windows - allow scripts to run
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
.\venv\Scripts\Activate.ps1
```

### Port 8000 already in use
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Or use different port
uvicorn main:app --port 8001
```

### Node modules permission error
```bash
# Fix npm permissions
npm install -g npm

# Or use Yarn
yarn install
```

### PostgreSQL connection error
```bash
# Check if PostgreSQL is running
pg_isready

# If not running:
# macOS: brew services start postgresql
# Linux: sudo systemctl start postgresql
# Windows: Open Services and start PostgreSQL

# Verify connection string
psql -U postgres -c "SELECT 1"
```

### Docker service won't start
```bash
# Check Docker is installed
docker --version

# Check Docker daemon is running
docker ps

# Debug compose
docker-compose logs -f api
docker-compose logs -f postgres
```

---

## Development Workflow

### 1. Making Changes
```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes to code
# Changes in api/ will auto-reload (--reload flag)
# Changes in web/ will auto-reload
```

### 2. Testing Changes
```bash
# Run tests
pytest api/tests -v

# Or with Docker
docker-compose exec api pytest tests -v
```

### 3. Committing Changes
```bash
# Format code
black api/app
isort api/app

# Lint
flake8 api/app

# Commit
git add .
git commit -m "feat: Add my feature"
git push origin feature/my-feature
```

### 4. Pull Request
- Go to GitHub
- Create PR from feature branch
- CI/CD will run automatically
- Wait for approval
- Merge to develop/main

---

## Configuration Files Explained

### .env.development
Used for local development. Contains:
- Development database URL
- Mock API keys (can use dummy values)
- Debug mode enabled
- All features enabled

### .env.production
Used for production deployment. Contains:
- Production database URL
- Real API keys
- Debug mode disabled
- Optimized settings

### .env.testing
Used for automated tests. Contains:
- Test database URL
- Mock external APIs
- Isolated configuration

### api/app/config/settings.py
Python settings module that:
- Loads environment variables
- Validates configuration
- Provides type safety
- Supports multiple environments

---

## Project Structure

```
auraudio/
├── api/                          # FastAPI backend
│   ├── main.py                  # FastAPI application entry
│   ├── requirements.txt          # Python dependencies
│   ├── app/
│   │   ├── config/              # Configuration
│   │   ├── models/              # Pydantic models
│   │   ├── routes/              # API endpoints
│   │   ├── services/            # Business logic
│   │   └── utils/               # Utilities
│   └── tests/                   # Unit tests
│
├── web/                          # Next.js frontend
│   ├── src/
│   │   ├── app/                 # Next.js pages
│   │   ├── components/          # React components
│   │   ├── hooks/               # Custom hooks
│   │   ├── lib/                 # Utilities
│   │   └── types/               # TypeScript types
│   ├── package.json             # npm dependencies
│   └── tsconfig.json
│
├── db/                           # Database
│   ├── migrations/              # SQL migrations
│   └── README.md
│
├── .env.development              # Dev config
├── .env.production               # Prod config
├── docker-compose.yml            # Docker services
├── Dockerfile.api                # API container
└── setup.py                      # Setup script
```

---

## Common Tasks

### Add a new API endpoint
1. Create route in `api/app/routes/`
2. Add Pydantic models in `api/app/models/`
3. Add service logic in `api/app/services/`
4. Test with `curl` or Swagger UI
5. Add frontend component in `web/src/components/`

### Add a new environment variable
1. Add to `.env.*` files
2. Add to `api/app/config/settings.py`
3. Use `settings.your_variable` in code

### Run database migrations
1. Edit migration file in `db/migrations/`
2. Run: `psql -f migrations/001_*.sql`
3. Verify with: `psql -l` and `\dt`

### Deploy to production
1. Push to main branch
2. CI/CD builds Docker image
3. Deploy to AWS ECS or Vercel
4. Run migrations on production DB
5. Monitor with CloudWatch

---

## Performance Optimization

### Backend
```bash
# Run with more workers
uvicorn main:app --workers 4

# Enable caching
REDIS_ENABLED=true

# Use pgvector for embeddings
VECTOR_DB_TYPE=pgvector
```

### Frontend
```bash
# Build for production
npm run build

# Analyze bundle size
npm run analyze
```

### Database
```bash
# Add indexes
CREATE INDEX idx_user_memory ON user_memory(user_id);

# Monitor slow queries
\timing on
```

---

## Security Checklist

- [ ] API keys in `.env` (never in code)
- [ ] HTTPS in production
- [ ] JWT tokens for authentication
- [ ] CORS properly configured
- [ ] Database password strong
- [ ] Regular backups
- [ ] Security scanning in CI/CD
- [ ] Rate limiting enabled
- [ ] Input validation
- [ ] Error messages don't leak info

---

## Monitoring & Logging

### Backend Logging
```bash
# Check logs
tail -f logs/api.log

# Or with Docker
docker-compose logs -f api
```

### Frontend Monitoring
```bash
# Browser DevTools
F12 -> Console tab

# Or check Next.js server output
```

### Database Monitoring
```bash
# Connect to PgAdmin
http://localhost:5050

# Login: admin@example.com / admin
# Add server: postgres:5432
```

---

## Next Steps

1. ✅ Complete setup (you are here)
2. → Configure API keys
3. → Explore API documentation
4. → Build your features
5. → Write tests
6. → Deploy to production

---

## Support & Resources

- **Documentation**: See `docs/` folder
- **API Docs**: http://localhost:8000/api/docs
- **GitHub Issues**: Create issue on GitHub
- **Discussions**: GitHub Discussions
- **Email**: support@auraudio.com

---

**Happy Coding! 🚀**

For more details, see:
- [DEVELOPER_ONBOARDING.md](DEVELOPER_ONBOARDING.md)
- [IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md)
- [docs/QUICKSTART_ADVANCED.md](docs/QUICKSTART_ADVANCED.md)
