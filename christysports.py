import requests
from bs4 import BeautifulSoup

def get_ski_info_christysports(url):
    """
    Scrapes the product name and price from a Christy Sports product page.

    Args:
        url (str): The URL of the Christy Sports product page.

    Returns:
        dict: A dictionary with keys:
            - "name" (str or None): The product name or a fallback string if not found.
            - "price" (str or None): The product price or a fallback string if not found.
            - "error" (str, optional): An error message if something goes wrong.
    """
    try:
        headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/91.0.4472.124 Safari/537.36'
            )
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return {
                "name": None,
                "price": None,
                "error": f"Failed to fetch webpage. Status code: {response.status_code}"
            }

        soup = BeautifulSoup(response.content, 'html.parser')

        # ----- 1) Product name -----
        # Looks for: <h1 class="product-name hidden-sm-down">...</h1>
        name_element = soup.select_one('h1.product-name.hidden-sm-down')
        product_name = name_element.get_text(strip=True) if name_element else "Name not found"

        # ----- 2) Price -----
        # One CSS selector to find either:
        #   1) Discounted price => .price .sales .value
        #   2) No discount price => .no-discount-price span
        price_element = soup.select_one('.price .sales .value, .no-discount-price span')
        price = price_element.get_text(strip=True) if price_element else "Price not found"

        return {
            "name": product_name,
            "price": price
        }

    except Exception as e:
        return {
            "name": None,
            "price": None,
            "error": str(e)
        } 