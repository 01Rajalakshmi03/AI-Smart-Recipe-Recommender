# Deployment Guide

## Architecture

```
Frontend (Vercel)  -->  Backend (Render)  -->  SQLite Database
```

---

## 1. Deploy Backend to Render

### Step 1: Push to GitHub

```bash
cd AI-Smart-Recipe-Recommender
git add .
git commit -m "Production-ready deployment"
git push origin main
```

### Step 2: Create Render Web Service

1. Go to [render.com](https://render.com) and sign up / log in
2. Click **New +** > **Web Service**
3. Connect your GitHub repository
4. Configure the service:

| Setting | Value |
|---------|-------|
| **Name** | `ai-recipe-backend` |
| **Region** | Oregon (or closest to you) |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

### Step 3: Add Environment Variables

In Render dashboard, go to **Environment** tab and add:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | (Generate a random string, e.g. `openssl rand -hex 32`) |
| `JWT_SECRET_KEY` | (Same random string as above) |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` |
| `GEMINI_API_KEY` | `your_gemini_api_key` |
| `FRONTEND_URL` | `https://your-app.vercel.app` (update after deploying frontend) |
| `DEBUG` | `false` |

### Step 4: Deploy

- Click **Create Web Service**
- Render will build and deploy automatically
- Wait for deployment to finish (~2-3 minutes)
- Note your backend URL: `https://your-app.onrender.com`

### Step 5: Verify Backend

Open in browser:
```
https://your-app.onrender.com/
```
Expected response:
```json
{"message":"AI Smart Recipe Recommender API","version":"1.0.0"}
```

Test health endpoint:
```
https://your-app.onrender.com/api/health
```
Expected response:
```json
{"status":"healthy"}
```

> **Note:** Render free tier spins down after inactivity. First request may take 30-50 seconds.

---

## 2. Deploy Frontend to Vercel

### Step 1: Import Repository

1. Go to [vercel.com](https://vercel.com) and sign up / log in
2. Click **Add New Project**
3. Import your GitHub repository

### Step 2: Configure Project

| Setting | Value |
|---------|-------|
| **Framework Preset** | Vite |
| **Root Directory** | `frontend` |
| **Build Command** | `npm run build` |
| **Output Directory** | `dist` |

### Step 3: Add Environment Variables

| Key | Value |
|-----|-------|
| `VITE_API_URL` | `https://your-app.onrender.com/api` |
| `VITE_GEMINI_API_KEY` | `your_gemini_api_key` |

### Step 4: Deploy

- Click **Deploy**
- Wait for build to finish (~1-2 minutes)
- Vercel gives you a URL: `https://your-app.vercel.app`

---

## 3. Connect Frontend and Backend

After deploying both, update the backend's `FRONTEND_URL`:

1. Go to **Render** dashboard > **Environment**
2. Update `FRONTEND_URL` to your Vercel URL:
   ```
   FRONTEND_URL=https://your-app.vercel.app
   ```
3. Render will auto-redeploy

---

## 4. Update API URLs

The frontend uses `VITE_API_URL` to connect to the backend.

- **Development:** `http://localhost:8000/api`
- **Production:** `https://your-app.onrender.com/api`

The API service (`frontend/src/services/api.js`) reads this:
```js
baseURL: import.meta.env.VITE_API_URL || '/api'
```

In development, the Vite proxy forwards `/api` to `localhost:8000`. In production, it uses the full URL.

---

## 5. Verify CORS Configuration

The backend allows requests from:
- Your Vercel frontend URL
- `localhost:5173` (development)
- `localhost:3000` (development)

If you get CORS errors, check that `FRONTEND_URL` is set correctly on Render.

---

## 6. Troubleshooting

### Backend won't start on Render

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Check `requirements.txt` has all dependencies |
| `Address already in use` | Ensure start command uses `$PORT` not a fixed port |
| Database error | SQLite needs write permissions; Render's disk is ephemeral (data resets on redeploy) |

### Frontend shows blank page

| Problem | Solution |
|---------|----------|
| Build fails | Check Node version; ensure `npm run build` works locally |
| API calls fail | Verify `VITE_API_URL` is set correctly in Vercel |
| Blank page on refresh | Ensure `vercel.json` SPA rewrite is configured |

### API requests return 401

| Problem | Solution |
|---------|----------|
| Token expired | Tokens expire after 60 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`) |
| Wrong secret key | Ensure `JWT_SECRET_KEY` is set and consistent |

### Database resets on redeploy

| Problem | Solution |
|---------|----------|
| Data lost | Render free tier has ephemeral disk. Data resets on each deploy. Upgrade to paid tier for persistent disk, or migrate to PostgreSQL |

### Slow first request

| Problem | Solution |
|---------|----------|
| 30-50s cold start | Render free tier spins down after 15 min of inactivity. This is expected behavior. Upgrade to paid tier for always-on |

---

## 7. Production Checklist

- [ ] `SECRET_KEY` is set to a random, secure string
- [ ] `JWT_SECRET_KEY` is set to a random, secure string  
- [ ] `GEMINI_API_KEY` is set
- [ ] `FRONTEND_URL` matches your Vercel URL exactly
- [ ] `DEBUG` is set to `false`
- [ ] Backend returns healthy response at `/api/health`
- [ ] Frontend loads and connects to backend API
- [ ] Login/Register works
- [ ] Recipe browsing works with pagination
- [ ] Filters (category, cuisine, dietary) work correctly
- [ ] AI recipe generation works

---

## Environment Variables Summary

### Backend (Render)

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | App-level secret key |
| `JWT_SECRET_KEY` | Yes | JWT token signing key |
| `ALGORITHM` | No | JWT algorithm (default: `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | Token expiry (default: `60`) |
| `GEMINI_API_KEY` | Yes | Google Gemini API key |
| `FRONTEND_URL` | Yes | Vercel frontend URL for CORS |
| `DEBUG` | No | Enable debug mode (default: `false`) |

### Frontend (Vercel)

| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_API_URL` | Yes | Backend API base URL |
| `VITE_GEMINI_API_KEY` | No | Gemini API key (if used client-side) |
