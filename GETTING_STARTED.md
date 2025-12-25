# 🎯 AuraStudio Omni - Getting Started (5 Minutes)

**Status**: ✅ Ready to Code  
**Last Updated**: December 25, 2025

---

## 👋 Welcome!

You have a fully configured development environment. Follow these 5 simple steps to start developing.

---

## Step 1: Configure Your API Keys (2 minutes)

```bash
# Edit the configuration file
code .env.development

# Add your real API keys:

# Required for basic functionality:
OPENAI_API_KEY=sk-your_key_here

# Optional (can add later):
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key_here
PINECONE_API_KEY=your_key_here
```

💡 **Don't have keys?** Get free API keys from:
- [OpenAI](https://platform.openai.com/api-keys) - Free trial
- [Supabase](https://supabase.com) - Free tier
- [Pinecone](https://www.pinecone.io) - Free tier

---

## Step 2: Start the Backend (1 minute)

### Option A: Automated (Recommended)
```bash
# Windows PowerShell
.\dev-start.ps1

# Linux/macOS
./dev-start.sh
```

### Option B: Manual
```bash
# Activate Python environment
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1

# Start API server
cd api
uvicorn main:app --reload
```

✅ **Success**: Server running at `http://localhost:8000`

---

## Step 3: Start the Frontend (1 minute)

Open a **new terminal** and run:

```bash
cd web
npm run dev
```

✅ **Success**: Frontend at `http://localhost:3000`

---

## Step 4: Verify Everything Works (30 seconds)

### Check Backend
```bash
curl http://localhost:8000/health
# Should return: {"status": "healthy", "version": "3.0.0"}
```

### Check Frontend
Open in browser: `http://localhost:3000`

### Check API Docs
Open in browser: `http://localhost:8000/api/docs`

✅ **Success**: All systems operational!

---

## Step 5: Make Your First API Call (30 seconds)

### Using Browser (Easiest)
1. Go to `http://localhost:8000/api/docs`
2. Expand any endpoint
3. Click "Try it out"
4. Click "Execute"

### Using curl (Terminal)
```bash
# Get API information
curl http://localhost:8000/api/info

# Try memory endpoint
curl -X POST http://localhost:8000/api/advanced/memory/store \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "summary": "Had coffee this morning",
    "full_text": "Started the day with a nice cup of coffee at my favorite cafe",
    "emotion": "happy"
  }'
```

---

## 🎉 You're Ready to Code!

### What to Do Next

**For Beginners**: 
- Explore `http://localhost:8000/api/docs` 
- Try different endpoints
- Read `DEVELOPER_ONBOARDING.md`

**For Developers**:
- Check `api/app/routes/advanced.py` for endpoints
- Look at `web/src/hooks/` for frontend integration
- Run `pytest api/tests` for tests

**For DevOps**:
- Use `docker-compose up` to run everything in containers
- See `DEPLOYMENT_CHECKLIST.md` for production setup

---

## 📚 Important Files

| File | Purpose | Read When |
|------|---------|-----------|
| [COMPLETE_SETUP_GUIDE.md](COMPLETE_SETUP_GUIDE.md) | Detailed setup steps | Need help with setup |
| [DEVELOPER_ONBOARDING.md](DEVELOPER_ONBOARDING.md) | Team training guide | Starting development |
| [VISION_3.0_MASTERPLAN.md](VISION_3.0_MASTERPLAN.md) | Feature roadmap | Understanding architecture |
| [IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md) | Progress tracking | Tracking work |
| [api/main.py](api/main.py) | API entry point | Understanding code |
| [api/app/config/settings.py](api/app/config/settings.py) | Configuration | Adding settings |

---

## 🆘 Troubleshooting

### Port 8000 already in use?
```bash
# Find what's using it
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill it
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Or use different port
cd api
uvicorn main:app --port 8001
```

### npm modules error?
```bash
cd web
rm -rf node_modules package-lock.json
npm install
```

### Python import errors?
```bash
# Reinstall dependencies
pip install -r api/requirements.txt
```

### Database connection error?
Database is optional for development. You can:
1. Install PostgreSQL locally
2. Use Docker: `docker-compose up postgres`
3. Continue without database (in-memory only)

---

## 🚀 Quick Commands

```bash
# Start everything (Backend + Frontend)
./dev-start.ps1  # Windows
./dev-start.sh   # Linux/macOS

# Start with Docker (includes PostgreSQL + Redis)
docker-compose up

# Run tests
pytest api/tests -v

# Format code
black api/app
isort api/app

# Lint code
flake8 api/app

# Check types
mypy api/app
```

---

## 📞 Need Help?

| Question | Answer |
|----------|--------|
| How do I add a new endpoint? | See `api/app/routes/advanced.py` |
| How do I add environment variables? | Edit `api/app/config/settings.py` |
| How do I connect to database? | See `COMPLETE_SETUP_GUIDE.md` |
| How do I deploy? | See `DEPLOYMENT_CHECKLIST.md` |
| Where are API docs? | `http://localhost:8000/api/docs` |
| How do I run tests? | `pytest api/tests -v` |

---

## 🎓 Learn More

**Understanding the Architecture**:
1. Read `VISION_3.0_MASTERPLAN.md` (5 min)
2. Look at `api/main.py` (2 min)
3. Check `api/app/routes/advanced.py` (5 min)

**Building Features**:
1. Review `DEVELOPER_ONBOARDING.md` (10 min)
2. Study existing endpoints (10 min)
3. Create your first endpoint (20 min)

**Deploying**:
1. Review `DEPLOYMENT_CHECKLIST.md` (10 min)
2. Configure production `.env` (5 min)
3. Deploy with Docker (10 min)

---

## ✅ Checklist

- [ ] Configured `.env.development` with API keys
- [ ] Started backend (`./dev-start.ps1` or `./dev-start.sh`)
- [ ] Started frontend (`npm run dev`)
- [ ] Verified API works (`http://localhost:8000/health`)
- [ ] Verified Frontend works (`http://localhost:3000`)
- [ ] Explored API docs (`http://localhost:8000/api/docs`)
- [ ] Read `DEVELOPER_ONBOARDING.md`
- [ ] Ready to code!

---

## 🎯 Next Steps

### Today (This Hour)
- ✅ Complete this guide
- → Explore API documentation
- → Try a few endpoints

### This Week
- → Set up database (optional)
- → Write first test
- → Make first code change
- → Submit pull request

### This Month
- → Implement major feature
- → Integrate with external API
- → Deploy to staging
- → Get code review

---

## 💡 Pro Tips

1. **Use Swagger UI**: Much better than curl!
   - Visit `http://localhost:8000/api/docs`
   - Try endpoints directly in browser

2. **Auto-reload**: Code changes auto-reload
   - Backend: Watch `api/app/`
   - Frontend: Watch `web/src/`

3. **Check logs**: See what's happening
   - Backend: Terminal where uvicorn runs
   - Frontend: Console in DevTools
   - Database: Docker logs

4. **Use TypeScript**: Get better IDE support
   - Hooks have types in `web/src/hooks/`
   - Models have types in `api/app/models/`

5. **Read documentation**: It's there!
   - Start with `DEVELOPER_ONBOARDING.md`
   - Reference `VISION_3.0_MASTERPLAN.md`
   - Use `http://localhost:8000/api/docs` for API

---

## 🎉 Welcome to AuraStudio Omni!

You now have access to:
- ✅ Complete FastAPI backend
- ✅ Modern Next.js frontend
- ✅ Comprehensive documentation
- ✅ Full development environment
- ✅ Production-ready architecture

**Everything is ready. Let's build something amazing!** 🚀

---

### Questions?
1. Check `COMPLETE_SETUP_GUIDE.md` for detailed help
2. Read `DEVELOPER_ONBOARDING.md` for best practices
3. See `VISION_3.0_MASTERPLAN.md` for architecture
4. Browse `/docs` folder for more guides

### Ready to code?
Go to: `http://localhost:3000` 🚀

---

**Happy Coding!**  
*AuraStudio Omni Development Team*
