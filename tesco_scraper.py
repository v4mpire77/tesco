"""
Tesco Web Scraper
A comprehensive web scraper for extracting product data from Tesco's website.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
import re
from urllib.parse import urljoin, quote
from dataclasses import dataclass
from typing import List, Dict, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Product:
    """Data class to represent a Tesco product"""
    name: str
    price: str
    price_per_unit: Optional[str]
    image_url: Optional[str]
    product_url: str
    availability: str
    rating: Optional[float]
    review_count: Optional[int]
    description: Optional[str]
    brand: Optional[str]

class TescoScraper:
    """Main scraper class for Tesco website"""
    
    def __init__(self, delay=2):
        """
        Initialize the scraper
        Args:
            delay (int): Delay between requests in seconds to be respectful
        """
        self.base_url = "https://www.tesco.com"
        self.session = requests.Session()
        self.delay = delay
        
        # Set headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
    def search_products(self, query: str, max_pages: int = 5) -> List[Product]:
        """
        Search for products on Tesco website
        Args:
            query (str): Search term
            max_pages (int): Maximum number of pages to scrape
        Returns:
            List[Product]: List of scraped products
        """
        products = []
        
        for page in range(1, max_pages + 1):
            logger.info(f"Scraping page {page} for query: {query}")
            
            # Construct search URL
            search_url = f"{self.base_url}/groceries/en-GB/search?query={quote(query)}&page={page}"
            
            try:
                response = self.session.get(search_url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                page_products = self._parse_product_listing(soup)
                
                if not page_products:
                    logger.info(f"No more products found on page {page}")
                    break
                    
                products.extend(page_products)
                
                # Respectful delay
                time.sleep(self.delay)
                
            except requests.RequestException as e:
                logger.error(f"Error fetching page {page}: {e}")
                break
                
        return products
    
    def scrape_category(self, category_url: str, max_pages: int = 5) -> List[Product]:
        """
        Scrape products from a specific category
        Args:
            category_url (str): URL of the category page
            max_pages (int): Maximum number of pages to scrape
        Returns:
            List[Product]: List of scraped products
        """
        products = []
        
        for page in range(1, max_pages + 1):
            logger.info(f"Scraping category page {page}")
            
            # Add page parameter to URL
            page_url = f"{category_url}?page={page}"
            
            try:
                response = self.session.get(page_url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                page_products = self._parse_product_listing(soup)
                
                if not page_products:
                    break
                    
                products.extend(page_products)
                time.sleep(self.delay)
                
            except requests.RequestException as e:
                logger.error(f"Error fetching category page {page}: {e}")
                break
                
        return products
    
    def _parse_product_listing(self, soup: BeautifulSoup) -> List[Product]:
        """
        Parse product information from a listing page
        Args:
            soup (BeautifulSoup): Parsed HTML content
        Returns:
            List[Product]: List of parsed products
        """
        products = []
        
        # Common selectors for Tesco product tiles (these may need updating)
        product_selectors = [
            '.product-tile',
            '[data-auto="product-tile"]',
            '.product-list--list-item',
            '.beans-tile'
        ]
        
        product_elements = []
        for selector in product_selectors:
            elements = soup.select(selector)
            if elements:
                product_elements = elements
                break
        
        for element in product_elements:
            try:
                product = self._extract_product_data(element)
                if product:
                    products.append(product)
            except Exception as e:
                logger.warning(f"Error parsing product: {e}")
                continue
                
        return products
    
    def _extract_product_data(self, element) -> Optional[Product]:
        """
        Extract product data from a single product element
        Args:
            element: BeautifulSoup element containing product data
        Returns:
            Optional[Product]: Parsed product or None if parsing fails
        """
        try:
            # Extract product name
            name_selectors = [
                '.product-tile--title',
                '[data-auto="product-tile-title"]',
                '.product-details--content h3',
                'h3 a'
            ]
            name = self._get_text_by_selectors(element, name_selectors)
            
            if not name:
                return None
            
            # Extract price
            price_selectors = [
                '.product-tile--price',
                '[data-auto="price-current"]',
                '.price-current',
                '.beans-price__text'
            ]
            price = self._get_text_by_selectors(element, price_selectors)
            
            # Extract price per unit
            unit_price_selectors = [
                '.product-tile--price-per-unit',
                '[data-auto="price-per-quantity-weight"]',
                '.price-per-unit'
            ]
            price_per_unit = self._get_text_by_selectors(element, unit_price_selectors)
            
            # Extract product URL
            link_selectors = [
                'a[href*="/groceries/"]',
                '.product-tile--title a',
                'h3 a'
            ]
            product_link = None
            for selector in link_selectors:
                link_element = element.select_one(selector)
                if link_element and link_element.get('href'):
                    product_link = urljoin(self.base_url, link_element.get('href'))
                    break
            
            # Extract image URL
            img_selectors = [
                '.product-tile--image img',
                'img[src*="digitalcontent"]',
                '.product-image img'
            ]
            image_url = None
            for selector in img_selectors:
                img_element = element.select_one(selector)
                if img_element and img_element.get('src'):
                    image_url = img_element.get('src')
                    break
            
            # Extract availability
            availability_selectors = [
                '.product-tile--availability',
                '[data-auto="availability"]',
                '.availability-text'
            ]
            availability = self._get_text_by_selectors(element, availability_selectors) or "Available"
            
            # Extract brand (if available)
            brand_selectors = [
                '.product-tile--brand',
                '[data-auto="brand"]',
                '.brand-name'
            ]
            brand = self._get_text_by_selectors(element, brand_selectors)
            
            return Product(
                name=name.strip(),
                price=price.strip() if price else "N/A",
                price_per_unit=price_per_unit.strip() if price_per_unit else None,
                image_url=image_url,
                product_url=product_link or "",
                availability=availability.strip(),
                rating=None,  # Would need to parse rating if available
                review_count=None,  # Would need to parse review count if available
                description=None,  # Would need separate request to product page
                brand=brand.strip() if brand else None
            )
            
        except Exception as e:
            logger.warning(f"Error extracting product data: {e}")
            return None
    
    def _get_text_by_selectors(self, element, selectors: List[str]) -> Optional[str]:
        """
        Try multiple CSS selectors to find text content
        Args:
            element: BeautifulSoup element to search in
            selectors: List of CSS selectors to try
        Returns:
            Optional[str]: Found text or None
        """
        for selector in selectors:
            found_element = element.select_one(selector)
            if found_element:
                text = found_element.get_text(strip=True)
                if text:
                    return text
        return None
    
    def get_product_details(self, product_url: str) -> Dict:
        """
        Get detailed information for a specific product
        Args:
            product_url (str): URL of the product page
        Returns:
            Dict: Detailed product information
        """
        try:
            response = self.session.get(product_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract detailed information
            details = {
                'description': self._get_text_by_selectors(soup, ['.product-description', '.product-details']),
                'ingredients': self._get_text_by_selectors(soup, ['.ingredients', '.product-ingredients']),
                'nutrition': self._extract_nutrition_info(soup),
                'reviews': self._extract_review_info(soup)
            }
            
            time.sleep(self.delay)
            return details
            
        except requests.RequestException as e:
            logger.error(f"Error fetching product details: {e}")
            return {}
    
    def _extract_nutrition_info(self, soup: BeautifulSoup) -> Dict:
        """Extract nutrition information if available"""
        nutrition = {}
        nutrition_table = soup.select_one('.nutrition-table, .nutritional-information')
        
        if nutrition_table:
            rows = nutrition_table.select('tr')
            for row in rows:
                cells = row.select('td, th')
                if len(cells) >= 2:
                    key = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True)
                    nutrition[key] = value
                    
        return nutrition
    
    def _extract_review_info(self, soup: BeautifulSoup) -> Dict:
        """Extract review information if available"""
        reviews = {
            'rating': None,
            'review_count': None
        }
        
        # Try to find rating
        rating_element = soup.select_one('[data-rating], .star-rating, .rating-value')
        if rating_element:
            rating_text = rating_element.get_text(strip=True)
            rating_match = re.search(r'(\d+\.?\d*)', rating_text)
            if rating_match:
                reviews['rating'] = float(rating_match.group(1))
        
        # Try to find review count
        review_count_element = soup.select_one('.review-count, [data-review-count]')
        if review_count_element:
            count_text = review_count_element.get_text(strip=True)
            count_match = re.search(r'(\d+)', count_text)
            if count_match:
                reviews['review_count'] = int(count_match.group(1))
        
        return reviews
    
    def save_to_csv(self, products: List[Product], filename: str):
        """
        Save products to CSV file
        Args:
            products (List[Product]): List of products to save
            filename (str): Output filename
        """
        if not products:
            logger.warning("No products to save")
            return
        
        # Convert products to dictionaries
        product_dicts = []
        for product in products:
            product_dict = {
                'name': product.name,
                'price': product.price,
                'price_per_unit': product.price_per_unit,
                'image_url': product.image_url,
                'product_url': product.product_url,
                'availability': product.availability,
                'rating': product.rating,
                'review_count': product.review_count,
                'description': product.description,
                'brand': product.brand
            }
            product_dicts.append(product_dict)
        
        # Create DataFrame and save to CSV
        df = pd.DataFrame(product_dicts)
        df.to_csv(filename, index=False, encoding='utf-8')
        logger.info(f"Saved {len(products)} products to {filename}")
    
    def save_to_json(self, products: List[Product], filename: str):
        """
        Save products to JSON file
        Args:
            products (List[Product]): List of products to save
            filename (str): Output filename
        """
        if not products:
            logger.warning("No products to save")
            return
        
        # Convert products to dictionaries
        product_dicts = []
        for product in products:
            product_dict = {
                'name': product.name,
                'price': product.price,
                'price_per_unit': product.price_per_unit,
                'image_url': product.image_url,
                'product_url': product.product_url,
                'availability': product.availability,
                'rating': product.rating,
                'review_count': product.review_count,
                'description': product.description,
                'brand': product.brand
            }
            product_dicts.append(product_dict)
        
        # Save to JSON
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(product_dicts, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(products)} products to {filename}")


def main():
    """Example usage of the Tesco scraper"""
    
    # Initialize scraper
    scraper = TescoScraper(delay=2)
    
    # Example 1: Search for products
    print("Searching for 'bread' products...")
    bread_products = scraper.search_products("bread", max_pages=2)
    print(f"Found {len(bread_products)} bread products")
    
    # Save results
    if bread_products:
        scraper.save_to_csv(bread_products, "tesco_bread_products.csv")
        scraper.save_to_json(bread_products, "tesco_bread_products.json")
        
        # Print first few products
        for i, product in enumerate(bread_products[:5]):
            print(f"\n{i+1}. {product.name}")
            print(f"   Price: {product.price}")
            print(f"   URL: {product.product_url}")
    
    # Example 2: Get detailed information for a specific product
    if bread_products:
        first_product = bread_products[0]
        if first_product.product_url:
            print(f"\nGetting detailed information for: {first_product.name}")
            details = scraper.get_product_details(first_product.product_url)
            print(f"Details: {details}")


if __name__ == "__main__":
    main()
