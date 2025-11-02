#!/usr/bin/env python3
"""
Customer Support Chatbot - Single file GUI
- FAQ keywords + ticket creation (CSV) + simple sentiment
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import csv, os, datetime

FAQ = {
    "refund": "To request a refund, please provide your order ID. Refunds take 5-7 days.",
    "shipping": "Standard shipping takes 3-5 business days. Express is 1-2 days.",
    "order": "You can track your order in the Orders section using your email.",
    "cancel": "Orders can be canceled within 2 hours of placement from your account.",
    "password": "Use 'Forgot Password' on the login page to reset your password.",
}

POS = {"good","great","awesome","love","thanks","thank you","perfect"}
NEG = {"bad","terrible","angry","hate","problem","issue","late","delay"}

class SupportBot:
    def answer(self, text:str)->str:
        low = text.lower()
        for k,v in FAQ.items():
            if k in low:
                return v
        score = sum(1 for w in POS if w in low) - sum(1 for w in NEG if w in low)
        if score < 0:
            return "I'm sorry for the trouble. I can create a support ticket for you."
        if score > 0:
            return "Glad to hear that! How else can I help?"
        if low.endswith("?"):
            return "Great question. Could you share your order ID or more details?"
        return "I can help with refunds, shipping, orders, and accounts. What happened?"

class SupportGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Support Chatbot")
        self.root.geometry("760x520")
        self.bot = SupportBot()
        self.build()

    def build(self):
        top = ttk.Frame(self.root, padding=8)
        top.pack(fill=tk.BOTH, expand=True)

        self.chat = scrolledtext.ScrolledText(top, wrap=tk.WORD, state=tk.DISABLED)
        self.chat.pack(fill=tk.BOTH, expand=True)

        form = ttk.Frame(self.root, padding=8)
        form.pack(fill=tk.X)
        self.entry = ttk.Entry(form)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind('<Return>', self.send)
        ttk.Button(form, text="Send", command=self.send).pack(side=tk.LEFT, padx=6)
        ttk.Button(form, text="Create Ticket", command=self.create_ticket).pack(side=tk.LEFT)

        self.write("bot", "Hi! I'm your support assistant. Ask me anything.")

    def write(self, who, text):
        self.chat.config(state=tk.NORMAL)
        prefix = "You" if who=="user" else "Support"
        self.chat.insert(tk.END, f"{prefix}: {text}\n")
        self.chat.config(state=tk.DISABLED)
        self.chat.see(tk.END)

    def send(self, event=None):
        msg = self.entry.get().strip()
        if not msg:
            return
        self.entry.delete(0, tk.END)
        self.write("user", msg)
        self.write("bot", self.bot.answer(msg))

    def create_ticket(self):
        last = self.chat.get('1.0', tk.END).strip().splitlines()
        desc = last[-1] if last else "Issue reported by user"
        os.makedirs('tickets', exist_ok=True)
        path = os.path.join('tickets', 'tickets.csv')
        new = not os.path.exists(path)
        with open(path, 'a', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            if new:
                w.writerow(["ticket_id","created_at","description"])
            tid = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            w.writerow([tid, datetime.datetime.now().isoformat(timespec='seconds'), desc])
        messagebox.showinfo("Ticket Created", f"Your ticket ID is {tid}")


def main():
    root = tk.Tk()
    app = SupportGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
