"""
Test script for Tesco scraper to validate functionality
"""

import requests
from bs4 import BeautifulSoup
import time

def test_connection():
    """Test if we can connect to Tesco website"""
    print("Testing connection to Tesco website...")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get("https://www.tesco.com", headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Successfully connected to Tesco website")
            return True
        else:
            print(f"❌ Connection failed with status code: {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False

def test_search_page():
    """Test if we can access the search page"""
    print("\nTesting search page access...")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        search_url = "https://www.tesco.com/groceries/en-GB/search?query=milk"
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Successfully accessed search page")
            
            # Try to parse with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for common product-related elements
            potential_selectors = [
                '.product-tile',
                '[data-auto="product-tile"]',
                '.product-list--list-item',
                '.beans-tile',
                '[class*="product"]',
                '[data-testid*="product"]'
            ]
            
            found_elements = []
            for selector in potential_selectors:
                elements = soup.select(selector)
                if elements:
                    found_elements.append(f"{selector}: {len(elements)} elements")
            
            if found_elements:
                print("✅ Found potential product elements:")
                for element in found_elements[:5]:  # Show first 5
                    print(f"   - {element}")
            else:
                print("⚠️  No obvious product elements found - selectors may need updating")
            
            return True
        else:
            print(f"❌ Search page access failed with status code: {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Search page error: {e}")
        return False

def analyze_page_structure():
    """Analyze the page structure to help identify selectors"""
    print("\nAnalyzing page structure for selector identification...")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        search_url = "https://www.tesco.com/groceries/en-GB/search?query=bread"
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for elements that might contain product information
            print("Looking for common e-commerce patterns...")
            
            # Check for price patterns
            price_patterns = ['£', 'price', 'cost', 'GBP']
            price_elements = []
            for pattern in price_patterns:
                elements = soup.find_all(text=lambda text: text and pattern in text)
                if elements:
                    price_elements.extend(elements[:3])  # Take first 3
            
            if price_elements:
                print("✅ Found price-related text:")
                for element in price_elements[:3]:
                    print(f"   - {element.strip()}")
            
            # Check for common class names
            all_classes = []
            for element in soup.find_all(class_=True):
                all_classes.extend(element.get('class'))
            
            # Look for product-related class names
            product_classes = [cls for cls in set(all_classes) if 
                             any(keyword in cls.lower() for keyword in 
                                 ['product', 'tile', 'item', 'card', 'bean'])]
            
            if product_classes:
                print("✅ Found potential product-related classes:")
                for cls in product_classes[:10]:  # Show first 10
                    print(f"   - .{cls}")
            
            # Check for data attributes
            data_attrs = []
            for element in soup.find_all(lambda tag: any(attr.startswith('data-') for attr in tag.attrs)):
                for attr in element.attrs:
                    if attr.startswith('data-') and 'product' in attr.lower():
                        data_attrs.append(f"{attr}=\"{element.attrs[attr]}\"")
            
            if data_attrs:
                print("✅ Found product-related data attributes:")
                for attr in list(set(data_attrs))[:5]:  # Show first 5 unique
                    print(f"   - [{attr}]")
            
            return True
        else:
            print(f"❌ Page analysis failed with status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Page analysis error: {e}")
        return False

def test_scraper_imports():
    """Test if our scraper can be imported and initialized"""
    print("\nTesting scraper imports and initialization...")
    
    try:
        from tesco_scraper import TescoScraper, Product
        print("✅ Successfully imported TescoScraper and Product classes")
        
        # Try to initialize
        scraper = TescoScraper(delay=1)
        print("✅ Successfully initialized TescoScraper")
        
        # Test Product creation
        test_product = Product(
            name="Test Product",
            price="£1.99",
            price_per_unit="99p per 100g",
            image_url="https://example.com/image.jpg",
            product_url="https://example.com/product",
            availability="Available",
            rating=4.5,
            review_count=123,
            description="Test description",
            brand="Test Brand"
        )
        print("✅ Successfully created test Product instance")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return False

def run_quick_test():
    """Run a quick test of the scraper with minimal requests"""
    print("\nRunning quick scraper test...")
    
    try:
        from tesco_scraper import TescoScraper
        
        scraper = TescoScraper(delay=2)
        
        # Try a very limited search
        print("Attempting to search for 'milk' (1 page only)...")
        products = scraper.search_products("milk", max_pages=1)
        
        if products:
            print(f"✅ Successfully found {len(products)} products")
            
            # Show first product details
            first_product = products[0]
            print(f"First product: {first_product.name}")
            print(f"Price: {first_product.price}")
            print(f"URL: {first_product.product_url}")
            
            # Test saving functionality
            try:
                scraper.save_to_csv(products[:3], "test_output.csv")
                print("✅ Successfully saved to CSV")
            except Exception as e:
                print(f"⚠️  CSV save error: {e}")
            
            try:
                scraper.save_to_json(products[:3], "test_output.json")
                print("✅ Successfully saved to JSON")
            except Exception as e:
                print(f"⚠️  JSON save error: {e}")
            
            return True
        else:
            print("⚠️  No products found - selectors may need updating")
            return False
            
    except Exception as e:
        print(f"❌ Quick test error: {e}")
        return False

def main():
    """Run all tests"""
    print("TESCO SCRAPER TEST SUITE")
    print("=" * 50)
    
    tests = [
        test_connection,
        test_search_page,
        analyze_page_structure,
        test_scraper_imports,
        run_quick_test
    ]
    
    results = []
    
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
        
        print()  # Add spacing between tests
        time.sleep(1)  # Small delay between tests
    
    # Summary
    print("=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The scraper should work correctly.")
    elif passed >= total * 0.7:  # 70% or more
        print("⚠️  Most tests passed. The scraper should work with minor issues.")
    else:
        print("❌ Several tests failed. The scraper may need significant updates.")
    
    print("\nNext steps:")
    if passed < total:
        print("- Check the failed tests above")
        print("- Update CSS selectors in config.json if needed")
        print("- Verify Tesco website accessibility")
    print("- Run 'python examples.py' to try the scraper")
    print("- Check the generated output files")

if __name__ == "__main__":
    main()
