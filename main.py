import json
from untracked import get_ski_info as get_untracked_info
from christysports import get_ski_info_christysports

def update_ski_prices():
    # Read the current JSON file
    with open('ski_prices.json', 'r') as file:
        data = json.load(file)
    
    # Update prices for each ski
    for ski in data['skis']:
        if ski['site_name'] == 'Untracked':
            info = get_untracked_info(ski['site_url'])
        elif ski['site_name'] == 'Christy Sports':
            info = get_ski_info_christysports(ski['site_url'])
        else:
            print(f"Unknown site: {ski['site_name']}")
            continue
            
        ski['current_price'] = info['price']
        print(f"Updated {ski['ski_name']}: {ski['current_price']}")
    
    # Write the updated data back to the JSON file
    with open('ski_prices.json', 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    update_ski_prices()
