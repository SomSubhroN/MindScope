import tkinter as tk

class MainWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.configure(bg="#f7f7f7")

        tk.Label(
            self,
            text="🧠 Welcome to MindScope",
            font=("Helvetica", 20, "bold"),
            bg="#f7f7f7",
            fg="#333"
        ).pack(pady=40)

        tk.Button(
            self,
            text="Start Diagnosis",
            font=("Helvetica", 14),
            width=20,
            bg="#4caf50",
            fg="white",
            command=lambda: controller.show_frame("DiagnosisPage")
        ).pack(pady=15)

        tk.Button(
            self,
            text="View Therapists",
            font=("Helvetica", 14),
            width=20,
            bg="#2196f3",
            fg="white",
            command=lambda: controller.show_frame("TherapistPage")
        ).pack(pady=15)

        tk.Button(
            self,
            text="Exit",
            font=("Helvetica", 14),
            width=20,
            bg="#f44336",
            fg="white",
            command=self.quit
        ).pack(pady=15)
