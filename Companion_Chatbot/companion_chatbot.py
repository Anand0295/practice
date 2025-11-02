#!/usr/bin/env python3
"""
Companion Chatbot - Single file minimal GUI
- Simple rule-based + context memory
- tkinter chat window with input box
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime

class CompanionBot:
    def __init__(self):
        self.memory = []  # list of (role, text)
        self.name = "Companion"

    def reply(self, text: str) -> str:
        t = text.strip()
        self.memory.append(("user", t))
        lower = t.lower()
        # simple intents
        if any(g in lower for g in ["hello", "hi", "hey"]):
            ans = "Hello! How can I support you today?"
        elif "time" in lower:
            ans = f"It's {datetime.now().strftime('%H:%M on %A, %d %b %Y')}"
        elif "name" in lower:
            ans = f"I'm {self.name}, your friendly companion chatbot."
        elif "remember" in lower:
            ans = "I will remember that."
        elif "help" in lower:
            ans = "I can chat, keep short memory, and offer friendly support."
        elif lower.endswith("?"):
            ans = "That's a good question! What do you think about it?"
        else:
            # echo with empathy
            ans = "I hear you. Tell me more."
        self.memory.append(("bot", ans))
        return ans

class ChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Companion Chatbot")
        self.root.geometry("700x500")
        self.bot = CompanionBot()
        self.build()

    def build(self):
        top = ttk.Frame(self.root, padding=8)
        top.pack(fill=tk.BOTH, expand=True)

        self.chat = scrolledtext.ScrolledText(top, wrap=tk.WORD, state=tk.DISABLED)
        self.chat.pack(fill=tk.BOTH, expand=True)

        bottom = ttk.Frame(self.root, padding=8)
        bottom.pack(fill=tk.X)

        self.entry = ttk.Entry(bottom)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind('<Return>', self.send)

        ttk.Button(bottom, text="Send", command=self.send).pack(side=tk.LEFT, padx=6)
        ttk.Button(bottom, text="Clear", command=self.clear).pack(side=tk.LEFT)

        self.write("bot", "Hello! I'm here to chat.")

    def write(self, who, text):
        self.chat.config(state=tk.NORMAL)
        prefix = "You" if who == "user" else "Companion"
        self.chat.insert(tk.END, f"{prefix}: {text}\n")
        self.chat.config(state=tk.DISABLED)
        self.chat.see(tk.END)

    def send(self, event=None):
        msg = self.entry.get().strip()
        if not msg:
            return
        self.entry.delete(0, tk.END)
        self.write("user", msg)
        ans = self.bot.reply(msg)
        self.write("bot", ans)

    def clear(self):
        self.chat.config(state=tk.NORMAL)
        self.chat.delete('1.0', tk.END)
        self.chat.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = ChatGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
