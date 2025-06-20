import tkinter as tk
from tkinter import messagebox
import threading
import pyttsx3
import cv2
from fer import FER
import speech_recognition as sr
from transformers import pipeline
import datetime

# Load HuggingFace text emotion model
emotion_nlp = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion", framework="pt")

# Initialize TTS
engine = pyttsx3.init()


class DiagnosisPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        self.title_label = tk.Label(self, text="🧠 Mental Health Diagnostic", font=("Arial", 18, "bold"), bg="white")
        self.title_label.pack(pady=20)

        self.result_label = tk.Label(self, text="", font=("Arial", 14), bg="white", justify="left")
        self.result_label.pack(pady=20)

        tk.Button(
            self, text="Run Diagnosis",
            font=("Arial", 14), bg="#388e3c", fg="white",
            command=self.run_diagnosis_threaded
        ).pack(pady=10)

        tk.Button(
            self, text="Back to Home",
            font=("Arial", 14), bg="#616161", fg="white",
            command=lambda: controller.show_frame("MainWindow")
        ).pack(pady=10)

    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

    def run_diagnosis_threaded(self):
        threading.Thread(target=self.run_diagnosis).start()

    def run_diagnosis(self):
        full_report = []

        self.title_label.config(text="📷 Detecting Facial Emotion...")
        facial_emotion = self.detect_facial_emotion()
        full_report.append(f"😐 Facial Emotion: {facial_emotion}")

        self.title_label.config(text="🎤 Listening to Your Voice...")
        user_text = self.capture_user_voice()

        self.title_label.config(text="🤖 Analyzing Voice Emotion...")
        emotion_result = self.analyze_emotion_from_text(user_text)
        voice_emotion = emotion_result[0]['label']
        voice_conf = float(emotion_result[0]['score'])
        full_report.append(f"🗣️ Voice Emotion: {voice_emotion} ({round(voice_conf * 100, 2)}%)")

        base_stress = self.calculate_stress_score(facial_emotion, voice_emotion, voice_conf)

        # Ask 3 mental health questions
        qna_stress, answers = self.ask_mental_health_questions()
        full_report.append("🧠 QnA Stress Add-on: " + str(round(qna_stress, 2)))

        final_stress = min(100, base_stress + qna_stress)
        full_report.append(f"📊 Final Stress Score: {round(final_stress)}/100")

        self.result_label.config(text="\n".join(full_report))

        self.save_report("\n".join(full_report) + "\n\nAnswers:\n" + "\n".join(answers))

        if final_stress >= 50:
            self.speak("Your stress levels are concerning. Please consult a therapist.")
            messagebox.showinfo("Urgent Attention", "High stress detected. Redirecting to therapist page.")
            self.controller.show_frame("TherapistPage")
        else:
            self.speak("You're emotionally stable. Stay positive and take care!")

    def detect_facial_emotion(self):
        try:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()
            if not ret:
                return "neutral"

            detector = FER(mtcnn=True)
            results = detector.detect_emotions(frame)
            if results:
                emotions = results[0]["emotions"]
                return max(emotions, key=emotions.get)
            else:
                return "neutral"
        except Exception as e:
            print("Facial detection error:", e)
            return "neutral"

    def capture_user_voice(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.speak("Tell me how you’ve been feeling lately.")
            try:
                audio = recognizer.listen(source, timeout=10)
                text = recognizer.recognize_google(audio)
                return text
            except Exception as e:
                print("Speech recognition error:", e)
                return "I don't know how I feel."

    def analyze_emotion_from_text(self, text):
        try:
            return emotion_nlp(text)
        except Exception as e:
            print("Transformer error:", e)
            return [{"label": "neutral", "score": 0.5}]

    def ask_mental_health_questions(self):
        questions = [
            "Do you often feel overwhelmed or hopeless?",
            "Have you lost interest in things you once enjoyed?",
            "Are you having trouble sleeping or feeling restless?",
            "Do you feel supported by the prople around you?",
            "Do you feel palpitations?",
            "Do you have unexplained body pain?",
            "Do you feel lethargic?",
            "Do you have unexplained bloating?",
            "Do you have trembling?",
            "Do you have respiratory distress?"
        ]
        stress = 0
        answers = []

        for q in questions:
            self.speak(q)
            self.title_label.config(text=q)
            answer = self.capture_user_voice()
            answers.append(f"Q: {q}\nA: {answer}")
            try:
                analysis = emotion_nlp(answer)
                if analysis:
                    label = analysis[0]["label"].lower()
                    score = float(analysis[0]["score"])
                    if label in ["sadness", "anger", "fear"]:
                        stress += score * 10
                    elif label == "neutral":
                        stress += 3
                    else:
                        stress += 1
            except Exception as e:
                print("Error during QnA analysis:", e)
                stress += 5  # mild stress fallback

        return stress, answers

    def calculate_stress_score(self, face_emotion, voice_emotion, score):
        stress = 0

        if face_emotion.lower() in ['angry', 'sad', 'fear', 'disgust']:
            stress += 30
        elif face_emotion.lower() == 'neutral':
            stress += 10
        else:
            stress += 5

        if voice_emotion.lower() in ['anger', 'sadness', 'fear']:
            stress += int(score * 50)
        elif voice_emotion.lower() == 'neutral':
            stress += 10
        else:
            stress += 5

        return min(100, stress)

    def save_report(self, text):
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"Report_{now}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
