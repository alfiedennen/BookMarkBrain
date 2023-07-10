import json
from collections import Counter
import nltk
import string
from nltk.corpus import stopwords

import nltk
nltk.download('stopwords')

def is_ascii(word):
    return all(ord(c) < 128 for c in word)

def calculate_frequencies(data, stopwords_list):
    all_keywords = []
    for item in data:
        content = item['content'].split(' ')
        keywords = item['keywords']  # "keywords" is already a list
        website_name = item['website_name'].split('.')[:-1]  # Exclude the domain extension
        path_info = item['path_info'].strip('/').split('/')
        
        words = content + keywords + website_name + path_info
        words = [w.replace('-', ' ').lower().translate(str.maketrans('', '', string.punctuation)) for w in words]
        words = [w for w in words if w not in stopwords_list and w.isalnum() and not any(c.isdigit() for c in w) and is_ascii(w)]
        
        all_keywords += words

    frequencies = Counter(all_keywords)
    return frequencies

def main():
    with open('final_bookmark_data.json', 'r', encoding='utf8') as f:
        data = json.load(f)

    stopwords_list = set(stopwords.words('english'))
    
    # Add additional words to ignore
    additional_stopwords = ['www', 'youtube', 'text', 'provides', 'mentions', 'website', 'facebook', 'watch', 'platform', 'users', 'cookies']
    stopwords_list.update(additional_stopwords)

    frequencies = calculate_frequencies(data, stopwords_list)

    # Convert the Counter object to a dictionary
    frequencies_dict = dict(frequencies)

    # Save the dictionary to a JSON file
    with open('word_frequencies.json', 'w', encoding='utf8') as wf:
        json.dump(frequencies_dict, wf)

if __name__ == "__main__":
    main()
