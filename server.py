import pandas as pd
import json
from flask import Flask, jsonify, request, render_template
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from urllib.parse import quote, unquote

app = Flask(__name__)
stemmer = SnowballStemmer("english")

def tokenize_and_stem(text):
    tokens = word_tokenize(text.lower())
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return set(stemmed_tokens)

# Load the final_bookmark_data.json at the start of the application
with open('final_bookmark_data.json', 'r', encoding='utf8') as f:
    data = json.load(f)
df = pd.DataFrame(data)

# Load the word_frequencies.json data into a Pandas Series
with open('word_frequencies.json', 'r', encoding='utf8') as wf:
    word_frequencies = pd.Series(json.load(wf))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data)

@app.route('/api/wordFrequency', methods=['GET'])
def get_word_frequency():
    # Convert the Series to dictionary before returning the result
    return word_frequencies.to_dict()

def process_keywords(row, keywords):
    return any(keyword_stem in (set(row["content_tokens"]).union(row["keywords_tokens"]))
                for keyword_stem in keywords)

@app.route('/api/search', methods=['GET'])
def search():
    keyword_string = request.args.get('keyword', '').lower()
    keywords = tokenize_and_stem(keyword_string)
    result_df = df[df.apply(lambda row: process_keywords(row, keywords), axis=1)]
    result = result_df.to_dict('records')
    return jsonify(result)

@app.route('/search')
def search_view():
    return render_template('search.html')

@app.route('/wordcloud')
def wordcloud():
    return render_template('wordcloud.html')

if __name__ == '__main__':
    app.run(debug=True)
