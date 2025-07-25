# Tesco Scraper - Deploy to Web

## Quick Deploy Options

### 1. Render (Recommended - Free)
- ✅ Free hosting
- ✅ Automatic deployments from GitHub
- ✅ Custom domain support

### 2. Railway
- ✅ Free tier available
- ✅ Easy deployment
- ✅ Built-in database

### 3. Heroku
- ✅ Popular platform
- ✅ Easy scaling
- ⚠️ No longer free but affordable

## Step-by-Step Deployment

### Option 1: Deploy to Render (Free)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Use these settings:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `python web_ui.py`
     - **Environment:** Python 3

3. **Your app will be live at:** `https://your-app-name.onrender.com`

### Option 2: Deploy to Railway

1. **Push to GitHub** (same as above)

2. **Deploy on Railway:**
   - Go to https://railway.app
   - Click "Deploy from GitHub repo"
   - Select your repo
   - Railway auto-detects Python and deploys!

### Option 3: One-Click Deploy

Use the deploy buttons in your README:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## Environment Variables

For production, set these environment variables:
- `FLASK_ENV=production`
- `PORT=5000` (usually auto-set by hosting platform)

## Production Ready Features

Your scraper includes:
- ✅ Error handling
- ✅ Rate limiting (delays between requests)
- ✅ Responsive web design
- ✅ File downloads
- ✅ Progress tracking
- ✅ Mobile-friendly interface

## Sharing Your App

Once deployed, you can share your scraper with:
- **Direct URL:** `https://your-app-name.onrender.com`
- **QR Code:** Generate one for mobile access
- **Embed:** Use iframe in other websites

## Custom Domain (Optional)

Most platforms support custom domains:
- Buy domain (e.g., from Namecheap, GoDaddy)
- Add CNAME record pointing to your hosting platform
- Configure in hosting platform settings

## Security Notes

- The scraper respects Tesco's robots.txt
- Includes appropriate delays between requests
- No data is stored permanently on server
- Users download their own results
