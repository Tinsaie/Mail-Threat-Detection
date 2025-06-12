import os
import re

# Set base directory path and folder labels
base_dir = r"P:\email-threat-detector\training\dataset"
folders = {
    "spam": 1,
    "spam_2": 1,
    "easy_ham": 0,
    "easy_ham_2": 0,
    "hard_ham": 0
}

# Load emails from each folder and store with label
data = []
for folder, label in folders.items():
    folder_path = os.path.join(base_dir, folder)
    if not os.path.isdir(folder_path):
        print(f"Warning: Folder not found: {folder_path}")
        continue
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='latin1') as f:
                    content = f.read()
                    data.append((content, label))
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

# Define function to clean email text
def clean_email(text):
    # Remove email headers
    text = re.split(r'\n\n', text, maxsplit=1)[-1]
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Keep only letters and spaces
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    # Convert to lowercase and remove extra spaces
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Clean all emails using the cleaning function
cleaned_data = [(clean_email(email), label) for email, label in data]

