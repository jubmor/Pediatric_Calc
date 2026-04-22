# Deployment Guide - GitHub + Render.com

## Step 1: Create GitHub Repository

### 1a. Create account at GitHub.com (if you don't have one)
- Go to https://github.com
- Sign up for free

### 1b. Create a new repository
- Click "New Repository" 
- Name: `peds-calculator`
- Description: "Pediatric Emergency Calculator - ETC Reference"
- Set to **Public** (so others can access it)
- Click "Create repository"

### 1c. Push your code to GitHub

In PowerShell, navigate to your project folder:
```powershell
cd c:\Users\joana\py_new\Peds
```

Initialize git and push:
```powershell
git init
git add .
git commit -m "Initial commit: Pediatric emergency calculator"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/peds-calculator.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## Step 2: Deploy to Render.com (FREE)

### 2a. Create Render Account
- Go to https://render.com
- Sign up with GitHub (easiest option)
- Click "Connect GitHub"
- Authorize & select your repository

### 2b. Create New Web Service
1. Click "New +" → "Web Service"
2. Search for `peds-calculator` repository
3. Click "Connect"

### 2c. Configure the Service
Fill in the settings:

| Setting | Value |
|---------|-------|
| **Name** | `peds-calculator` |
| **Environment** | Python 3.10 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Plan** | Free (starter) |

4. Click "Create Web Service"

### 2d. Wait for Deployment
- Render will automatically build and deploy
- Watch the logs - should take 2-3 minutes
- Your app will be live at: `https://peds-calculator.onrender.com` (or similar)

---

## Step 3: Share Your Live App

Once deployed, share the URL:
- **Live App**: https://peds-calculator.onrender.com
- **GitHub Code**: https://github.com/YOUR_USERNAME/peds-calculator

---

## Troubleshooting

### App won't deploy?
- Check the logs in Render dashboard
- Verify `Procfile` exists and has correct syntax
- Ensure all Python dependencies are in `requirements.txt`

### Getting 502 error?
- Wait a few minutes (cold start takes time on free tier)
- Check Render logs for errors
- Restart the service from Render dashboard

### Need to update the app?
- Make changes locally
- Push to GitHub: `git add . && git commit -m "Update" && git push`
- Render automatically redeploys!

---

## Free Tier Note

Render's free tier will:
- ✅ Work perfectly for your use case
- ✅ Auto-deploy on GitHub push
- ✅ Have ~30s response time after inactivity (cold start)
- ⚠️ Spin down after 15 minutes of inactivity

For production use, consider upgrading to a paid tier.

---

## Local Testing Before Deployment

To test locally before pushing:
```powershell
cd c:\Users\joana\py_new\Peds
venv\Scripts\activate
pip install -r requirements.txt
gunicorn app:app
```

Then visit: `http://localhost:8000`
