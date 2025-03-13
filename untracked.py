import requests
from bs4 import BeautifulSoup


def get_ski_info(url):
    try:
        # Set headers to mimic a browser request
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Make the request to the website
        response = requests.get(url, headers=headers)

        # Check if request was successful
        if response.status_code != 200:
            return {
                "name":
                None,
                "price":
                None,
                "error":
                f"Failed to fetch webpage. Status code: {response.status_code}"
            }

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # ---------- 1) Get the product name ----------
        name_element = soup.find('span', class_='secondHeaderName')
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

        # Return both in a dictionary for clarity
        return {"name": product_name, "price": price}

    except Exception as e:
        return {"name": None, "price": None, "error": str(e)}


# Example usage
urls = [
    "https://www.untracked.com/p8097-25_icelantic_nomad_112_freeride_all_mountain_skis.html",
    "https://www.untracked.com/p8100-25_icelantic_saba_117_big_mountain_freeride_skis.html",
    "https://www.untracked.com/p8089c14b43-25_atomic_maven_86_c_womens_all_mountain_skis.html",
    "https://www.untracked.com/p8169c101b53-25_volkl_m7_mantra_96_skis_w_tyrolia_attack_14gw_black_bindings.html"
]

for url in urls:
    info = get_ski_info(url)
    print(f"URL: {url}")
    print(f"Product Name: {info['name']}")
    print(f"Price: {info['price']}")
    if 'error' in info:
        print(f"Error (if any): {info['error']}")
    print('-' * 60)
