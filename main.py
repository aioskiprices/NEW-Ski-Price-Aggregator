
from untracked import get_ski_info

def main():
    # Example URLs to test
    urls = [
        "https://www.untracked.com/p8097-25_icelantic_nomad_112_freeride_all_mountain_skis.html",
        "https://www.untracked.com/p8100-25_icelantic_saba_117_big_mountain_freeride_skis.html"
    ]
    
    for url in urls:
        info = get_ski_info(url)
        print(f"URL: {url}")
        print(f"Product Name: {info['name']}")
        print(f"Price: {info['price']}")
        if 'error' in info:
            print(f"Error (if any): {info['error']}")
        print('-' * 60)

if __name__ == "__main__":
    main()
