import requests
from bs4 import BeautifulSoup
import json

def get_ski_info_evo(url):
    """
    Scrapes the product name and price from an Evo product page using structured data.

    Args:
        url (str): The URL of the Evo product page.

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

        product_name = "Name not found"
        price = "Price not found"
        
        # EVO includes structured data in script tags of type application/ld+json
        # We look for the Product object and extract name & price from there.
        script_tags = soup.find_all('script', type='application/ld+json')
        
        for tag in script_tags:
            try:
                data = json.loads(tag.string)
                
                # data can be a dict or a list of dicts, so handle both
                if isinstance(data, list):
                    for obj in data:
                        if isinstance(obj, dict) and obj.get("@type") == "Product":
                            product_name = obj.get("name", product_name)
                            offers = obj.get("offers", {})
                            # A single or multiple offers – handle whichever is present
                            if isinstance(offers, dict):
                                price = offers.get("price", price)
                            elif isinstance(offers, list) and len(offers) > 0:
                                price = offers[0].get("price", price)
                            break
                elif isinstance(data, dict) and data.get("@type") == "Product":
                    product_name = data.get("name", product_name)
                    offers = data.get("offers", {})
                    if isinstance(offers, dict):
                        price = offers.get("price", price)
                    elif isinstance(offers, list) and len(offers) > 0:
                        price = offers[0].get("price", price)
                
            except (json.JSONDecodeError, TypeError):
                continue
        
        # Format price with dollar sign if it's a number
        if price != "Price not found":
            try:
                price = f"${float(price):.2f}"
            except (ValueError, TypeError):
                pass

        # ----- 3) Update JSON file with new name if found -----
        if product_name != "Name not found":
            try:
                with open('ski_prices.json', 'r') as file:
                    data = json.load(file)
                
                # Find and update the ski name for this URL
                for ski in data['skis']:
                    if ski['site_name'] == 'Evo' and ski['site_url'] == url:
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