import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to fetch and parse the web page
def fetch_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve page with status code {response.status_code}")
        return None
    return BeautifulSoup(response.content, 'html.parser')

# Function to extract product data from the page
def extract_product_info(soup):
    products = []
    # Find all product containers
    product_containers = soup.select('.product_pod')
    
    for container in product_containers:
        name = container.select_one('h3 a').get('title')
        price = container.select_one('.price_color').get_text(strip=True)
        rating = container.select_one('p')['class'][1]  # Ratings are given as class names
        
        products.append({
            'Name': name,
            'Price': price,
            'Rating': rating
        })
    
    return products

# Function to save product data to a CSV file
def save_to_csv(products, filename):
    df = pd.DataFrame(products)
    df.to_csv(filename, index=False)

def main():
    url = 'https://books.toscrape.com/'
    soup = fetch_page(url)
    
    if soup:
        products = extract_product_info(soup)
        save_to_csv(products, 'books.csv')
        print("Product information has been saved to 'books.csv'.")

if __name__ == '__main__':
    main()
