from tesco_scraper import TescoScraper

# Initialize the scraper
scraper = TescoScraper(delay=1)  # 1 second delay between requests

# Search for what you want
search_term = input("What product do you want to search for? ")
print(f"Searching for '{search_term}'...")

# Get products
products = scraper.search_products(search_term, max_pages=2)

print(f"Found {len(products)} products!")

# Show first 10 results
for i, product in enumerate(products[:10]):
    print(f"\n{i+1}. {product.name}")
    print(f"   Price: {product.price}")
    print(f"   Brand: {product.brand or 'N/A'}")
    print(f"   Available: {product.availability}")

# Save results
if products:
    filename = f"{search_term.replace(' ', '_')}_products"
    scraper.save_to_csv(products, f"{filename}.csv")
    scraper.save_to_json(products, f"{filename}.json")
    print(f"\nSaved results to {filename}.csv and {filename}.json")
else:
    print("No products found!")
