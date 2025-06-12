import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import pytesseract
import pickle
import os
import threading
from tkinter import font as tkfont
import time

# Tesseract OCR path (edit this path to where Tesseract is installed on your system)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # <-- EDIT THIS PATH YOURSELF

class PhishingEmailDetectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ PhishShieldX ")
        self.root.geometry("760x650")
        self.root.configure(bg="#121212")
        self.root.resizable(False, False)

        # Fonts
        self.title_font = tkfont.Font(family="Segoe UI", size=22, weight="bold")
        self.result_font = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        self.text_font = tkfont.Font(family="Consolas", size=11)

        # Icons
        try:
            # Make sure these icon files are in the same directory or provide full paths
            self.ok_icon = ImageTk.PhotoImage(Image.open("ok_icon.png").resize((28, 28)))  # <-- EDIT PATH if needed
            self.bad_icon = ImageTk.PhotoImage(Image.open("bad_icon.png").resize((28, 28)))  # <-- EDIT PATH if needed
        except:
            self.ok_icon = self.bad_icon = None

        self.model = None
        self.vectorizer = None
        if not self.load_models():
            self.root.destroy()
            return

        self.file_type_var = tk.StringVar(value="text")
        self.extracted_text = ""

        self.setup_ui()

        # Bind close window event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Bind file type change to adjust text_area state
        self.file_type_var.trace_add("write", self.on_file_type_change)

        # Set initial state for text_area depending on file type
        self.on_file_type_change()

    def load_models(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))  # Current script directory
            # Paths to your trained model and vectorizer files - update if stored elsewhere
            model_path = os.path.join(script_dir, "spam_classifier_model.pkl")  # <-- EDIT PATH if needed
            vectorizer_path = os.path.join(script_dir, "vectorizer.pkl")      # <-- EDIT PATH if needed

            if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
                messagebox.showerror("Missing Files", "Required model/vectorizer files not found.")
                return False

            with open(model_path, "rb") as f:
                self.model = pickle.load(f)
            with open(vectorizer_path, "rb") as f:
                self.vectorizer = pickle.load(f)

            return True
        except Exception as e:
            messagebox.showerror("Model Load Error", str(e))
            return False

    def setup_ui(self):
        header = tk.Frame(self.root, bg="#1f1f1f", padx=10, pady=10)
        header.pack(fill="x")
        tk.Label(header, text="🛡️ PhishShieldX", font=self.title_font, fg="#00bcd4", bg="#1f1f1f").pack()

        filetype_frame = tk.Frame(self.root, bg="#121212", pady=5)
        filetype_frame.pack(fill="x", padx=20)
        tk.Label(filetype_frame, text="Select file type:", bg="#121212", fg="white", font=self.text_font).pack(side="left", padx=(0, 10))
        for label, val in [("Text File", "text"), ("Image File", "image")]:
            tk.Radiobutton(filetype_frame, text=label, variable=self.file_type_var, value=val,
                           bg="#121212", fg="white", activebackground="#1f1f1f", selectcolor="#1f1f1f",
                           font=self.text_font).pack(side="left", padx=10)

        controls = tk.Frame(self.root, bg="#121212", pady=8)
        controls.pack(fill="x", padx=20)

        self.upload_btn = tk.Button(controls, text="📂 Upload File", font=self.text_font, bg="#263238", fg="white",
                                    relief="flat", activebackground="#00bcd4", activeforeground="black", command=self.upload_file)
        self.upload_btn.pack(side="left", padx=(0, 12))

        self.predict_btn = tk.Button(controls, text="🚀 Predict", font=self.text_font, bg="#263238", fg="white",
                                     relief="flat", activebackground="#00e676", activeforeground="black",
                                     command=self.start_prediction, state="disabled")
        self.predict_btn.pack(side="left")

        # Text area
        text_frame = tk.Frame(self.root, bg="#121212", pady=6)
        text_frame.pack(fill="both", expand=True, padx=20)
        tk.Label(text_frame, text="📄 Email Content:", bg="#121212", fg="#00bcd4", font=self.text_font).pack(anchor="w")
        self.text_area = scrolledtext.ScrolledText(text_frame, font=self.text_font, bg="#1e1e1e", fg="#aaaaaa",
                                                   height=14, insertbackground="white", wrap=tk.WORD,
                                                   padx=10, pady=8, borderwidth=0)
        self.text_area.pack(fill="both", expand=True)
        self.placeholder = "Upload a file to start analyzing..."

        # Bind focus events for placeholder
        self.text_area.bind("<FocusIn>", self.clear_placeholder)
        self.text_area.bind("<FocusOut>", self.add_placeholder_if_empty)

        # Bind to typing/pasting to enable/disable predict button dynamically
        self.text_area.bind("<KeyRelease>", self.update_predict_button_state)
        self.text_area.bind("<<Paste>>", self.update_predict_button_state)

        # Start with predict button disabled
        self.predict_btn.config(state="disabled")

        # Result
        result_container = tk.Frame(self.root, bg="#121212")
        result_container.pack(fill="x", padx=20)
        tk.Label(result_container, text="📊 Prediction Result:", bg="#121212", fg="#00bcd4", font=self.text_font).pack(anchor="w")

        result_box = tk.Frame(result_container, bg="#1f1f1f", height=60, padx=10, pady=5)
        result_box.pack(fill="x", pady=5)
        result_box.pack_propagate(False)

        self.result_icon_label = tk.Label(result_box, bg="#1f1f1f")
        self.result_icon_label.pack(side="left", padx=(0, 10))

        self.result_label = tk.Label(result_box, text="No prediction made yet.", font=self.result_font,
                                     fg="#888", bg="#1f1f1f", anchor="w", justify="left")
        self.result_label.pack(side="left", fill="x", expand=True)

        self.status_var = tk.StringVar()
        status_bar = tk.Label(self.root, textvariable=self.status_var, font=("Segoe UI", 9),
                              bg="#1f1f1f", fg="#aaaaaa", anchor="w", pady=4)
        status_bar.pack(fill="x", side="bottom")

        self.add_hover_effect(self.upload_btn)
        self.add_hover_effect(self.predict_btn)

    def on_file_type_change(self, *args):
        file_type = self.file_type_var.get()
        if file_type == "text":
            self.text_area.config(state="normal", fg="#aaaaaa")
            # Clear placeholder and allow typing
            current_text = self.text_area.get("1.0", tk.END).strip()
            if current_text == self.placeholder or not current_text:
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, self.placeholder)
                self.text_area.config(fg="#aaaaaa")
            self.predict_btn.config(state="disabled")  # wait for user input or upload
        else:  # image
            # Disable editing until image uploaded
            self.text_area.config(state="normal")
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, "Upload an image to extract text...")
            self.text_area.config(state="disabled", fg="#666666")
            self.predict_btn.config(state="disabled")

    def update_predict_button_state(self, event=None):
        if self.text_area.cget("state") == "normal":
            current_text = self.text_area.get("1.0", tk.END).strip()
            if current_text and current_text != self.placeholder:
                self.predict_btn.config(state="normal")
            else:
                self.predict_btn.config(state="disabled")
        else:
            self.predict_btn.config(state="disabled")

    def clear_placeholder(self, event=None):
        if self.text_area.cget("state") == "normal":
            current_text = self.text_area.get("1.0", tk.END).strip()
            if current_text == self.placeholder:
                self.text_area.delete("1.0", tk.END)
                self.text_area.config(fg="#eeeeee")

    def add_placeholder_if_empty(self, event=None):
        if self.text_area.cget("state") == "normal":
            current_text = self.text_area.get("1.0", tk.END).strip()
            if not current_text:
                self.text_area.insert(tk.END, self.placeholder)
                self.text_area.config(fg="#aaaaaa")
                self.predict_btn.config(state="disabled")  # disable predict when placeholder present

    def on_closing(self):
        self.root.destroy()

    def add_hover_effect(self, button):
        def on_enter(e):
            button['bg'] = '#00bcd4'
            button['fg'] = 'black'
        def on_leave(e):
            button['bg'] = '#263238'
            button['fg'] = 'white'
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def upload_file(self):
        ftypes = [("Text files", "*.txt"), ("All files", "*.*")]
        if self.file_type_var.get() == "image":
            ftypes = [("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff"), ("All files", "*.*")]
        file_path = filedialog.askopenfilename(title="Select File", filetypes=ftypes)
        if not file_path:
            return
        try:
            if self.file_type_var.get() == "text":
                with open(file_path, "r", encoding="utf-8") as f:
                    self.extracted_text = f.read()
                self.text_area.config(state="normal", fg="#eeeeee")
            else:
                img = Image.open(file_path)
                self.extracted_text = pytesseract.image_to_string(img)
                # After OCR, make text_area editable for image type
                self.text_area.config(state="normal", fg="#eeeeee")

            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, self.extracted_text)
            
            self.status_var.set(f"Loaded file: {os.path.basename(file_path)}")
            self.result_label.config(text="No prediction made yet.", fg="#888")
            self.result_icon_label.config(image="")
            self.predict_btn.config(state="normal")

        except Exception as e:
            messagebox.showerror("File Error", f"Unable to read file:\n{e}")
            self.status_var.set("File load failed.")
            self.predict_btn.config(state="disabled")
            if self.file_type_var.get() == "image":
                # disable editing if image load failed
                self.text_area.config(state="disabled")

    def start_prediction(self):
        if self.text_area.cget("state") != "normal":
            messagebox.showwarning("Input Needed", "Please upload a file or enter some text.")
            return

        text = self.text_area.get("1.0", tk.END).strip()
        if not text or text == self.placeholder:
            messagebox.showwarning("Input Needed", "Please upload a file or enter some text.")
            return

        self.predict_btn.config(state="disabled")
        
        self.result_label.config(text="Predicting...", fg="#ffca28")
        self.result_icon_label.config(image="")

        threading.Thread(target=self.predict_thread, args=(text,), daemon=True).start()

    def predict_thread(self, text):
        for i in range(5):
            dots = '.' * ((i % 3) + 1)
          
            time.sleep(0.3)

        try:
            text_features = self.vectorizer.transform([text])

            # Get probability for phishing class (1)
            probs = self.model.predict_proba(text_features)[0]
            phishing_prob = probs[1]

            threshold = 0.17  # Adjust this threshold

            if phishing_prob >= threshold:
                self.result_label.config(text="⚠️ PHISHING DETECTED!", fg="#ef5350")
                icon = self.bad_icon
            else:
                self.result_label.config(text="✅ NORMAL EMAIL.", fg="#66bb6a")
                icon = self.ok_icon

            if icon:
                self.result_icon_label.config(image=icon)
                self.result_icon_label.image = icon
            else:
                self.result_icon_label.config(image="")

            
        except Exception as e:
            messagebox.showerror("Prediction Error", str(e))
            self.status_var.set("Prediction failed.")
        finally:
            self.predict_btn.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = PhishingEmailDetectorGUI(root)
    root.mainloop()
