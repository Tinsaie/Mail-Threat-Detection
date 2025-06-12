import os
import re
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score

# Configuration
# Set your dataset folder path here
base_dir = r"P:\email-threat-detector\training\dataset"

# Path to save model and vectorizer
model_dir = r"P:\email-threat-detector\saved_models"

# Map each folder to its label: 1 for spam, 0 for ham
folders = {
    "spam": 1,
    "spam_2": 1,
    "easy_ham": 0,
    "easy_ham_2": 0,
    "hard_ham": 0
}

# Load emails from the folders and assign labels
def load_emails(base_dir, folders):
    data = []
    for folder, label in folders.items():
        folder_path = os.path.join(base_dir, folder)
        if not os.path.isdir(folder_path):
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
    return data

# Clean the email text by removing headers, HTML, and non-letter characters
def clean_email(text):
    text = re.split(r'\n\n', text, maxsplit=1)[-1]
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Train the model using cleaned data and save the model and vectorizer
def train_and_save_model(data):
    cleaned_data = [(clean_email(email), label) for email, label in data]
    texts = [text for text, label in cleaned_data]
    labels = [label for text, label in cleaned_data]

    vectorizer = CountVectorizer(stop_words='english', max_features=3000)
    X = vectorizer.fit_transform(texts)

    X_train, X_test, y_train, y_test = train_test_split(
        X, labels, test_size=0.2, random_state=42
    )

    model = MultinomialNB()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

    os.makedirs(model_dir, exist_ok=True)
    with open(os.path.join(model_dir, "spam_classifier_model.pkl"), "wb") as f:
        pickle.dump(model, f)
    with open(os.path.join(model_dir, "vectorizer.pkl"), "wb") as f:
        pickle.dump(vectorizer, f)

    print("Model and vectorizer saved")

# Predict whether a new email is spam or not using the saved model
def predict_email(text):
    with open(os.path.join(model_dir, "spam_classifier_model.pkl"), "rb") as f:
        model = pickle.load(f)
    with open(os.path.join(model_dir, "vectorizer.pkl"), "rb") as f:
        vectorizer = pickle.load(f)

    cleaned = clean_email(text)
    vectorized = vectorizer.transform([cleaned])
    prediction = model.predict(vectorized)[0]
    return "Spam" if prediction == 1 else "Not Spam"

# Main process to load data, train the model, and test prediction
if __name__ == "__main__":
    print("Loading emails")
    data = load_emails(base_dir, folders)

    if not data:
        print("No email data found. Please check the dataset path and folder names")
    else:
        print(f"Loaded {len(data)} emails. Training model")
        train_and_save_model(data)

        sample_email = "Congratulations! You have been selected to win a $1000 Amazon gift card. Click here to claim now!"
        result = predict_email(sample_email)
        print("Sample Email:")
        print(sample_email)
        print("Prediction Result:", result)
