import requests
from bs4 import BeautifulSoup

def get_ski_price(url):
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

        # Find the price element based on the provided HTML
        price_element = soup.find('span', class_='money', attrs={'data-price': ''})

        if price_element:
            # The price is already in the "$X,XXX.XX" format
            return price_element.text.strip()
        else:
            return "Price element not found"

    except requests.RequestException as e:
        return f"Error fetching page: {e}"


# List of Skipro product URLs (example)
urls = [
    "https://skipro.com/collections/all-mountain-skis/products/wingman-86-ti-flat-45w",
    "https://skipro.com/collections/all-mountain-skis/products/unleashed-98-flat-45w"
    # Add as many as you want
]

# Loop through each URL to get and print the price
for url in urls:
    price = get_ski_price(url)
    print(f"Price at {url} is: {price}")
