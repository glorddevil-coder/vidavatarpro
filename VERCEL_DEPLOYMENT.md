# 🚀 Vercel Deployment Guide - AuraStudio Omni v3.0+

**Status**: Ready for Deployment  
**Date**: December 25, 2025  
**Framework**: Next.js 16.1.1  

---

## ⚠️ Common Deployment Issues & Fixes

### Issue 1: API Routes Not Working
**Problem**: Backend API calls fail in production
**Solution**: Configure environment variables for production API

### Issue 2: Environment Variables Missing
**Problem**: `.env` variables not loaded
**Solution**: Add to Vercel project settings

### Issue 3: Build Failures
**Problem**: TypeScript or dependency errors during build
**Solution**: Verify all dependencies installed

---

## ✅ Step-by-Step Deployment

### Step 1: Prepare Your Repository

Ensure your git repository is clean and committed:

```bash
cd "g:\softwere\develop\avator 2"
git status
git add .
git commit -m "Add AuraStudio Omni v3.0+ advanced features"
git push -u origin main
```

### Step 2: Create Vercel Configuration

Create `vercel.json` in the root directory:

```json
{
  "version": 2,
  "buildCommand": "cd web && npm run build",
  "devCommand": "cd web && npm run dev",
  "installCommand": "npm install",
  "env": {
    "NEXT_PUBLIC_API_URL": {
      "required": true
    }
  },
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "${NEXT_PUBLIC_API_URL}/api/:path*"
    }
  ]
}
```

### Step 3: Update Next.js Config

Update `web/next.config.ts`:

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactCompiler: true,
  headers: async () => [
    {
      source: "/api/:path*",
      headers: [
        { key: "Access-Control-Allow-Credentials", value: "true" },
        { key: "Access-Control-Allow-Origin", value: "*" },
        { key: "Access-Control-Allow-Methods", value: "GET,OPTIONS,PATCH,DELETE,POST,PUT" },
        { key: "Access-Control-Allow-Headers", value: "X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version" },
      ],
    },
  ],
  rewrites: async () => ({
    beforeFiles: [
      {
        source: "/api/:path*",
        destination: `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/:path*`,
      },
    ],
  }),
};

export default nextConfig;
```

### Step 4: Create Environment File

Create `.env.production`:

```
NEXT_PUBLIC_API_URL=https://your-api-domain.com
NEXT_PUBLIC_APP_NAME=AuraStudio Omni
NEXT_PUBLIC_APP_VERSION=3.0.0
```

Create `.env.local` (for local testing):

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Step 5: Deploy to Vercel

#### Option A: Using Vercel CLI

```bash
npm install -g vercel
vercel login
cd "g:\softwere\develop\avator 2\web"
vercel --prod
```

#### Option B: Using GitHub Integration

1. Go to https://vercel.com
2. Click "New Project"
3. Connect your GitHub repository
4. Select the project
5. Configure:
   - **Root Directory**: `web`
   - **Build Command**: `npm run build`
   - **Install Command**: `npm install`
   - **Output Directory**: `.next`
6. Add Environment Variables:
   - `NEXT_PUBLIC_API_URL` = Your backend API URL
7. Click Deploy

---

## 🔧 Configuration Files to Create

### vercel.json
```json
{
  "version": 2,
  "buildCommand": "cd web && npm run build",
  "devCommand": "cd web && npm run dev",
  "installCommand": "npm install",
  "env": {
    "NEXT_PUBLIC_API_URL": {
      "required": true,
      "description": "Backend API URL (e.g., https://api.yourdomain.com)"
    },
    "NEXT_PUBLIC_APP_VERSION": {
      "default": "3.0.0"
    }
  },
  "regions": ["iad1", "sfo1"],
  "crons": [
    {
      "path": "/api/cron/health-check",
      "schedule": "0 */6 * * *"
    }
  ]
}
```

### web/.env.production
```
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_APP_NAME=AuraStudio Omni
NEXT_PUBLIC_APP_VERSION=3.0.0
NEXT_PUBLIC_SENTRY_DSN=https://your-sentry-dsn@sentry.io/123456
```

### web/.env.local (development)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📋 Pre-Deployment Checklist

### Frontend Checks
- [ ] `npm run build` succeeds locally
- [ ] `npm run lint` passes
- [ ] No TypeScript errors
- [ ] All dependencies in package.json
- [ ] Environment variables configured
- [ ] CORS headers configured

### Backend Checks
- [ ] API running on accessible port
- [ ] All endpoints tested (29/29 ✅)
- [ ] CORS enabled for frontend domain
- [ ] Database connected
- [ ] Error handling in place
- [ ] Logging configured

### Repository Checks
- [ ] All files committed
- [ ] `.gitignore` configured correctly
- [ ] No sensitive data in repo
- [ ] README updated
- [ ] Version bumped
- [ ] Changelog updated

---

## 🚀 Deployment Steps (Quick)

### 1. Build Frontend Locally
```bash
cd web
npm run build
```

Expected output:
```
✓ Compiled successfully
✓ Linting and checking validity of types
✓ Built successfully
```

### 2. Test Production Build
```bash
npm run start
```

Visit: http://localhost:3000

### 3. Deploy to Vercel
```bash
vercel --prod
```

---

## ❌ Common Errors & Solutions

### Error: "Cannot find module 'next'"
**Solution**:
```bash
cd web
npm install
vercel --prod
```

### Error: "API requests return 404"
**Solution**: 
- Check `NEXT_PUBLIC_API_URL` in Vercel settings
- Verify backend API is accessible
- Check CORS configuration on backend

### Error: "Build timeout"
**Solution**:
- Check for large files in project
- Ensure dependencies are optimized
- Increase build timeout in vercel.json

### Error: "Environment variable not found"
**Solution**:
- Add to Vercel Dashboard → Settings → Environment Variables
- Restart deployment

---

## 🔐 Security Checklist

### Before Going Live
- [ ] Environment variables are secret (not in code)
- [ ] API keys are not exposed
- [ ] HTTPS is enabled
- [ ] CORS is properly configured
- [ ] Rate limiting is in place
- [ ] Database credentials are secure

### Post-Deployment
- [ ] Monitor error logs
- [ ] Check performance metrics
- [ ] Verify security headers
- [ ] Test CORS handling
- [ ] Monitor API usage

---

## 📊 Deployment Architecture

```
┌─────────────────────────────────────┐
│     Vercel (Frontend)               │
│  - Next.js 16.1.1                   │
│  - Port: 443 (HTTPS)                │
│  - URL: yourdomain.vercel.app       │
└────────────┬────────────────────────┘
             │
             │ API Calls
             │
┌────────────▼────────────────────────┐
│     Backend API (Separate)          │
│  - FastAPI / Python                 │
│  - Port: 8000 or custom             │
│  - URL: api.yourdomain.com          │
└─────────────────────────────────────┘
```

---

## 🧪 Post-Deployment Testing

### Frontend Tests
```bash
curl http://yourdomain.vercel.app/
# Should return HTML homepage
```

### API Tests
```bash
curl http://yourdomain.vercel.app/api/v3/physique/health
# Should proxy to backend API
```

### Backend Tests
```bash
curl http://api.yourdomain.com/api/v3/physique/health
# Should return: {"status": "healthy"}
```

---

## 📈 Monitoring & Logging

### Set Up Sentry (Error Tracking)
```bash
npm install @sentry/nextjs
```

### Configure in next.config.ts
```typescript
import { withSentryConfig } from "@sentry/nextjs";

const nextConfig = {
  // ... your config
};

export default withSentryConfig(nextConfig, {
  org: "your-org",
  project: "your-project",
  authToken: process.env.SENTRY_AUTH_TOKEN,
});
```

### Monitor in Vercel Dashboard
- Analytics
- Performance metrics
- Error rates
- Build times

---

## 🎯 Quick Deployment Command

Once configured, deploy with:
```bash
cd "g:\softwere\develop\avator 2"
git add .
git commit -m "Production deployment"
git push origin main
# Vercel auto-deploys on push (if configured)
```

---

## 📞 Support

### Troubleshooting Resources
- Vercel Docs: https://vercel.com/docs
- Next.js Docs: https://nextjs.org/docs
- Discord: https://vercel.com/support

### Common Vercel Commands
```bash
vercel login                # Login to Vercel
vercel                      # Deploy to preview
vercel --prod              # Deploy to production
vercel env ls              # List environment variables
vercel env add VAR_NAME    # Add environment variable
vercel rollback            # Rollback to previous deployment
vercel remove              # Remove project from Vercel
```

---

## ✅ Final Checklist

- [ ] Repository pushed to GitHub/GitLab
- [ ] Vercel project created
- [ ] Environment variables configured
- [ ] Backend API accessible
- [ ] Frontend builds without errors
- [ ] CORS properly configured
- [ ] Deployment successful
- [ ] Tests pass in production
- [ ] Monitoring set up
- [ ] Domain configured

---

**Status**: Ready for Vercel Deployment  
**Next Step**: Follow steps 1-5 above  

🚀 **Your AuraStudio Omni is ready to launch on Vercel!**
