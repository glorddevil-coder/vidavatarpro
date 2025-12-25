# Production Deployment Guide - AuraStudio AI

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Production Environment                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────┐          ┌──────────────────┐         │
│  │    Vercel       │          │    Cloudflare    │         │
│  │   (Next.js)     │◄────────►│      (CDN)       │         │
│  │  Deployment     │          │   + DDoS Shield  │         │
│  └────────┬────────┘          └──────────────────┘         │
│           │                                                  │
│           │ API Requests                                    │
│           ▼                                                  │
│  ┌─────────────────────────────────────┐                   │
│  │   AWS ECS / Railway (FastAPI)       │                   │
│  │   - Auto-scaling containers         │                   │
│  │   - Health checks                   │                   │
│  │   - Load balancing                  │                   │
│  └────────┬────────────────────────────┘                   │
│           │                                                  │
│  ┌────────┼─────────────────────────────┐                  │
│  │        │                             │                   │
│  │  ┌─────▼──────┐        ┌─────────────▼──┐              │
│  │  │ Supabase   │        │   AWS S3       │              │
│  │  │ PostgreSQL │        │   (Assets)     │              │
│  │  │ + Realtime │        │   + CloudFront │              │
│  │  └────────────┘        └────────────────┘              │
│  │                                                          │
│  │  ┌──────────────────┐   ┌────────────────────┐         │
│  │  │   Modal.com      │   │   Redis Cache      │         │
│  │  │   (GPU Cluster)  │   │   (Session/Cache)  │         │
│  │  │   A100/H100      │   │                    │         │
│  │  └──────────────────┘   └────────────────────┘         │
│  │                                                          │
│  └──────────────────────────────────────────────────────────┘
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Web App Deployment (Next.js on Vercel)

### Prerequisites
- Vercel account (vercel.com)
- GitHub repository
- Environment variables configured

### Deployment Steps

1. **Connect GitHub Repository**
   ```bash
   # Push to GitHub
   git push origin main
   ```

2. **Import Project in Vercel**
   - Go to vercel.com
   - Click "Import Project"
   - Select GitHub repository
   - Configure build settings:
     - Framework: Next.js
     - Root Directory: `web`
     - Build Command: `npm run build`
     - Output Directory: `.next`

3. **Configure Environment Variables**
   In Vercel project settings:
   ```
   NEXT_PUBLIC_SUPABASE_URL = ...
   NEXT_PUBLIC_SUPABASE_ANON_KEY = ...
   NEXT_PUBLIC_API_URL = https://api.yourdomain.com
   NEXT_PUBLIC_OPENAI_API_KEY = ...
   NEXT_PUBLIC_ELEVENLABS_API_KEY = ...
   ... (other keys)
   ```

4. **Deploy**
   ```bash
   # Auto-deployment on git push
   git push origin main
   ```

   Vercel will:
   - Build Next.js app
   - Run tests (if configured)
   - Deploy to global CDN
   - Generate preview URLs for PRs

### Optimization

- **Image Optimization**: Next.js Image component auto-optimizes
- **Code Splitting**: Automatic route-based code splitting
- **ISR**: Incremental Static Regeneration for heavy pages
- **API Routes**: Use for lightweight backend operations

## API Deployment (FastAPI on AWS ECS)

### Option 1: AWS ECS + Fargate

1. **Create Docker Image**
   ```dockerfile
   # api/Dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Push to ECR**
   ```bash
   # Build image
   docker build -t aurastudio-api:latest api/
   
   # Tag for ECR
   docker tag aurastudio-api:latest \
     YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/aurastudio-api:latest
   
   # Push
   docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/aurastudio-api:latest
   ```

3. **Create ECS Cluster**
   - AWS Console → ECS
   - Create cluster (Fargate launch type)
   - Create task definition with:
     - CPU: 512+ (for audio processing)
     - Memory: 1024 MB+
     - Image from ECR
     - Port: 8000

4. **Create Service**
   - Min tasks: 2
   - Max tasks: 10 (auto-scaling)
   - Load balancer: ALB
   - Health check: `/health`

### Option 2: Railway (Simpler Alternative)

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login & Deploy**
   ```bash
   railway login
   cd api
   railway up
   ```

3. **Configure Environment**
   - Railway dashboard → Variables
   - Add all `.env` variables

4. **Deploy**
   - Railway auto-deploys on git push

## Database (Supabase Managed PostgreSQL)

### Setup

1. **Create Supabase Project**
   - supabase.com → New Project
   - Select region (close to users)
   - Generate password securely

2. **Run Migrations**
   ```bash
   # Via Supabase SQL Editor
   # Paste contents of db/migrations/*.sql
   ```

3. **Configure Backups**
   - Supabase → Settings → Backups
   - Enable daily backups
   - Set 30-day retention

4. **Enable RLS (Row Level Security)**
   ```sql
   ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
   
   CREATE POLICY "Users can see own projects"
   ON projects FOR SELECT
   USING (auth.uid() = user_id);
   ```

5. **Set Up Realtime**
   - Supabase → Realtime
   - Enable tables: `projects`, `export_jobs`

## Storage (AWS S3 + CloudFront)

### S3 Setup

1. **Create Bucket**
   ```bash
   aws s3 mb s3://aurastudio-assets --region us-east-1
   ```

2. **Configure CORS**
   ```json
   {
     "CORSRules": [
       {
         "AllowedHeaders": ["*"],
         "AllowedMethods": ["GET", "HEAD"],
         "AllowedOrigins": ["https://yourdomain.com"],
         "MaxAgeSeconds": 3000
       }
     ]
   }
   ```

3. **Enable Versioning**
   ```bash
   aws s3api put-bucket-versioning \
     --bucket aurastudio-assets \
     --versioning-configuration Status=Enabled
   ```

### CloudFront Distribution

1. **Create Distribution**
   - AWS CloudFront → Create Distribution
   - Origin: S3 bucket
   - Viewer Protocol: HTTPS only
   - Cache behavior: Compress + Cache long-lived

2. **Add Custom Domain**
   - Add CNAME: `assets.yourdomain.com`
   - Update DNS records

## GPU Rendering (Modal.com)

### Setup

1. **Create Account**
   - modal.com → Sign up
   - Create API token

2. **Deploy Function**
   ```python
   # api/services/modal_renderer.py
   import modal
   
   image = modal.Image.debian_slim().pip_install(
       "ffmpeg", "numpy", "torch"
   )
   app = modal.App(image=image)
   
   @app.function()
   def render_video(scene_data: dict) -> str:
       # Rendering logic
       return "s3://bucket/output.mp4"
   ```

3. **Deploy**
   ```bash
   modal deploy api/services/modal_renderer.py
   ```

## CI/CD Pipeline (GitHub Actions)

### Create `.github/workflows/deploy.yml`

```yaml
name: Deploy AuraStudio

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: 18
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11
      
      - name: Test Web
        run: |
          cd web
          npm install
          npm run lint
          npm run build
      
      - name: Test API
        run: |
          cd api
          pip install -r requirements.txt
          pytest

  deploy-web:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: vercel/action@main
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: web

  deploy-api:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build & Push Docker
        run: |
          docker build -t aurastudio-api:${{ github.sha }} api/
          docker login -u ${{ secrets.DOCKER_USER }} \
            -p ${{ secrets.DOCKER_PASS }}
          docker push aurastudio-api:${{ github.sha }}
      
      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster aurastudio \
            --service api \
            --force-new-deployment
```

## Monitoring & Logging

### Sentry (Error Tracking)

```python
# api/main.py
import sentry_sdk

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=1.0,
    environment="production"
)
```

### CloudWatch (AWS Logs)

```python
# api/config/settings.py
import logging
import watchtower

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        watchtower.CloudWatchLogHandler()
    ]
)
```

### Supabase Analytics

- Dashboard → Analytics
- Monitor API usage
- Database query performance
- Real-time connection count

## Security Checklist

- ✅ HTTPS everywhere (TLS 1.3)
- ✅ CORS properly configured
- ✅ Rate limiting enabled
- ✅ SQL injection prevention (ORM/parameterized queries)
- ✅ XSS protection (Next.js built-in)
- ✅ CSRF tokens
- ✅ Secrets management (never commit keys)
- ✅ Database encryption at rest
- ✅ API authentication (JWT tokens)
- ✅ Data backups (daily)
- ✅ DDoS protection (Cloudflare)

## Cost Optimization

| Service | Free Tier | Pro Pricing |
|---------|-----------|------------|
| Vercel | 100 GB bandwidth | $20/mo |
| Supabase | 500 MB DB | $25/mo |
| AWS S3 | 5 GB storage | $0.023/GB |
| CloudFront | 1 TB transfer | $0.085/GB |
| Modal GPU | - | $0.50/GPU hour |
| Railway | $5 credit | $7/mo base |

**Estimated Monthly Cost (small scale):** $100-200

## Scaling for 1M+ Users

1. **Database**: Upgrade Supabase to Enterprise
2. **API**: Increase ECS task count, add caching layer
3. **CDN**: Use multiple CloudFront distributions
4. **GPU**: Modal.com auto-scaling
5. **Analytics**: Add data warehouse (BigQuery)

---

**Deployment Status: Ready for Production** ✅
