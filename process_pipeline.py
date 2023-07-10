import os
import sys

# Add the 'preparation' folder to the system path
project_root = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(os.path.abspath(project_root), 'preparation'))

# Use relative imports to import the necessary main() functions from the scripts
from preparation._bookmark_scraper import main as scrape_bookmarks
from preparation.web_scraper import main as web_scrape
from preparation.neuroengine_summariser import main as neuroengine_summarise
from preparation.topics_and_keyword_extraction import main as extract_topics_keywords
from preparation.clean_json import main as clean_data
from preparation.pre_process_data import main as preprocess_data
from preparation.word_frequencies import main as calculate_word_frequencies


def is_first_run():
    return not os.path.exists("bookmarks_urls.txt")


def main():
    if is_first_run():
        # Initial run
        scrape_bookmarks()
        web_scrape()
        neuroengine_summarise()
        extract_topics_keywords()
        clean_data()
        preprocess_data()
        calculate_word_frequencies()
    else:
        # Updating bookmarks
        scrape_bookmarks()
        web_scrape()
        neuroengine_summarise()
        extract_topics_keywords()
        clean_data()
        preprocess_data()
        calculate_word_frequencies()

    print("\nProcess_pipeline finished.")


if __name__ == "__main__":
    main()