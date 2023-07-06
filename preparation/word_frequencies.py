import json
from collections import Counter
import pandas as pd
import nltk
import string
from nltk.corpus import stopwords

def is_ascii(word):
    return all(ord(c) < 128 for c in word)

def calculate_frequencies(data, stopwords_list):
    all_keywords = []

    for item in data:
        content = item['content'].split(' ')
        keywords = item['keywords'].split(', ')
        topics = item['topics'].split(', ')

        words = content + keywords + topics
        words = [w.replace('-', ' ').lower().translate(str.maketrans('', '', string.punctuation)) for w in words]
        words = [
            w for w in words
            if w not in stopwords_list and w.isalnum() and not any(c.isdigit() for c in w) and is_ascii(w)
        ]

        all_keywords += words

    frequencies = Counter(all_keywords)
    return frequencies

with open('topics_keywords.json', 'r', encoding='utf8') as f:
    data = json.load(f)

stopwords_list = set(stopwords.words('english'))
frequencies = calculate_frequencies(data, stopwords_list)

# Convert the Counter object to a dictionary
frequencies_dict = dict(frequencies)

# Save the dictionary to a JSON file
with open('word_frequencies.json', 'w', encoding='utf8') as wf:
    json.dump(frequencies_dict, wf)