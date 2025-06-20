import tkinter as tk
from tkinter import Canvas, Scrollbar
from datetime import datetime
import os
import random

# Create directory to store conversations
if not os.path.exists("logs"):
    os.makedirs("logs")
log_file = os.path.join("logs", "support.txt")

# Predefined empathetic and supportive responses
empathy_bank = [
    ("sad", [
        "I'm here for you. Want to talk about what's making you feel this way?",
        "You're not alone. It's okay to feel this way sometimes.",
        "Would you like me to guide you through a calming exercise?"
    ]),
    ("angry", [
        "It’s alright to feel frustrated. Can you help me understand what happened?",
        "Anger is a valid emotion. Want to vent it out here?",
        "Let’s try to take a deep breath together."
    ]),
    ("alone", [
        "You matter. And I’m right here, listening.",
        "Even in silence, you’re not invisible. Talk to me.",
        "Feeling alone hurts — but I’m proud you reached out."
    ]),
    ("worthless", [
        "Your worth isn't measured by your worst days.",
        "You’re stronger than you think. I believe in you.",
        "Please consider speaking to a psychologist. You deserve support."
    ])
]

class AIChatPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        tk.Label(self, text="💬 24x7 AI Chat Support", font=("Arial", 18, "bold"), bg="white", fg="#3f51b5").pack(pady=10)

        self.canvas = Canvas(self, bg="white")
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.scrollbar.pack(side="right", fill="y")

        self.entry = tk.Entry(self, font=("Arial", 13), width=70, bg="#ffffff")
        self.entry.pack(padx=10, pady=(0, 10), side=tk.LEFT, expand=True, fill='x')
        self.entry.bind("<Return>", self.process_user_message)

        send_btn = tk.Button(self, text="Send", font=("Arial", 12, "bold"), bg="#4caf50", fg="white", command=self.process_user_message)
        send_btn.pack(padx=5, pady=(0, 10), side=tk.RIGHT)

        back_btn = tk.Button(self, text="🔙 Back", font=("Arial", 12), bg="#616161", fg="white", command=lambda: controller.show_frame("MainWindow"))
        back_btn.pack(pady=(5, 10))

    def process_user_message(self, event=None):
        user_msg = self.entry.get().strip()
        if not user_msg:
            return

        self.add_chat_bubble("🧑 You", user_msg, align='right', bubble_color="#e0f7fa")
        self.entry.delete(0, tk.END)

        response = self.generate_response(user_msg)
        self.add_chat_bubble("🤖 MindBot", response, align='left', bubble_color="#ede7f6")
        self.save_conversation(user_msg, response)

    def generate_response(self, message):
        msg_lower = message.lower()
        for keyword, responses in empathy_bank:
            if keyword in msg_lower:
                response = random.choice(responses)
                if "psychologist" in response:
                    response += "\nWould you like me to show you therapists nearby?"
                return response
        # Fallback generic response
        return "I'm listening. Feel free to share more about how you're feeling."

    def add_chat_bubble(self, sender, message, align='left', bubble_color="#f0f0f0"):
        bubble = tk.Frame(self.scrollable_frame, bg=bubble_color, padx=10, pady=5, bd=1, relief="solid")
        tk.Label(bubble, text=sender, font=("Arial", 10, "bold"), bg=bubble_color, anchor="w").pack(anchor="w")
        tk.Label(bubble, text=message, font=("Arial", 11), bg=bubble_color, wraplength=400, justify="left").pack(anchor="w")

        if align == 'right':
            bubble.pack(anchor="e", pady=5, padx=10)
        else:
            bubble.pack(anchor="w", pady=5, padx=10)

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def save_conversation(self, user, bot):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, "a", encoding='utf-8') as f:
            f.write(f"\n[{timestamp}]\nYou: {user}\nMindBot: {bot}\n")