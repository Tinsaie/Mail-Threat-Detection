# 🛡️ PhishShield

**PhishShield** is a simple and powerful desktop application built using **Python**, **Tkinter**, and a trained **machine learning model** to detect phishing websites in real-time.

---

## 📌 Features

- ✅ Detects phishing URLs using a trained ML model
- 🧠 Uses `RandomForestClassifier` trained on phishing data
- 🖥️ Built with `Tkinter` for a simple GUI
- 💡 Easy to use: paste a URL and get instant results!

---

## 📁 Folder Structure

```
PhishShield/
├── main.py                    # Main GUI application
├── spam_classifier_model.pkl  # Trained ML model
├── vectorizer.pkl             # Text vectorizer for URLs
├── requirements.txt           # List of required libraries
└── README.md                  # Project documentation
```

---

## ⚙️ Requirements

Install the required libraries with:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```
tk
scikit-learn
joblib
```

(Include any others you use like `numpy`, `pandas`, etc.)

---

## 🚀 How to Run

1. Clone the repository:

```bash
git clone https://github.com/Tinsaie/PhishShield.git
cd PhishShield
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python main.py
```

---

## 🧪 Model Info

- **Algorithm:** RandomForestClassifier
- **Input:** URL (string)
- **Output:** "Safe" or "Phishing"

---

## 📸 Screenshots

_Add your app screenshots here if available._

---

## ✍️ Author

- **Tinsaie**
- Email: tinsaiebbs@gmail.com
- GitHub: [@Tinsaie](https://github.com/Tinsaie)

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
