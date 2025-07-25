"""
Simple usage examples for the Tesco scraper
"""

from tesco_scraper import TescoScraper
import json

def search_example():
    """Example of searching for products"""
    print("=== TESCO SCRAPER - SEARCH EXAMPLE ===\n")
    
    # Initialize scraper
    scraper = TescoScraper(delay=1)  # 1 second delay between requests
    
    # Search for products
    search_terms = ["milk", "bread", "bananas"]
    
    for term in search_terms:
        print(f"Searching for '{term}'...")
        products = scraper.search_products(term, max_pages=2)
        
        print(f"Found {len(products)} products for '{term}'\n")
        
        # Display first 3 products
        for i, product in enumerate(products[:3]):
            print(f"  {i+1}. {product.name}")
            print(f"     Price: {product.price}")
            print(f"     Brand: {product.brand or 'N/A'}")
            print(f"     Available: {product.availability}")
            print()
        
        # Save results
        if products:
            filename = f"tesco_{term.replace(' ', '_')}_products"
            scraper.save_to_csv(products, f"{filename}.csv")
            scraper.save_to_json(products, f"{filename}.json")
            print(f"Results saved to {filename}.csv and {filename}.json\n")
        
        print("-" * 50)

def category_example():
    """Example of scraping from a category URL"""
    print("=== TESCO SCRAPER - CATEGORY EXAMPLE ===\n")
    
    scraper = TescoScraper(delay=1)
    
    # Example category URLs (these would need to be updated with real Tesco URLs)
    example_categories = {
        "Fresh Food": "https://www.tesco.com/groceries/en-GB/shop/fresh-food",
        "Bakery": "https://www.tesco.com/groceries/en-GB/shop/fresh-food/bakery"
    }
    
    for category_name, category_url in example_categories.items():
        print(f"Scraping category: {category_name}")
        print(f"URL: {category_url}")
        
        try:
            products = scraper.scrape_category(category_url, max_pages=1)
            print(f"Found {len(products)} products in {category_name}\n")
            
            # Display first 3 products
            for i, product in enumerate(products[:3]):
                print(f"  {i+1}. {product.name}")
                print(f"     Price: {product.price}")
                print()
                
        except Exception as e:
            print(f"Error scraping {category_name}: {e}\n")
        
        print("-" * 50)

def detailed_product_example():
    """Example of getting detailed product information"""
    print("=== TESCO SCRAPER - DETAILED PRODUCT EXAMPLE ===\n")
    
    scraper = TescoScraper(delay=1)
    
    # First, search for a product
    products = scraper.search_products("organic milk", max_pages=1)
    
    if products:
        product = products[0]
        print(f"Getting detailed information for: {product.name}")
        print(f"Product URL: {product.product_url}\n")
        
        if product.product_url:
            details = scraper.get_product_details(product.product_url)
            
            print("Product Details:")
            print(f"Description: {details.get('description', 'N/A')}")
            print(f"Ingredients: {details.get('ingredients', 'N/A')}")
            
            if details.get('nutrition'):
                print("\nNutrition Information:")
                for key, value in details['nutrition'].items():
                    print(f"  {key}: {value}")
            
            if details.get('reviews'):
                print(f"\nRating: {details['reviews'].get('rating', 'N/A')}")
                print(f"Review Count: {details['reviews'].get('review_count', 'N/A')}")
    else:
        print("No products found for detailed analysis")

def custom_search_with_filters():
    """Example of custom search with specific requirements"""
    print("=== TESCO SCRAPER - CUSTOM SEARCH EXAMPLE ===\n")
    
    scraper = TescoScraper(delay=1)
    
    # Search for products and filter results
    search_term = "chocolate"
    products = scraper.search_products(search_term, max_pages=3)
    
    # Filter products by price (example: under £5)
    affordable_products = []
    for product in products:
        # Extract numeric price (basic example)
        price_str = product.price.replace('£', '').replace(',', '')
        try:
            price_value = float(price_str.split()[0])  # Get first number
            if price_value < 5.0:
                affordable_products.append(product)
        except (ValueError, IndexError):
            continue
    
    print(f"Found {len(products)} total chocolate products")
    print(f"Found {len(affordable_products)} chocolate products under £5\n")
    
    # Display affordable products
    for i, product in enumerate(affordable_products[:10]):
        print(f"  {i+1}. {product.name}")
        print(f"     Price: {product.price}")
        print(f"     Brand: {product.brand or 'N/A'}")
        print()
    
    # Save filtered results
    if affordable_products:
        scraper.save_to_csv(affordable_products, "affordable_chocolate.csv")
        print("Affordable chocolate products saved to affordable_chocolate.csv")

def main():
    """Run all examples"""
    print("TESCO WEB SCRAPER EXAMPLES")
    print("=" * 50)
    print()
    
    try:
        # Run examples
        search_example()
        print("\n" + "=" * 50 + "\n")
        
        # category_example()  # Uncomment if you have valid category URLs
        # print("\n" + "=" * 50 + "\n")
        
        detailed_product_example()
        print("\n" + "=" * 50 + "\n")
        
        custom_search_with_filters()
        
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    print("\nScraping examples completed!")

if __name__ == "__main__":
    main()
