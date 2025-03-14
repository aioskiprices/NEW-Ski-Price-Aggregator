import requests
from bs4 import BeautifulSoup
import json


def get_ski_info(url):
    """
    Scrapes the product name and price from an Untracked product page.

    Args:
        url (str): The URL of the Untracked product page.

    Returns:
        dict: A dictionary with keys:
            - "name" (str or None): The product name or a fallback string if not found.
            - "price" (str or None): The product price or a fallback string if not found.
            - "error" (str, optional): An error message if something goes wrong.
    """
    try:
        # Set headers to mimic a browser request
        headers = {
            'User-Agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/114.0.0.0 Safari/537.36'
            )
        }

        # Make the request to the website
        response = requests.get(url, headers=headers)

        # Check if request was successful
        if response.status_code != 200:
            return {
                "name": None,
                "price": None,
                "error": f"Failed to fetch webpage. Status code: {response.status_code}"
            }

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # ---------- 1) Get the product name ----------
        name_element = soup.find('h1', class_='product-name')
        if not name_element:
            # Fallback if the above fails
            name_element = soup.find('div', class_='headers')

        if name_element:
            product_name = name_element.get_text(strip=True)
        else:
            product_name = "Name not found"

        # ---------- 2) Get the price ----------
        # Find the price container div
        price_container = soup.find('div', class_='priceCompareFloatRight')
        if price_container:
            # Find the ourPrice span that contains the price
            our_price_span = price_container.find('span', class_='ourPrice')
            if our_price_span:
                # Find the span with class starting with 'minPriceForPID-' inside ourPrice
                price_element = our_price_span.find(
                    'span',
                    class_=lambda x: x and x.startswith('minPriceForPID-'))
                if price_element:
                    # Get the text and add the dollar sign
                    price = '$' + price_element.get_text(strip=True)
                else:
                    price = "Price span not found within ourPrice"
            else:
                price = "ourPrice span not found within priceCompareFloatRight"
        else:
            price = "Price container div not found"

        # ----- 3) Update JSON file with new name if found -----
        if product_name != "Name not found":
            try:
                with open('ski_prices.json', 'r') as file:
                    data = json.load(file)
                
                # Find and update the ski name for this URL
                for ski in data['skis']:
                    if ski['site_name'] == 'Untracked' and ski['site_url'] == url:
                        ski['ski_name'] = product_name
                        break
                
                # Write the updated data back to the JSON file
                with open('ski_prices.json', 'w') as file:
                    json.dump(data, file, indent=4)
            except Exception as e:
                print(f"Error updating ski name in JSON: {str(e)}")

        # Return both in a dictionary for clarity
        return {"name": product_name, "price": price}

    except Exception as e:
        return {"name": None, "price": None, "error": str(e)}


# Example usage
urls = [
   
]

for url in urls:
    info = get_ski_info(url)
    print(f"URL: {url}")
    print(f"Product Name: {info['name']}")
    print(f"Price: {info['price']}")
    if 'error' in info:
        print(f"Error (if any): {info['error']}")
    print('-' * 60)
