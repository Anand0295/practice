#!/usr/bin/env python3
"""
Spam Email Classifier - Complete Single File Implementation
A minimal GUI application for classifying emails as spam or ham
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import re
import string
from collections import Counter

class SpamClassifier:
    """Simple Naive Bayes spam classifier"""
    
    def __init__(self):
        self.spam_words = Counter()
        self.ham_words = Counter()
        self.spam_count = 0
        self.ham_count = 0
        self.trained = False
        
        # Pre-train with common patterns
        self._pretrain()
    
    def _pretrain(self):
        """Pre-train with common spam/ham indicators"""
        spam_samples = [
            "Congratulations! You've won a prize! Click here now!",
            "Get rich quick! Make money fast! Limited time offer!",
            "Free viagra cialis buy now cheap pharmacy pills",
            "You have won the lottery! Claim your prize money now!",
            "Urgent! Your account needs verification. Click link immediately!",
            "Dear friend, I am a prince with millions to share with you",
            "Lose weight fast! Amazing diet pills! Order now!",
            "Casino bonus! Play now and win big money!"
        ]
        
        ham_samples = [
            "Hi, how are you? Let's meet for coffee tomorrow.",
            "The meeting is scheduled for 3 PM in the conference room.",
            "Thank you for your email. I will review the documents.",
            "Can you send me the project report by Friday?",
            "Looking forward to our discussion next week.",
            "Please find the attached file for your reference.",
            "Happy birthday! Hope you have a wonderful day!",
            "The team lunch is at noon. See you there!"
        ]
        
        for email in spam_samples:
            self.train(email, is_spam=True)
        
        for email in ham_samples:
            self.train(email, is_spam=False)
        
        self.trained = True
    
    def preprocess(self, text):
        """Clean and tokenize text"""
        text = text.lower()
        text = re.sub(f'[{re.escape(string.punctuation)}]', ' ', text)
        words = text.split()
        return [w for w in words if len(w) > 2]
    
    def train(self, text, is_spam):
        """Train classifier with labeled email"""
        words = self.preprocess(text)
        
        if is_spam:
            self.spam_words.update(words)
            self.spam_count += 1
        else:
            self.ham_words.update(words)
            self.ham_count += 1
    
    def classify(self, text):
        """Classify email as spam or ham"""
        if not self.trained:
            return "Unknown", 0.5
        
        words = self.preprocess(text)
        
        # Calculate spam score
        spam_score = 1.0
        ham_score = 1.0
        
        total_spam_words = sum(self.spam_words.values()) + len(self.spam_words)
        total_ham_words = sum(self.ham_words.values()) + len(self.ham_words)
        
        for word in words:
            spam_prob = (self.spam_words.get(word, 0) + 1) / total_spam_words
            ham_prob = (self.ham_words.get(word, 0) + 1) / total_ham_words
            
            spam_score *= spam_prob
            ham_score *= ham_prob
        
        # Normalize
        total = spam_score + ham_score
        spam_probability = spam_score / total if total > 0 else 0.5
        
        result = "SPAM" if spam_probability > 0.5 else "HAM"
        confidence = max(spam_probability, 1 - spam_probability)
        
        return result, confidence

class SpamEmailGUI:
    """GUI for Spam Email Classifier"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Spam Email Classifier")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        self.classifier = SpamClassifier()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            title_frame,
            text="📧 Spam Email Classifier",
            font=("Arial", 18, "bold")
        )
        title_label.pack()
        
        # Input frame
        input_frame = ttk.LabelFrame(self.root, text="Email Content", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.email_input = scrolledtext.ScrolledText(
            input_frame,
            height=10,
            wrap=tk.WORD,
            font=("Arial", 10)
        )
        self.email_input.pack(fill=tk.BOTH, expand=True)
        self.email_input.insert("1.0", "Enter email text here...")
        
        # Buttons frame
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.X)
        
        classify_btn = ttk.Button(
            button_frame,
            text="🔍 Classify Email",
            command=self.classify_email,
            width=20
        )
        classify_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_input,
            width=15
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        train_spam_btn = ttk.Button(
            button_frame,
            text="Train as Spam",
            command=lambda: self.train_email(True),
            width=15
        )
        train_spam_btn.pack(side=tk.LEFT, padx=5)
        
        train_ham_btn = ttk.Button(
            button_frame,
            text="Train as Ham",
            command=lambda: self.train_email(False),
            width=15
        )
        train_ham_btn.pack(side=tk.LEFT, padx=5)
        
        # Result frame
        result_frame = ttk.LabelFrame(self.root, text="Classification Result", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.result_label = ttk.Label(
            result_frame,
            text="No classification yet",
            font=("Arial", 14),
            justify=tk.CENTER
        )
        self.result_label.pack(pady=10)
        
        self.confidence_label = ttk.Label(
            result_frame,
            text="",
            font=("Arial", 11)
        )
        self.confidence_label.pack()
        
        # Status bar
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(
            status_frame,
            text="Ready | Pre-trained model loaded",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, padx=5, pady=2)
    
    def classify_email(self):
        """Classify the email in the input box"""
        email_text = self.email_input.get("1.0", tk.END).strip()
        
        if not email_text or email_text == "Enter email text here...":
            messagebox.showwarning("Warning", "Please enter email text to classify")
            return
        
        result, confidence = self.classifier.classify(email_text)
        
        # Update result display
        if result == "SPAM":
            self.result_label.config(
                text=f"🚨 {result} 🚨",
                foreground="red"
            )
        else:
            self.result_label.config(
                text=f"✅ {result} (Legitimate) ✅",
                foreground="green"
            )
        
        self.confidence_label.config(
            text=f"Confidence: {confidence*100:.1f}%"
        )
        
        self.status_label.config(text=f"Classified as {result}")
    
    def train_email(self, is_spam):
        """Train the classifier with current email"""
        email_text = self.email_input.get("1.0", tk.END).strip()
        
        if not email_text or email_text == "Enter email text here...":
            messagebox.showwarning("Warning", "Please enter email text to train")
            return
        
        self.classifier.train(email_text, is_spam)
        
        label = "spam" if is_spam else "ham"
        messagebox.showinfo(
            "Training Complete",
            f"Email added to training set as {label.upper()}"
        )
        self.status_label.config(text=f"Trained with new {label} example")
    
    def clear_input(self):
        """Clear the input text area"""
        self.email_input.delete("1.0", tk.END)
        self.result_label.config(text="No classification yet", foreground="black")
        self.confidence_label.config(text="")
        self.status_label.config(text="Ready")

def main():
    """Main entry point"""
    root = tk.Tk()
    app = SpamEmailGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
