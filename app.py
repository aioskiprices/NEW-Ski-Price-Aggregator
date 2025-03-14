from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for session management

def clean_price(price_str):
    """Convert price string to float, removing currency symbols and commas."""
    if not price_str or price_str == "Price not found":
        return float('inf')
    return float(price_str.replace('$', '').replace(',', '').replace(' USD', ''))

def load_ski_data():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, 'ski_prices.json')
        with open(json_path, 'r') as f:
            data = json.load(f)
            return data['skis']  # Return just the skis array
    except FileNotFoundError:
        print("Warning: ski_prices.json not found")
        return []
    except json.JSONDecodeError:
        print("Warning: Invalid JSON in ski_prices.json")
        return []

def format_ski_data(ski):
    """Format ski data for template display."""
    return {
        'name': ski['ski_name'],
        'deals': [{
            'price': ski['current_price'],
            'store': ski['site_name'],
            'url': ski['site_url'],
            'image_url': ski.get('image_url', ''),
        }]
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        ski_data = load_ski_data()
        print("Loaded ski data:", len(ski_data), "skis")  # Debug print
        
        if request.method == 'POST':
            search_query = request.form.get('ski_name', '').lower()
            print("Search query:", search_query)  # Debug print
            
            # Filter skis based on search query
            search_results = []
            for ski in ski_data:
                if search_query in ski['ski_name'].lower():
                    formatted_ski = format_ski_data(ski)
                    search_results.append(formatted_ski)
                    print("Found matching ski:", ski['ski_name'])  # Debug print
            
            # Sort by price
            search_results.sort(key=lambda x: clean_price(x['deals'][0]['price']))
            print("Number of search results:", len(search_results))  # Debug print
            
            return render_template('index.html', 
                                 search_results=search_results if search_results else None,
                                 default_skis=[])
        
        # For initial page load, show all skis sorted by best price
        default_skis = []
        for ski in ski_data:
            formatted_ski = format_ski_data(ski)
            default_skis.append(formatted_ski)
        
        # Sort by price
        default_skis.sort(key=lambda x: clean_price(x['deals'][0]['price']))
        print("Number of default skis:", len(default_skis))  # Debug print
        
        return render_template('index.html', 
                             default_skis=default_skis if default_skis else None,
                             search_results=None)
    except Exception as e:
        print(f"Error in index route: {str(e)}")  # Debug print
        return render_template('index.html', default_skis=[], search_results=None)

@app.route('/update-prices')
def update_prices():
    update_ski_prices()
    return "Prices updated successfully!"

if __name__ == '__main__':
    # Development server configuration
    app.run(
        host='127.0.0.1',  # Only allow local connections
        port=5000,
        debug=True
    ) 