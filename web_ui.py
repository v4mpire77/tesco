"""
Simple Web UI for Tesco Scraper
A Flask web interface to make scraping easier
"""

from flask import Flask, render_template, request, jsonify, send_file
from tesco_scraper import TescoScraper
import os
import json
from datetime import datetime
import threading

app = Flask(__name__)

# Global variables to track scraping status
scraping_status = {
    'is_running': False,
    'progress': 0,
    'message': '',
    'results': [],
    'error': None
}

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_products():
    """Start product search"""
    global scraping_status
    
    if scraping_status['is_running']:
        return jsonify({'error': 'Scraping already in progress'}), 400
    
    data = request.get_json()
    search_term = data.get('search_term', '').strip()
    max_pages = int(data.get('max_pages', 2))
    
    if not search_term:
        return jsonify({'error': 'Search term is required'}), 400
    
    # Reset status
    scraping_status.update({
        'is_running': True,
        'progress': 0,
        'message': f'Starting search for "{search_term}"...',
        'results': [],
        'error': None
    })
    
    # Start scraping in background thread
    thread = threading.Thread(target=scrape_products, args=(search_term, max_pages))
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': 'Search started', 'status': 'started'})

def scrape_products(search_term, max_pages):
    """Background function to scrape products"""
    global scraping_status
    
    try:
        scraper = TescoScraper(delay=1)
        
        scraping_status['message'] = f'Searching for "{search_term}"...'
        scraping_status['progress'] = 10
        
        products = scraper.search_products(search_term, max_pages=max_pages)
        
        scraping_status['progress'] = 80
        scraping_status['message'] = f'Found {len(products)} products, saving results...'
        
        # Convert products to dictionaries for JSON
        results = []
        for product in products:
            results.append({
                'name': product.name,
                'price': product.price,
                'price_per_unit': product.price_per_unit,
                'image_url': product.image_url,
                'product_url': product.product_url,
                'availability': product.availability,
                'brand': product.brand or 'N/A'
            })
        
        # Save to files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{search_term.replace(' ', '_')}_{timestamp}"
        
        scraper.save_to_csv(products, f"static/downloads/{filename}.csv")
        scraper.save_to_json(products, f"static/downloads/{filename}.json")
        
        scraping_status.update({
            'is_running': False,
            'progress': 100,
            'message': f'Search completed! Found {len(products)} products.',
            'results': results,
            'csv_file': f"{filename}.csv",
            'json_file': f"{filename}.json"
        })
        
    except Exception as e:
        scraping_status.update({
            'is_running': False,
            'progress': 0,
            'message': 'Search failed',
            'error': str(e),
            'results': []
        })

@app.route('/status')
def get_status():
    """Get current scraping status"""
    return jsonify(scraping_status)

@app.route('/download/<filename>')
def download_file(filename):
    """Download results file"""
    file_path = os.path.join('static', 'downloads', filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'}), 404

@app.route('/clear')
def clear_results():
    """Clear current results"""
    global scraping_status
    if not scraping_status['is_running']:
        scraping_status.update({
            'progress': 0,
            'message': '',
            'results': [],
            'error': None
        })
    return jsonify({'message': 'Results cleared'})

# Create necessary directories
os.makedirs('static/downloads', exist_ok=True)
os.makedirs('templates', exist_ok=True)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print("Starting Tesco Scraper Web UI...")
    print(f"Running on port: {port}")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
