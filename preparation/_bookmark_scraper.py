import os
import json

def extract_urls_from_bookmarks(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    urls = []
    for category in data['roots']:
        urls.extend(extract_urls(data['roots'][category]))
    return urls

def extract_urls(node):
    urls = []
    if 'children' in node:
        for child in node['children']:
            urls.extend(extract_urls(child))
    elif 'type' in node and node['type'] == 'url':
        urls.append(node['url'])
    return urls

def save_urls_to_file(urls, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for url in urls:
            f.write(url + "\n")

def main():
    file_path = 'D:\\Visual Studio Code Projects\\BOOKMARKBRAIN\\Bookmarks.json'
    urls = extract_urls_from_bookmarks(file_path)
    save_urls_to_file(urls, 'bookmarks_urls.txt')

if __name__ == "__main__":
    main()