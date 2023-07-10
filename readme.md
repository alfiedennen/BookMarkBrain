# BookMark Brain

BookMark Brain is an intelligent bookmark management system designed to help you efficiently and quickly find the bookmarked web pages based on their content, topics, and keywords. Powered by an artificial intelligence model, this app sorts through your saved bookmarks, extracting key topics and keywords, and then summarises the content, allowing you to search for bookmarks using these data points.

## Features
- **Storage and Pre-processing**: BookMark Brain stores bookmark data in JSON format, pre-processes the textual content, and removes stopwords.
- **Content Summary**: The application generates summaries for the content of each bookmarked web page, making it easier to manage and scan through.
- **Topic and Keyword Extraction**: The AI model extracts topics and keywords, so you can find specific bookmarks using those search terms.
- **Search**: You can search for your bookmarks based on given keywords.
- **Visualisation**: The application creates a word cloud, visually displaying the most frequently occurring words in your bookmarks - click through to show search results on any word/phrase.

## Prerequisites

Before you get started, make sure you have the following installed:

- Python 3.7+
- An internet connection to use the NeuroEngine LLM API (note - you can swap out for any LLM you want, Neuroengine is powerful and free so it's good for bulk work like this).

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/bookmark_brain.git
cd bookmark_brain
```

Install required packages:

```bash
pip install -r requirements.txt
```

Download NLTK dependencies:

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## Usage

To use BookMark Brain, you will need to extract your bookmarks from your browser. Most browsers allow you to export bookmarks as an HTML format. Export your bookmarks and use a tool to convert the HTML format to JSON format.

Save the JSON formatted bookmarks as "bookmarks.json" in the root directory of this project.

1. Run the bookmark scraper script to scrape your bookmarked pages:

```bash
python ./preparation/web_scraper.py
```

2. Extract topics and keywords from the scraped pages:

```bash
python ./preparation/topics_and_keyword_extraction.py
```

3. Clean the JSON file:

```bash
python ./preparation/clean_json.py
```

4. Summarise the scraped content using the AI engine:

```bash
python ./preparation/neuroengine_summariser.py
```

5. Pre-process the data and save it to another JSON file:

```bash
python ./preparation/pre_process_data.py
```

6. Calculate word frequencies and store them in the JSON format:

```bash
python ./preparation/word_frequencies.py
```

7. Run the server:

```bash
python ./server.py
```

Now visit `http://127.0.0.1:5000` in your web browser to access BookMark Brain.

## Contribution

Contributions, issues, and feature requests are welcome!
## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.