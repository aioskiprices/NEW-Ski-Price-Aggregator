import requests
from bs4 import BeautifulSoup

def get_ski_info(url):
    # Set headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # Fetch the webpage
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for request errors

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the price element
        price_element = soup.find('span', class_='money', attrs={'data-price': ''})
        price = price_element.text.strip() if price_element else "Price not found"

        # Find the image element (adjust selector based on the website's structure)
        image_element = soup.find('img', class_='product__image')  # Adjust class name as needed
        image_url = image_element['src'] if image_element else None
        
        # If the image URL is relative, make it absolute
        if image_url and not image_url.startswith(('http://', 'https://')):
            image_url = f"https://skipro.com{image_url}"

        return {
            'price': price,
            'image_url': image_url
        }

    except requests.RequestException as e:
        return {
            'price': f"Error fetching page: {e}",
            'image_url': None
        }

# List of Skipro product URLs (example)
urls = [
    "https://skipro.com/collections/all-mountain-skis/products/wingman-86-ti-flat-45w",
    "https://skipro.com/collections/all-mountain-skis/products/unleashed-98-flat-45w"
    # Add as many as you want
]

# Loop through each URL to get and print the info
for url in urls:
    info = get_ski_info(url)
    print(f"URL: {url}")
    print(f"Price: {info['price']}")
    print(f"Image URL: {info['image_url']}")
    print("---")
