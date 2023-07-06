import json
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

stemmer = SnowballStemmer("english")

def tokenize_and_stem(text):
    tokens = word_tokenize(text.lower())
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return set(stemmed_tokens)

def preprocess_data(data):
    preprocessed_data = []
    for index, item in enumerate(data):
        preprocessed_item = item.copy()
        preprocessed_item["id"] = index  # Add this line to assign an 'id' field to each record
        preprocessed_item["content_tokens"] = list(tokenize_and_stem(item["content"]))
        preprocessed_item["topics_tokens"] = list(tokenize_and_stem(item["topics"]))
        preprocessed_item["keywords_tokens"] = list(tokenize_and_stem(item["keywords"]))
        preprocessed_data.append(preprocessed_item)
    return preprocessed_data

if __name__ == "__main__":
    with open("topics_keywords.json", "r", encoding="utf8") as f:
        data = json.load(f)

    preprocessed_data = preprocess_data(data)

    with open("preprocessed_topics_keywords.json", "w", encoding="utf8") as f:
        json.dump(preprocessed_data, f, ensure_ascii=False, indent=4)