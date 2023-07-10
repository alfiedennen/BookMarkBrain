import json

def filter_records(record):
    for key, value in record.items():
        unwanted_phrases = [
            "write a response for an instruction",
            "LOADING",
            "loading",
            "error",
            "403",
            "forbidden",
            "Forbidden",
            "Page Not Found",
            "Google Colab",
            "Just a moment",
            "We’ve detected that JavaScript is disabled",
            "LinkedIn",
            "The provided instruction",
            "The provided text",
            "Just a moment..."
        ]

        # If value is a list, convert it to a single string
        if isinstance(value, list):
            value = " ".join(value)
            
        # Now value is definitely a string, so we can perform the check
        if any(phrase.lower() in value.lower() for phrase in unwanted_phrases):
            print(f"Filtering out record: {record}")  # Debug print
            return False
    return True


def clean_data(input_file='keywords.json', output_file='cleaned_bookmarks.json'):
    with open(input_file, 'r', encoding='utf8') as f:
        data = json.load(f)

    # Filter out records containing unwanted phrases
    filtered_data = list(filter(filter_records, data))

    # Write the filtered data back to the file
    with open(output_file, 'w', encoding='utf8') as f:
        json.dump(filtered_data, f)

def main():
    clean_data()

if __name__ == "__main__":
    main()