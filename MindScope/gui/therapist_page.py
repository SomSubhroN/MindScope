import tkinter as tk
from tkinter import ttk
import pandas as pd
import webbrowser

class TherapistPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        tk.Label(self, text="🧑‍⚕️ Therapists Near You", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

        # Dropdown for cities
        self.city_var = tk.StringVar()
        self.city_dropdown = ttk.Combobox(self, textvariable=self.city_var, state="readonly", width=30)
        self.city_dropdown.pack(pady=5)

        self.city_dropdown.bind("<<ComboboxSelected>>", self.filter_by_city)

        # Scrollable frame setup
        canvas = tk.Canvas(self, bg="white", height=450)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Load therapist data
        self.load_therapists()

        # Back button
        tk.Button(self, text="🔙 Back", font=("Arial", 12), bg="#616161", fg="white",
                  command=lambda: controller.show_frame("DiagnosisPage")).pack(pady=10)

    def load_therapists(self):
        try:
            self.df = pd.read_csv("gui/therapists.csv")
            cities = sorted(self.df['City'].dropna().unique())
            self.city_dropdown['values'] = cities
            if cities:
                self.city_var.set(cities[0])
                self.filter_by_city()
        except Exception as e:
            print("Error reading CSV:", e)
            self.df = pd.DataFrame()
            tk.Label(self.scrollable_frame, text="Error loading therapist data.", fg="red", bg="white").pack()

    def filter_by_city(self, event=None):
        selected_city = self.city_var.get()
        filtered_df = self.df[self.df['City'] == selected_city]
        self.display_therapists(filtered_df)

    def display_therapists(self, df):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if df.empty:
            tk.Label(self.scrollable_frame, text="No therapists found for this city.", bg="white").pack()
            return

        for _, row in df.iterrows():
            name = str(row.get("Name", "N/A")).strip()
            city = str(row.get("City", "N/A")).strip()
            specialty = str(row.get("Specialty", "N/A")).strip()
            whatsapp_raw = row.get("WhatsApp", "")
            whatsapp = str(int(float(whatsapp_raw))) if pd.notna(whatsapp_raw) else ""


            frame = tk.Frame(self.scrollable_frame, bg="#f1f1f1", pady=8, padx=8, bd=1, relief="solid")
            frame.pack(fill="x", pady=5, padx=10)

            tk.Label(frame, text=f"👩‍⚕️ {name}", font=("Arial", 12, "bold"), bg="#f1f1f1").pack(anchor="w")
            tk.Label(frame, text=f"🏙️ City: {city}", bg="#f1f1f1").pack(anchor="w")
            tk.Label(frame, text=f"🧠 Specialty: {specialty}", bg="#f1f1f1").pack(anchor="w")

            # ✅ Display mobile number
            if whatsapp:
                tk.Label(frame, text=f"📞 Mobile: {whatsapp}", bg="#f1f1f1", fg="blue", font=("Arial", 10, "bold")).pack(anchor="w", pady=(3, 0))
                tk.Button(frame, text="📲 Message on WhatsApp", bg="#25D366", fg="white",
                          command=lambda number=whatsapp: self.open_whatsapp(number)).pack(anchor="e", pady=5)
            else:
                tk.Label(frame, text="❌ No WhatsApp number available", fg="red", bg="#f1f1f1").pack(anchor="e")

    def open_whatsapp(self, number):
        link = f"https://wa.me/{int(str("+91"+number))}"
        webbrowser.open(link)
