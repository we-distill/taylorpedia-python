import os
import sys
import requests
from bs4 import BeautifulSoup

# Constaints
LIMIT_PER_PAGE = 5
MAX_DEPTH = 2
GLOBAL_MAX = 50
global_counter = 0

def fetch_page(url, depth=0):
    global global_counter
    if global_counter >= GLOBAL_MAX:
        raise Exception('Reached global max limit')

    global_counter += 1
    print(f"Loading site: {url}")
    response = requests.get(url)
    html = response.text
    print(f'Got {len(html) / 1024:.2f} KB of HTML')
    
    links = process_page(url, html)

def process_page(url, html):
    soup = BeautifulSoup(html, 'html.parser')

    # Clean up page by removing unwanted elements
    for selector in ['script', '.vector-header', 'nav', '#p-lang-btn', 'style']:
        for tag in soup.select(selector):
            tag.decompose()

    # Output HTML to a file
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    base_name = url.split('/')[-1] or 'index'
    output_path = os.path.join(output_dir, f"{base_name}.html")
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))
    print(f'Saved HTML to {output_path}')

    # Extract links starting with /wiki/
    links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('/wiki/') and ':' not in a['href']]
    print(f'Found links: {links[:LIMIT_PER_PAGE]}')
    return links[:LIMIT_PER_PAGE]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    fetch_page(url)
    print(f'Total pages fetched: {global_counter}')