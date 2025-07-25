# Tesco Scraper Web App 🛒

A powerful web-based scraper for Tesco products with a beautiful, responsive interface.

## ✨ Features

- 🔍 **Smart Search**: Search for any product on Tesco
- 📊 **Real-time Progress**: Live progress tracking during scraping
- 💾 **Export Options**: Download results as CSV or JSON
- 📱 **Mobile Friendly**: Responsive design works on all devices
- 🖼️ **Product Cards**: Beautiful display with images and details
- ⚡ **Fast & Reliable**: Optimized scraping with error handling

## 🚀 Quick Deploy to Web

### Deploy to Render (Free & Easy)
1. Push your code to GitHub
2. Go to https://render.com
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. Your app will be live at: `https://your-app-name.onrender.com`

### Deploy to Railway
1. Go to https://railway.app
2. Click "Deploy from GitHub repo"
3. Select your repo - auto-deploys!

## 🛠️ Local Setup

**Run the Web UI:**
```bash
.\.venv\Scripts\python.exe launch_ui.py
```

**Or run examples:**
```bash
.\.venv\Scripts\python.exe examples.py
```

## 📖 Web Interface Usage

1. **Start the web app:** Run `launch_ui.py`
2. **Enter product name:** (e.g., "milk", "bread", "chocolate")
3. **Set pages to scrape:** (1-10)
4. **Click "Search Products"**
5. **Watch real-time progress**
6. **View results and download data**

## 📊 What You Get

- **Product names and prices**
- **Images and availability**
- **Brand information**
- **Price per unit**
- **Direct links to Tesco**
- **Downloadable CSV/JSON files**

## 🌐 Share Your Scraper Online

Once deployed, anyone can use your scraper by visiting your URL:
- **Example:** `https://tesco-scraper-abc123.onrender.com`
- **Mobile friendly** - works on phones and tablets
- **No installation needed** - just visit the website
- **Real-time results** - see progress as it scrapes

## 🚨 Important Notes

- ✅ Respects Tesco's rate limits
- ✅ Built-in delays between requests  
- ✅ For personal/educational use
- ❗ Check Tesco's Terms of Service
- ❗ Don't overwhelm their servers

## 📁 Files Created

- `web_ui.py` - Web interface
- `tesco_scraper.py` - Core scraper
- `launch_ui.py` - Local launcher
- `templates/index.html` - Beautiful web UI
- `Procfile` - Deployment config
- `requirements.txt` - Dependencies

**Made with ❤️ for easy web scraping**
