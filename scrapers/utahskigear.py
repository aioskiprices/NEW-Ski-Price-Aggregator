import requests
from bs4 import BeautifulSoup
import json

def get_ski_info_utahskigear(url):
    """
    Scrapes the product name and price from a Utah Ski Gear product page.

    Args:
        url (str): The URL of the Utah Ski Gear product page.

    Returns:
        dict: A dictionary with keys:
            - "name" (str or None): The product name or a fallback string if not found.
            - "price" (str or None): The product price or a fallback string if not found.
            - "error" (str, optional): An error message if something goes wrong.
    """
    try:
        headers = {
            'User-Agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/114.0.0.0 Safari/537.36'
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
        name_element = soup.find('h2', class_='product-single__title')
        product_name = name_element.get_text(strip=True) if name_element else "Name not found"

        # ----- 2) Price -----
        price_element = soup.find('span', {'data-product-price': True})
        price = price_element.get_text(strip=True) if price_element else "Price not found"

        # ----- 3) Update JSON file with new name if found -----
        if product_name != "Name not found":
            try:
                with open('ski_prices.json', 'r') as file:
                    data = json.load(file)
                
                # Find and update the ski name for this URL
                for ski in data['skis']:
                    if ski['site_name'] == 'Utah Ski Gear' and ski['site_url'] == url:
                        ski['ski_name'] = product_name
                        break
                
                # Write the updated data back to the JSON file
                with open('ski_prices.json', 'w') as file:
                    json.dump(data, file, indent=4)
            except Exception as e:
                print(f"Error updating ski name in JSON: {str(e)}")

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