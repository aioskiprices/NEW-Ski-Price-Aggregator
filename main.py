import json
from untracked import get_ski_info

def update_ski_prices():
    # Read the current JSON file
    with open('ski_prices.json', 'r') as file:
        data = json.load(file)
    
    # Update prices for each ski
    for ski in data['skis']:
        info = get_ski_info(ski['site_url'])
        ski['current_price'] = info['price']
        print(f"Updated {ski['ski_name']}: {ski['current_price']}")
    
    # Write the updated data back to the JSON file
    with open('ski_prices.json', 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    update_ski_prices()
