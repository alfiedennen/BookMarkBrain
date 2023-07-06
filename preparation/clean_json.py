import json

def filter_records(record):
    for key, value in record.items():
        if "write a response for an instruction" in value:
            return False
    return True

with open('topics_keywords.json', 'r', encoding='utf8') as f:
    data = json.load(f)

# Filter out records containing "Enable JavaScript"
filtered_data = list(filter(filter_records, data))

# Write the filtered data back to the file
with open('topics_keywords.json', 'w', encoding='utf8') as f:
    json.dump(filtered_data, f)