# BookMark Brain

![Demo](https://github.com/alfiedennen/BookMarkBrain/blob/main/demo.gif)

BookMark Brain is an intelligent bookmark management system developed to help you search and access bookmarked web pages based on their content, topics, and keywords. Powered by a GPT-3.5 Turbo engine from OpenAI, this application sorts through your saved bookmarks, extracts key topics and keywords, summarizes content, and then allows you to search for bookmarks using these data points.

## Python Scripts:

### 1. `.\preparation\_bookmark_scraper.py`

This script is for extracting bookmark URLs from the provided bookmarks JSON file. The URLs are then stored in a new text file named `bookmarks_urls.txt`.

### 2. `.\preparation\web_scraper.py`

This script retrieves, processes, and saves the content from each of the URLs in `bookmarks_urls.txt`, unless it's already been scraped or is an unwanted URL type (pdf, mp3, etc.). The scraped content is saved to a new JSON file named `scraped_pages.json`.

### 3. `.\preparation\neuroengine_summariser.py`

This script takes the scraped web pages, sends each page's content to OpenAI's GPT-3.5 Turbo engine for summarization, and then saves these updated records back to the JSON file.

### 4. `.\preparation\topics_and_keyword_extraction.py`

This script identifies the main topics and keywords from the summarized content of each scraped page, using OpenAI's GPT-3.5 Turbo engine. These topics and keywords are then added back to the JSON file.

### 5. `.\preparation\clean_json.py`

This script goes through the JSON file and filters out any records containing unwanted phrases. The remaining records are saved back to the JSON file.

### 6. `.\preparation\pre_process_data.py`

This script tokenizes and stems the content, keywords, website name, and path info of each record in the JSON file, and then saves this pre-processed data to a new JSON file named `final_bookmark_data.json`.

### 7. `.\preparation\word_frequencies.py`

This script calculates the frequency of each word in the dataset, excluding any stopwords and special characters, and saves these frequencies to a new JSON file named `word_frequencies.json`.

### 8. `.\process_pipeline.py`

This script calls the main function of each of the above scripts (except `_bookmark_scraper.py`), in the order that they are listed, to automate the entire bookmark processing pipeline.

### 9. `.\server.py`

This script sets up a web server which loads in all of the processed data and serves it via an API built using Flask. The server includes a custom search function that allows for searching through your bookmarks based on given keywords.

### 10. `.\preparation\__init__.py`

An empty file that indicates to Python that the `preparation` directory should be treated as a package.

## File Structure:

- `.\preparation` - This directory contains all of the Python scripts necessary for processing and summarizing bookmark data.
- `.\readme.md` - This markdown file provides an overview of the BookMark Brain application and describes how to install and use it.
- `.\requirements.txt` - This file lists all Python libraries required for the application.
- `.\server.py` - This Python script, located in the root directory, starts up the web server and API.

## Getting Started:

Refer to the installation and usage instructions in `.\readme.md` to get started. The scripts are designed to be run sequentially, as dictated in `.\process_pipeline.py`. This process can be repeated periodically to update your bookmarks.

## Note:

Please remember to set up your OpenAI API key in the `.\preparation\neuroengine_summariser.py` and `.\preparation\topics_and_keyword_extraction.py` scripts before running.

## Contribution:

Contributions and feature requests are welcome!

## License:

This project is licensed under the MIT License.