import requests
from bs4 import BeautifulSoup
import json
import time
import random
import os

def load_urls_from_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f]

def save_scraped_link(filename, link):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(link + "\n")

def append_to_json_file(filename, page_data):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(page_data)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Load URLs from the text file
all_links = load_urls_from_file('bookmarks_urls.txt')

print(f"Found {len(all_links)} links in the text file.")

scraped_links_file = "scraped_links.txt"
scraped_links = load_urls_from_file(scraped_links_file)
print(f"Loaded {len(scraped_links)} scraped links from previous runs.")

output_file = 'scraped_pages.json'

for i, link in enumerate(all_links):
    if link in scraped_links:
        print(f"Skipping already scraped link: {link} ({i+1}/{len(all_links)})")
        continue

    try:
        print(f"Scraping content from {link} ({i+1}/{len(all_links)})")
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text if soup.find('title') else ''
        paragraphs = [p.text for p in soup.find_all('p')]
        content = ' '.join([title] + paragraphs)
        
        page_data = {'url': link, 'content': content}
        append_to_json_file(output_file, page_data)

        print(f"Successfully scraped {link} and appended to {output_file}")

        save_scraped_link(scraped_links_file, link)
    except Exception as e:
        print(f"Error processing {link}: {e}")

    # Wait for a random time between 1 and 2 seconds:
    wait_time = random.uniform(1, 2)
    print(f"Waiting {wait_time:.2f} seconds before next request")
    time.sleep(wait_time)

print("Scraping completed.")
