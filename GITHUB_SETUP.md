# Quick GitHub Setup Commands

If you prefer to use command line instead of the script:

## 1. Initialize Git (if not done)
```bash
git init
```

## 2. Add files
```bash
git add .
git commit -m "Initial commit: Tesco Web Scraper with UI"
```

## 3. Create GitHub repository
- Go to https://github.com/new
- Repository name: `tesco-scraper`
- Make it **Public** (required for free deployments)
- **Don't** initialize with README
- Click "Create repository"

## 4. Connect and push
```bash
git remote add origin https://github.com/YOURUSERNAME/tesco-scraper.git
git branch -M main
git push -u origin main
```

## 5. Deploy online (Free options)

### Render (Recommended)
1. Go to https://render.com
2. "New +" → "Web Service"
3. Connect GitHub → Select your repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `python web_ui.py`
6. Deploy!

### Railway
1. Go to https://railway.app
2. "Deploy from GitHub repo"
3. Select your repo
4. Auto-deploys!

### Vercel
1. Go to https://vercel.com
2. "New Project" → Import GitHub repo
3. Auto-detects and deploys!

## Your live app will be at:
- `https://your-app-name.onrender.com`
- `https://your-app-name.up.railway.app`
- `https://your-app-name.vercel.app`

## Share your creation! 🎉
