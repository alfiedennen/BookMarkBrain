import json
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

stemmer = SnowballStemmer("english")


def tokenize_and_stem(text):
    if isinstance(text, list): 
        text = ' '.join(text)  # Convert list to a single string
    tokens = word_tokenize(text.lower())
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return set(stemmed_tokens)


def preprocess_data(data):
    preprocessed_data = []
    for index, item in enumerate(data):
        preprocessed_item = item.copy()
        preprocessed_item["id"] = index
        preprocessed_item["content_tokens"] = list(tokenize_and_stem(item["content"]))
        preprocessed_item["keywords_tokens"] = list(tokenize_and_stem(item["keywords"]))
        preprocessed_item["website_name_tokens"] = list(tokenize_and_stem(item["website_name"]))
        preprocessed_item["path_info_tokens"] = list(tokenize_and_stem(item["path_info"]))
        preprocessed_data.append(preprocessed_item)
    return preprocessed_data


def main():
    with open("cleaned_bookmarks.json", "r", encoding="utf8") as f:
        data = json.load(f)

    preprocessed_data = preprocess_data(data)

    with open("final_bookmark_data.json", "w", encoding="utf8") as f:
        json.dump(preprocessed_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()