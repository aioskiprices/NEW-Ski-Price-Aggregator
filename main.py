import json
from scrapers.untracked import get_ski_info as get_untracked_info
from scrapers.christysports import get_ski_info_christysports
from scrapers.evo import get_ski_info_evo
from scrapers.utahskigear import get_ski_info_utahskigear
from scrapers.skihaus import get_ski_info_skihaus
from scrapers.bootpro import get_ski_info_bootpro
from scrapers.blackcrows import get_ski_info_blackcrows
from scrapers.bakerst import get_ski_info_bakerst
from scrapers.gearx import get_ski_info_gearx
from scrapers.sportsbasement import get_ski_info_sportsbasement

def clean_price(price_str):
    """Convert price string to float, removing currency symbols and commas."""
    if not price_str or price_str == "Price not found":
        return float('inf')
    return float(price_str.replace('$', '').replace(',', '').replace(' USD', ''))

def find_best_price(ski_name):
    """Find the best price for a given ski model across all stores."""
    # Read the current JSON file
    with open('ski_prices.json', 'r') as file:
        data = json.load(file)
    
    # Convert ski name to lowercase for case-insensitive comparison
    ski_name = ski_name.lower()
    
    # Find all matching skis
    matching_skis = []
    for ski in data['skis']:
        if ski_name in ski['ski_name'].lower():
            matching_skis.append(ski)
    
    if not matching_skis:
        return None
    
    # Sort by price
    matching_skis.sort(key=lambda x: clean_price(x['current_price']))
    
    # Get the best price
    best_deal = matching_skis[0]
    
    # Format the results
    results = {
        'best_price': best_deal['current_price'],
        'best_store': best_deal['site_name'],
        'best_url': best_deal['site_url'],
        'best_image_url': best_deal.get('image_url', ''),
        'all_options': [
            {
                'store': ski['site_name'],
                'price': ski['current_price'],
                'url': ski['site_url'],
                'name': ski['ski_name'],
                'image_url': ski.get('image_url', '')
            }
            for ski in matching_skis
        ]
    }
    
    return results

def update_ski_prices():
    # Read the current JSON file
    with open('ski_prices.json', 'r') as file:
        data = json.load(file)
    
    # Update prices for each ski
    for ski in data['skis']:
        if ski['site_name'] == 'Untracked':
            info = get_untracked_info(ski['site_url'])
            ski['current_price'] = info['price']
            if info['name'] and info['name'] != "Name not found":
                ski['ski_name'] = info['name']
        elif ski['site_name'] == 'Christy Sports':
            info = get_ski_info_christysports(ski['site_url'])
            ski['current_price'] = info['price']
            if info['name'] and info['name'] != "Name not found":
                ski['ski_name'] = info['name']
        elif ski['site_name'] == 'Evo':
            info = get_ski_info_evo(ski['site_url'])
            ski['current_price'] = info['price']
            if info['name'] and info['name'] != "Name not found":
                ski['ski_name'] = info['name']
        elif ski['site_name'] == 'Utah Ski Gear':
            info = get_ski_info_utahskigear(ski['site_url'])
            ski['current_price'] = info['price']
            if info['name'] and info['name'] != "Name not found":
                ski['ski_name'] = info['name']
        elif ski['site_name'] == 'Ski Haus':
            info = get_ski_info_skihaus(ski['site_url'])
            ski['current_price'] = info['price']
            if info['name'] and info['name'] != "Name not found":
                ski['ski_name'] = info['name']
        elif ski['site_name'] == 'Boot Pro':
            info = get_ski_info_bootpro(ski['site_url'])
            ski['current_price'] = info['price']
            if info['name'] and info['name'] != "Name not found":
                ski['ski_name'] = info['name']
        elif ski['site_name'] == 'Black Crows':
            info = get_ski_info_blackcrows(ski['site_url'])
            ski['current_price'] = info['price']
            if info['name'] and info['name'] != "Name not found":
                ski['ski_name'] = info['name']
        elif ski['site_name'] == 'Baker Street':
            info = get_ski_info_bakerst(ski['site_url'])
            ski['current_price'] = info['price']
            if info['name'] and info['name'] != "Name not found":
                ski['ski_name'] = info['name']
        elif ski['site_name'] == 'GearX':
            info = get_ski_info_gearx(ski['site_url'])
            ski['current_price'] = info['price']
            if info['name'] and info['name'] != "Name not found":
                ski['ski_name'] = info['name']
        elif ski['site_name'] == 'Sports Basement':
            info = get_ski_info_sportsbasement(ski['site_url'])
            ski['current_price'] = info['price']
            if info['name'] and info['name'] != "Name not found":
                ski['ski_name'] = info['name']
        else:
            print(f"Unknown site: {ski['site_name']}")
            continue
            
        print(f"({ski['site_name']}) Updated {ski['ski_name']}: {ski['current_price']}")
    
    # Write the updated data back to the JSON file
    with open('ski_prices.json', 'w') as file:
        json.dump(data, file, indent=4)

def main():
    while True:
        print("\nSki Price Aggregator")
        print("1. Update all prices")
        print("2. Search for best price")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            update_ski_prices()
        elif choice == "2":
            ski_name = input("\nEnter the ski name to search for: ")
            results = find_best_price(ski_name)
            
            if results:
                print(f"\nBest price found: {results['best_price']} at {results['best_store']}")
                print(f"URL: {results['best_url']}")
                
                print("\nAll available options:")
                for option in results['all_options']:
                    print(f"- {option['store']}: {option['price']} ({option['name']})")
            else:
                print("\nNo matching skis found.")
        elif choice == "3":
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
