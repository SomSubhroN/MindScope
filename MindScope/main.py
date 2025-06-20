import tkinter as tk
from gui.main_window import MainWindow
from gui.diagnosis_page import DiagnosisPage
from gui.therapist_page import TherapistPage


class MindScopeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MindScope – Psychological Diagnostic App")
        self.geometry("600x600")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = tk.Frame(self, bg="white")
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for PageClass in (MainWindow, DiagnosisPage, TherapistPage):  # Removed AIChatPage
            page_name = PageClass.__name__
            frame = PageClass(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainWindow")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = MindScopeApp()
    app.mainloop()
