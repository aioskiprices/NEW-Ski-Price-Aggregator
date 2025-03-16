import logging
from flask import Flask, render_template, request, url_for
import json
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for session management

def clean_price(price_str):
    """Convert price string to float, removing currency symbols and commas."""
    try:
        if not price_str or price_str == "Price not found":
            return float('inf')
        return float(price_str.replace('$', '').replace(',', '').replace(' USD', ''))
    except (ValueError, TypeError) as e:
        logger.error(f"Error cleaning price {price_str}: {str(e)}")
        return float('inf')

def load_ski_data():
    """Load and return ski data from JSON file."""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, 'ski_prices.json')
        with open(json_path, 'r') as f:
            data = json.load(f)
            logger.info(f"Successfully loaded {len(data['skis'])} skis from ski_prices.json")
            return data['skis']
    except FileNotFoundError:
        logger.error("ski_prices.json not found")
        return []
    except json.JSONDecodeError:
        logger.error("Invalid JSON in ski_prices.json")
        return []
    except Exception as e:
        logger.error(f"Unexpected error loading ski data: {str(e)}")
        return []

def get_image_path(ski_name):
    """Convert ski name to a valid filename and check if image exists."""
    # Remove year and 'Skis' from the name, and clean up special characters
    cleaned_name = ski_name.lower()
    cleaned_name = cleaned_name.replace('skis', '').replace('2024', '').replace('2025', '').replace('2026', '')
    cleaned_name = cleaned_name.replace('|', '').replace('  ', ' ').strip()
    
    # Handle special cases for our specific skis
    if "black crows mirus cor" in cleaned_name:
        filename = "black_crows_mirus_cor"
    elif "stockli montero ar" in cleaned_name:
        filename = "stockli_montero_ar"
    elif "mantra" in cleaned_name and ("volkl" in cleaned_name or "völkl" in cleaned_name):
        filename = "volkl_mantra"
    else:
        # Default case: Replace spaces and special chars with underscores
        filename = cleaned_name.replace(' ', '_').replace('-', '_')
    
    print(f"Original ski name: {ski_name}")
    print(f"Cleaned filename: {filename}")
    
    # Check for different possible extensions
    for ext in ['.png', '.jpg', '.jpeg', '.webp']:
        image_path = f'images/skis/{filename}{ext}'
        full_path = os.path.join('static', image_path)
        print(f"Checking path: {full_path}")
        if os.path.exists(full_path):
            print(f"Found image at: {image_path}")
            return image_path
    
    print(f"No image found for {ski_name}, using default")
    return 'images/skis/default_ski.jpg'

def find_best_deals(search_query=None):
    """Find best deals for skis, optionally filtered by search query."""
    ski_data = load_ski_data()
    
    if search_query:
        # Filter skis based on search query
        matching_skis = []
        search_query = search_query.lower().strip()
        search_terms = search_query.split()
        
        for ski in ski_data:
            ski_name_lower = ski['ski_name'].lower()
            # Check if all search terms are in the ski name
            if all(term in ski_name_lower for term in search_terms):
                matching_skis.append(ski)
        
        # Sort matching skis by price
        matching_skis.sort(key=lambda x: clean_price(x['current_price']))
        ski_data = matching_skis
    else:
        # For the landing page, show our three specific skis
        default_skis = []
        for target_name in ["Black Crows Mirus Cor", "Stockli Montero AR", "Volkl Mantra"]:
            target_name_lower = target_name.lower()
            matching_options = []
            
            for ski in ski_data:
                if target_name_lower in ski['ski_name'].lower():
                    matching_options.append(ski)
            
            # Sort by price and get the cheapest option
            if matching_options:
                matching_options.sort(key=lambda x: clean_price(x['current_price']))
                default_skis.append(matching_options[0])
        
        ski_data = default_skis
    
    # Format the results
    formatted_results = []
    for ski in ski_data:
        # Get the local image path for this ski
        image_path = get_image_path(ski['ski_name'])
        
        # Find the highest price for this ski model to calculate savings
        ski_name_base = ski['ski_name'].lower().replace('2024', '').replace('2025', '').replace('2026', '').strip()
        all_prices = [clean_price(s['current_price']) for s in ski_data if 
                     s['ski_name'].lower().replace('2024', '').replace('2025', '').replace('2026', '').strip() == ski_name_base]
        
        current_price = clean_price(ski['current_price'])
        highest_price = max(all_prices) if all_prices else current_price
        
        # Calculate savings
        savings_amount = highest_price - current_price
        savings_percentage = (savings_amount / highest_price) * 100 if highest_price > 0 else 0
        
        formatted_results.append({
            'name': ski['ski_name'],
            'deals': [{
                'price': f"${int(clean_price(ski['current_price']))}",
                'store': ski['site_name'],
                'url': ski['site_url'],
                'image_url': url_for('static', filename=image_path),
                'highest_price': f"${int(highest_price)}" if highest_price > current_price else None,
                'savings_amount': f"${int(savings_amount)}" if savings_amount > 0 else None,
                'savings_percentage': f"{int(savings_percentage)}%" if savings_amount > 0 else None
            }]
        })
    
    logger.info(f"Found {len(formatted_results)} results for query: {search_query}")
    return formatted_results

def load_featured_skis():
    """Load and return featured skis data from JSON file."""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, 'featured_skis.json')
        with open(json_path, 'r') as f:
            data = json.load(f)
            logger.info(f"Successfully loaded {len(data['featured_skis'])} featured skis")
            return data['featured_skis']
    except FileNotFoundError:
        logger.error("featured_skis.json not found")
        return []
    except json.JSONDecodeError:
        logger.error("Invalid JSON in featured_skis.json")
        return []
    except Exception as e:
        logger.error(f"Unexpected error loading featured skis: {str(e)}")
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        # Load featured skis for the landing page
        default_skis = load_featured_skis()
        if not default_skis:
            logger.warning("No featured skis loaded for landing page")
        
        search_results = None
        if request.method == 'POST':
            search_query = request.form.get('ski_name', '').strip()
            if search_query:
                search_results = find_best_deals(search_query)
                logger.info(f"Found {len(search_results)} results for '{search_query}'")
        
        return render_template('index.html', 
                             default_skis=default_skis if default_skis else None,
                             search_results=search_results if search_results else None)
    
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}")
        return render_template('index.html', default_skis=[], search_results=None)

@app.route('/update-prices')
def update_prices():
    update_ski_prices()
    return "Prices updated successfully!"

if __name__ == '__main__':
    # Development server configuration
    if os.environ.get('FLASK_ENV') == 'development':
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=True
        )
    else:
        # Production configuration
        app.run(
            host='0.0.0.0',
            port=8000,
            debug=False
        ) 