# PromptShield AI - Cloud Deployment Guide

This guide details how to deploy **PromptShield AI** to cloud hosting platforms.

---

## 1. Deploying Frontend (Next.js) on Vercel

1. **Push to GitHub**:
   Ensure your code is pushed to a remote GitHub repository.
2. **Connect to Vercel**:
   - Go to [Vercel Dashboard](https://vercel.com/new).
   - Import your repository and set Root Directory to `frontend`.
3. **Environment Variables**:
   Add the following environment variable:
   ```env
   NEXT_PUBLIC_API_URL=https://your-backend-service.onrender.com/api/v1
   ```
4. **Deploy**: Click **Deploy**. Vercel will build the Next.js static pages and API routes.

---

## 2. Deploying Backend (FastAPI + Docker) on Render / Railway

### Option A: Render
1. Go to [Render Dashboard](https://dashboard.render.com/) -> **New Web Service**.
2. Connect your repository and select directory `backend`.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variables:
   - `SECRET_KEY`: `your_random_secure_key`
   - `DATABASE_URL`: `sqlite+aiosqlite:///./promptshield.db` (or Render PostgreSQL URL)

### Option B: Railway
1. Go to [Railway.app](https://railway.app/).
2. Create New Project from GitHub Repo.
3. Add **PostgreSQL** and **Redis** database plugins.
4. Set `DATABASE_URL` and `REDIS_URL` in environment variables.

---

## 3. Deploying to Google Cloud Run (Containerized)

```bash
# 1. Build & Tag Docker Image
docker build -t gcr.io/YOUR_GCP_PROJECT_ID/promptshield-backend:v1 ./backend

# 2. Push to Google Container Registry
docker push gcr.io/YOUR_GCP_PROJECT_ID/promptshield-backend:v1

# 3. Deploy to Cloud Run
gcloud run deploy promptshield-backend \
  --image gcr.io/YOUR_GCP_PROJECT_ID/promptshield-backend:v1 \
  --platform managed \
  --allow-unauthenticated \
  --region us-central1 \
  --set-env-vars SECRET_KEY="your_secret_key"
```

---

## 4. Multi-Container Docker Compose Deployment

On an EC2 instance, DigitalOcean Droplet, or Linux VPS:

```bash
git clone https://github.com/YOUR_USERNAME/promptshield.git
cd promptshield
docker-compose up -d --build
```
This launches:
- `frontend`: Port 3000
- `backend`: Port 8000
- `celery_worker`: Background tasks
- `redis`: Port 6379
