# 📧 Mail Threat Detection

**Mail Threat Detection** is a smart email scanner built with **machine learning** and **OCR (Optical Character Recognition)**. It helps detect **phishing** and **spam emails** before they become a threat.

Users can **either type/paste the email content** or **upload an image** (like a screenshot of an email). The app will extract the text from the image, scan it using a trained model, and instantly show whether the message is **safe** or **spam**.

It’s a helpful tool for students, office workers, and anyone who wants to stay safe from online email threats.

---

## 🔍 Key Features

- ✅ Scans email text and predicts: `Spam` or `Safe`
- 🖼️ Supports image input — Extracts email content using OCR (Tesseract)
- 🧠 Uses trained ML model (Naive Bayes) and TfidfVectorizer
- 🖥️ Simple and clean GUI (Tkinter)
- 💡 Very easy to run – No advanced setup required
- 🔐 Works offline after installation
## 🖼️ Demo

![App Screenshot](UI.png)
---
## 🛠️ How to Run the Project

Follow these steps to set up and run the Mail Threat Detection app on your computer:

---

### ✅ 1. Clone the Repository

```bash
git clone https://github.com/Tinsaie/Mail-Threat-Detection.git
cd Mail-Threat-Detection
