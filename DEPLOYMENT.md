# PromptShield AI - Cloud Deployment Guide

This guide details how to deploy **PromptShield AI** to cloud hosting platforms.

---

## 1. Deploying Frontend (Next.js) on Vercel & Connecting to GitHub

### Method A: Vercel Dashboard + GitHub Integration (Recommended - Push-to-Deploy)

1. **Push your code to GitHub**:
   Ensure all changes are committed and pushed to `https://github.com/stromberg007/promptshield.git`.
2. **Import to Vercel**:
   - Go to [Vercel New Project Dashboard](https://vercel.com/new).
   - Select **Continue with GitHub** and import `stromberg007/promptshield`.
   - **Framework Preset**: `Next.js`
   - **Root Directory**: `frontend` (or leave default `./` as `vercel.json` at root is preconfigured).
3. **Configure Environment Variables**:
   Under **Environment Variables**, add:
   - `NEXT_PUBLIC_API_URL`: `https://your-backend-api.onrender.com/api/v1` (or your deployed backend URL)
4. **Deploy**:
   Click **Deploy**. Vercel will build and deploy the application.
5. **Connect URL to GitHub Repository**:
   - Vercel automatically links to the GitHub repository and posts build status badges on pull requests/commits.
   - Copy your deployed Vercel URL (e.g. `https://promptshield-frontend.vercel.app`).
   - On GitHub (`https://github.com/stromberg007/promptshield`), click the ⚙️ **Settings icon next to About** (on the right sidebar) and paste the URL into the **Website** field.

---

### Method B: Vercel CLI (Command Line Deployment)

1. **Install Vercel CLI & Authenticate**:
   ```bash
   npm i -g vercel
   vercel login
   ```
2. **Deploy to Vercel**:
   ```bash
   # From the project root
   vercel --prod
   ```
   Follow the prompts to link to your Vercel account and set project settings (`Root Directory`: `./frontend` or `./`).


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
