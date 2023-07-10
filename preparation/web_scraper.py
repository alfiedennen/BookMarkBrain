import requests
from bs4 import BeautifulSoup
import json
import os
import traceback
import re
from urllib.parse import urlsplit


def process_url(url):
    parsed_url = urlsplit(url)
    website_name = parsed_url.hostname
    path_info = parsed_url.path
    return website_name, path_info


def load_urls_from_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f]


def save_scraped_link(filename, link):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(link + "\n")


def append_to_json_file(filename, page_data):
    data = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            file_content = f.read().strip()
            if file_content:
                data = json.loads(file_content)
    except json.JSONDecodeError:
        print(f"File {filename} does not contain valid JSON. Starting a new JSON array.")

    data.append(page_data)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def create_file_if_not_exist(filename, content=None):
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            if content:
                f.write(content)
            else:
                f.write("[]")


def is_unwanted_link(url):
    pattern = re.compile('.*?\.(pdf|mp3|jpg|png|gif|mp4)$')
    if pattern.match(url):
        return True
    if 'youtube' in url:
        return False
    return False


def main():
    all_links = load_urls_from_file('bookmarks_urls.txt')

    print(f"Found {len(all_links)} links in the text file.")

    scraped_links_file = "scraped_links.txt"
    create_file_if_not_exist(scraped_links_file)
    scraped_links = load_urls_from_file(scraped_links_file)
    print(f"Loaded {len(scraped_links)} scraped links from previous runs.")

    output_file = 'scraped_pages.json'
    create_file_if_not_exist(output_file, "[]")

    for i, link in enumerate(all_links):
        if link in scraped_links or is_unwanted_link(link):
            print(f"Skipping unwanted or already scraped link: {link} ({i+1}/{len(all_links)})")
            continue

        try:
            print(f"Scraping content from {link} ({i+1}/{len(all_links)})")

            response = requests.get(link)
            if not response.text:
                raise ValueError("Empty content")

            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.find('title').text if soup.find('title') else ''
            paragraphs = [p.text for p in soup.find_all('p')]
            content = ' '.join([title] + paragraphs)
            content = content[:3000]

            if not content.strip():
                print(f"Error: No content found when scraping {link}")
                continue

            website_name, path_info = process_url(link)
            page_data = {'url': link, 'content': content, 'website_name': website_name, 'path_info': path_info}
            append_to_json_file(output_file, page_data)

            print(f"Successfully scraped {link} and appended to {output_file}")

            save_scraped_link(scraped_links_file, link)
        except Exception as e:
            print("Error processing {}: {}".format(link, e))
            print(traceback.format_exc())

    print("Scraping completed.")


if __name__ == "__main__":
    main()