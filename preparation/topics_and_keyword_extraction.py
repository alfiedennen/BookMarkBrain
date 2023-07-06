import json
import time
import os
from neuroengine import Neuroengine

# Set up the service name
service_name = 'Neuroengine-Large'
api = Neuroengine(service_name=service_name)

def identify_topics(content):
    # Send the content to the LLM with instructions to identify key topics
    prompt = f"Your job is to read information and then select the most important topics in that text. You must select one and may select up to three if necessary. Each topic should be separated by a comma, and each topic should be no longer than two words. I have a text about: {content[:2000]}. What are up to three key topics in it? Reply only with the topics and no prefacing text."
    return api.request(prompt, temperature=0.4, top_p=0.9, max_new_len=30)

def identify_keywords(content):
    # Send the content to the LLM with instructions to identify keywords
    prompt = f"Your job is to read information and then select the most important keywords in that text. You must select one and may select up to three keywords if necessary. Each keyword should be separated by a comma, and each keyword should be no longer than one word. I have a text about: {content[:2000]}. What are up to three keywords in it? Reply only with the topics and no prefacing text."
    return api.request(prompt, temperature=0.4, top_p=0.9, max_new_len=30)

def load_processed_records(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f)
    else:
        return set()

def save_processed_record(filename, record_id):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(record_id + "\n")

def process_data(record):
    content = record['content']
    # Handle potential API errors with a retry loop
    for _ in range(5):  # Try up to 5 times
        try:
            print(f"Extracting topics for record {record['url']}...")
            topics = identify_topics(content)
            print(f"Received topics for record {record['url']}.")
            record['topics'] = topics

            print(f"Extracting keywords for record {record['url']}...")
            keywords = identify_keywords(content)
            print(f"Received keywords for record {record['url']}.")
            record['keywords'] = keywords

            return record  # return the updated record
        except Exception as e:
            print(f"Error processing record {record['url']}: {e}")
            time.sleep(5)  # Wait for 5 seconds before retrying
    return None  # Failed after 5 attempts

def process_file(filename, processed_records_file, output_filename='topics_keywords.json'):
    # Load data
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    processed_records = load_processed_records(processed_records_file)

    # Check if output file exists, if not, create an empty one
    if not os.path.exists(output_filename):
        print(f"Output file '{output_filename}' not found, creating a new one...")
        with open(output_filename, 'w') as f:
            json.dump([], f)

    # Process data
    for record in data:
        if record['url'] in processed_records:
            print(f"Skipping already processed record: {record['url']}")
            continue

        processed_record = process_data(record)
        if processed_record is not None:
            save_processed_record(processed_records_file, processed_record['url'])
            # Load the existing data from output file
            with open(output_filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            # Append the new processed data
            existing_data.append(processed_record)
            # Write the updated data back to the output file
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=4)
            print(f"Updated the output file with record {record['url']}")
        else:
            print(f"Failed to process record: {record['url']}. Continuing with next record.")

process_file('summarised.json', 'processed_records.txt')

