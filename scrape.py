import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")
        return None

def extract_body_content(dom_content):
    body = dom_content.find('body')
    return body.get_text() if body else ''

def clean_body_content(body_content):
    return ' '.join(body_content.split())

def split_dom_content(dom_content):
    # Example implementation to split content into chunks
    return [dom_content[i:i+1000] for i in range(0, len(dom_content), 1000)]