"""
Quick test of Tesco scraper functionality
"""

def test_basic_functionality():
    """Test basic scraper functionality"""
    print("Testing Tesco Scraper...")
    print("=" * 40)
    
    try:
        # Test imports
        from tesco_scraper import TescoScraper, Product
        print("✅ Successfully imported TescoScraper and Product")
        
        # Test initialization
        scraper = TescoScraper(delay=1)
        print("✅ Successfully initialized scraper")
        
        # Test Product creation
        test_product = Product(
            name="Test Bread",
            price="£2.50",
            price_per_unit="£1.25 per loaf",
            image_url="https://example.com/bread.jpg",
            product_url="https://tesco.com/test",
            availability="Available",
            rating=4.5,
            review_count=100,
            description="Delicious bread",
            brand="Tesco"
        )
        print("✅ Successfully created Product instance")
        
        # Test save functions with mock data
        test_products = [test_product]
        scraper.save_to_csv(test_products, "test_products.csv")
        scraper.save_to_json(test_products, "test_products.json")
        print("✅ Successfully saved test data to CSV and JSON")
        
        print("\n🎉 Basic functionality test PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_connection():
    """Test connection to Tesco website"""
    print("\nTesting connection to Tesco...")
    print("=" * 40)
    
    try:
        import requests
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Test basic connection
        response = requests.get("https://www.tesco.com", headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Successfully connected to Tesco website")
            return True
        else:
            print(f"⚠️  Connection returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_search_functionality():
    """Test actual search functionality with limited scope"""
    print("\nTesting search functionality...")
    print("=" * 40)
    
    try:
        from tesco_scraper import TescoScraper
        
        scraper = TescoScraper(delay=1)
        
        # Try a very limited search
        print("Attempting search for 'milk' (limited to 1 page)...")
        products = scraper.search_products("milk", max_pages=1)
        
        if products:
            print(f"✅ Found {len(products)} products")
            
            # Show details of first product
            first_product = products[0]
            print(f"   First product: {first_product.name}")
            print(f"   Price: {first_product.price}")
            
            # Test saving actual results
            scraper.save_to_csv(products[:3], "actual_test_results.csv")
            print("✅ Saved actual results to CSV")
            
            return True
        else:
            print("⚠️  No products found - may need selector updates")
            return False
            
    except Exception as e:
        print(f"❌ Search test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("TESCO SCRAPER QUICK TEST")
    print("=" * 50)
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Connection Test", test_connection),
        ("Search Test", test_search_functionality)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Scraper is ready to use.")
    elif passed >= 2:
        print("⚠️  Most tests passed. Scraper should work with minor issues.")
        print("Try running: python examples.py")
    else:
        print("❌ Multiple tests failed. Check your setup.")
    
    print("\nFiles created during testing:")
    print("- test_products.csv/json (mock data)")
    if passed >= 2:
        print("- actual_test_results.csv (real data)")

if __name__ == "__main__":
    main()
