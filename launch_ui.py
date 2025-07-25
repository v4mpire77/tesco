"""
Launch the Tesco Scraper Web UI
"""

import webbrowser
import time
import threading
from web_ui import app

def open_browser():
    """Open browser after a short delay"""
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("🚀 Starting Tesco Scraper Web UI...")
    print("📱 Opening browser in 2 seconds...")
    print("🌐 URL: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Open browser in background
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start Flask app
    app.run(debug=False, host='0.0.0.0', port=5000)
