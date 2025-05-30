import sys
import pyttsx3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QApplication
import webbrowser
from modules.llama_engine import LLaMAChat
from modules.intent import IntentDetector
from modules.openhandler import Open
from modules.multitreading import MultithreadingModule
import socket
import speech_recognition as sr
from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
from pathlib import Path
import sounddevice as sd
import scipy.io.wavfile as wav
import random
import os
import time
from modules.task import example_task
from modules.musicplayer import MusicPlayer
import pyttsx3
import requests
from bs4 import BeautifulSoup
import datetime
import pyautogui
import keyboard
from modules.keyboad import volumeup, volumedown, volumeuptwice, volumedowntwice
from modules.status import get_system_status, get_ram_status, get_battery_status, get_disk_status
import re
from modules.weather_report import get_weather_report
from modules.schedulaer import AssistantScheduler
from modules.save_reminder import save_reminder
from modules.reminderextracter import parse_reminder_command
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout,
    QPushButton, QWidget
)
from PyQt5.QtGui import QFont, QIcon, QPainter, QColor
from PyQt5.QtCore import Qt, QSize, QTimer
from modules.reminder_checker import ReminderChecker

import threading
from threading import Lock

REMINDER_LOCK = Lock()

class HybridRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def is_connected(self):
        try:
            socket.create_connection(("www.google.com", 80), 2)
            return True
        except OSError:
            return False

    def recognize(self, audio_data):
        if self.is_connected():
            try:
                print("\U0001F310 Using Google Speech Recognition")
                result = self.recognizer.recognize_google(audio_data)
                if result.strip():
                    return result
                else:
                    print("\u26A0\uFE0F Google returned empty result.")
            except Exception as e:
                print(f"\u26A0\uFE0F Google failed: {e}.")
        print("\u274C Speech recognition failed.")
        return "Speech recognition failed."

class VoiceAuthenticator:
    def __init__(self):
        self.encoder = VoiceEncoder()
        self.user_embeddings = []
        self.user_folder = Path(r"C:\Users\ToshiTzudir\OneDrive\Desktop\logical interactive monitoring assistant\user_voices")
        self.user_folder.mkdir(exist_ok=True)
        self.load_existing_users()

    def load_existing_users(self):
        for file in self.user_folder.glob("user_*.wav"):
            wav_data = preprocess_wav(str(file))
            embedding = self.encoder.embed_utterance(wav_data)
            self.user_embeddings.append((file.stem, embedding))
        print(f"Loaded {len(self.user_embeddings)} user(s) for voice authentication.")

    def add_new_user(self, wav_fpath):
        wav_data = preprocess_wav(str(wav_fpath))
        embedding = self.encoder.embed_utterance(wav_data)
        user_id = wav_fpath.stem
        self.user_embeddings.append((user_id, embedding))
        print(f"Added new user: {user_id}")

    def verify_speaker(self, audio_path, threshold=0.6):
        wav_data = preprocess_wav(str(audio_path))
        query_embedding = self.encoder.embed_utterance(wav_data)

        if not self.user_embeddings:
            print("No users registered yet.")
            return False, None

        def cosine_similarity(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

        best_match = None
        best_score = -1
        for user_id, emb in self.user_embeddings:
            score = cosine_similarity(query_embedding, emb)
            if score > best_score:
                best_score = score
                best_match = user_id

        print(f"Best similarity score: {best_score:.3f} for user {best_match}")
        return (best_score >= threshold), best_match if best_score >= threshold else None

def record_and_save_user_voice(duration=5):
    print("\U0001F3A4 Recording your voice sample for 5 seconds...")
    fs = 16000
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    user_folder = Path(r"C:\\Users\\ToshiTzudir\\OneDrive\\Desktop\\logical interactive monitoring assistant\\user_voices")
    user_folder.mkdir(exist_ok=True)

    existing_files = list(user_folder.glob("user_*.wav"))
    next_num = len(existing_files) + 1
    filename = user_folder / f"user_{next_num}.wav"

    wav.write(str(filename), fs, recording)
    print(f"\u2705 Voice recorded and saved as {filename}")
    return filename

class VoiceVisualizer(QWidget):
    def __init__(self, bar_count=30):
        super().__init__()
        self.bar_count = bar_count
        self.bar_heights = [random.randint(10, 80) for _ in range(bar_count)]
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_bars)
        self.timer.start(100)  # update every 100ms
        self.setMinimumHeight(120)

    def update_bars(self):
        self.bar_heights = [random.randint(10, 80) for _ in range(self.bar_count)]
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        bar_width = self.width() / (self.bar_count * 1.5)
        spacing = bar_width / 2
        x = spacing
        color = QColor("#00ffe1")
        painter.setPen(Qt.NoPen)
        painter.setBrush(color)

        for height in self.bar_heights:
            y = (self.height() - height) / 2
            painter.drawRoundedRect(int(x), int(y), int(bar_width), int(height), 2, 2)
            x += bar_width + spacing

# --- Main GUI Assistant ---
class VoiceGUIAssistant(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize core components FIRST
        model_path = r"C:\Users\ToshiTzudir\OneDrive\Desktop\logical interactive monitoring assistant\llama.cpp\models\llama-2-7b-chat.Q3_K_M.gguf"
        self.llama = LLaMAChat(model_path=model_path)
        self.intent_detector = IntentDetector()
        self.tts_engine = pyttsx3.init()
        self.file_opener = Open()
        self.multitasker = MultithreadingModule()
        self.hybrid_recognizer = HybridRecognizer()
        self.voice_authenticator = VoiceAuthenticator()
        self.music_player = MusicPlayer()
        self.current_user = None
        self.is_task_running = False
        self.scheduler = AssistantScheduler(self.speak)
        self.scheduler.lock = REMINDER_LOCK

        # Build the UI
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('🧠 Voice GUI Assistant')
        self.setGeometry(100, 100, 400, 500)
        self.setStyleSheet("background-color: #121212; color: white;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Welcome Label
        self.label = QLabel("Welcome to LIMA, your AI Assistant")
        self.label.setFont(QFont("Segoe UI", 14))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Animated Frequency Visualizer
        self.visualizer = VoiceVisualizer(bar_count=35)
        layout.addWidget(self.visualizer)

        # Microphone Button
        self.mic_button = QPushButton()
        self.mic_button.setIcon(QIcon("assets/mic.png"))  # Make sure this path is correct
        self.mic_button.setIconSize(QSize(48, 48))
        self.mic_button.setFixedSize(80, 80)
        self.mic_button.setStyleSheet("""
            QPushButton {
                border: 2px solid #00ffe1;
                border-radius: 40px;
                background-color: #1f1f1f;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
            }
        """)
        layout.addWidget(self.mic_button, alignment=Qt.AlignCenter)

        # Set layout to central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.show()

        # Speak intro and start command loop
        self.speak("Hello, I am your virtual assistant. How may I help you today?")
        threading.Thread(target=self.command_loop, daemon=True).start()

    def listen(self, timeout=5, phrase_time_limit=4):
        """Listen to microphone input and return recognized text."""
        with sr.Microphone() as source:
            self.label.setText("🎙️ Listening for input...")
            try:
                audio = self.hybrid_recognizer.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            except sr.WaitTimeoutError:
                self.speak("I didn't hear anything.")
                return None
        recognized_text = self.hybrid_recognizer.recognize(audio)
        print(f"[🎧] Heard: {recognized_text}")
        return recognized_text

    def handle_new_user_registration(self):
        self.speak("Please say the password.")
        with sr.Microphone() as source:
            try:
                audio_password = self.hybrid_recognizer.recognizer.listen(
                    source, 
                    timeout=5,
                    phrase_time_limit=3
                )
            except sr.WaitTimeoutError:
                self.speak("I didn't hear the password.")
                return

        password = self.hybrid_recognizer.recognize(audio_password)
        print(f"[🔑] Password received: {password}")

        if password.strip() == "112233":
            self.speak("Password verified. Please say your voice sample after the beep.")
            new_voice_path = record_and_save_user_voice()
            self.voice_authenticator.add_new_user(new_voice_path)
            self.speak("New user registered and ready to go.")
            self.speak("Please say the wake word 'HAiLIMA' to authenticate.")
            self.command_loop()
        else:
            self.speak("Incorrect password. Registration failed.")

    def command_loop(self):
        # Step 1: Voice authentication with timeout
        self.speak("Please say the wake word 'HAiLIMA' to authenticate.")
        with sr.Microphone() as source:
            self.label.setText("🎙️ Listening for authentication...")
            try:
                audio = self.hybrid_recognizer.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=3
                )
            except sr.WaitTimeoutError:
                self.speak("No wake word detected. Please try again.")
                return

        temp_wav_path = Path("temp_auth.wav")
        with open(temp_wav_path, "wb") as f:
            f.write(audio.get_wav_data())

        auth_command = self.hybrid_recognizer.recognize(audio)
        if auth_command.lower().startswith("halima"):
            verified, user_id = self.voice_authenticator.verify_speaker(temp_wav_path)
            if not verified:
                self.speak("Voice not recognized. Say 'register me' to add your voice.")
                with sr.Microphone() as source:
                    try:
                        audio = self.hybrid_recognizer.recognizer.listen(
                            source,
                            timeout=5,
                            phrase_time_limit=3
                        )
                    except sr.WaitTimeoutError:
                        self.speak("Registration request timed out.")
                        return
                response = self.hybrid_recognizer.recognize(audio)
                if "register" in response.lower():
                    self.handle_new_user_registration()
                    return
                else:
                    return
            else:
                self.current_user = user_id
                print(f"[✅] Verified user: {user_id}")
                self.speak(f"Welcome {user_id}, voice authentication successful.")
        else:
            self.speak("Please say the wake word 'LIMA' to authenticate.")
            return

        # Step 2: Main command loop with timeouts
        while True:
            with sr.Microphone() as source:
                self.label.setText("🎙️ Listening for voice commands...")
                try:
                    audio = self.hybrid_recognizer.recognizer.listen(
                        source,
                        timeout=3,
                        phrase_time_limit=5
                    )
                except sr.WaitTimeoutError:
                    print("No command detected, listening again...")
                    continue

            try:
                command = self.hybrid_recognizer.recognize(audio)
                if command == "Speech recognition failed.":
                    self.speak("Sir, would you repeat again?")
                    continue

                print(f"[✔] Recognized command: {command}")
                self.label.setText(f"🗣️ Recognized: {command}")

                cmd_lower = command.lower().strip()
                if cmd_lower.startswith("lima"):
                    stripped_command = command[4:].strip(", ").strip()
                    self.process_speech_command(stripped_command)
                else:
                    print("[⏭️] Command does not start with LIMA. Ignored.")
                    continue

            except Exception as e:
                self.label.setText("❌ Sorry, I couldn't understand.")
                print(f"[ERROR] Recognition error: {e}")

    def speak(self, text):
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
        print(f"Speaking: {text}")

    def process_speech_command(self, command):
        filtered_command = command.lower().strip()
        intent_result = self.intent_detector.classify(filtered_command)
        filtered_command = self.filter_input(command)
        print(f"[🧹] Filtered Command: {filtered_command}")

        intent = self.intent_detector.classify(filtered_command)
        print(f"[🎯] Detected Intent: {intent}")
        if isinstance(intent_result, tuple):
            intent, direction = intent_result
        else:
            intent, direction = intent_result, None

        if intent == "register_user":
            self.handle_new_user_registration()
            return

        reminder_text, remind_time = parse_reminder_command(command)
        if reminder_text and remind_time:
            success = save_reminder(reminder_text, remind_time)
            if success:
                self.scheduler.add_reminder(  # Directly notify the scheduler
                    reminder_text,
                    remind_time,
                    lambda text: self.speak(f"Reminder: {text}")
                )
                self.speak(f"Reminder set for {remind_time.strftime('%I:%M %p')}")
            else:
                self.speak("Failed to save reminder.")
        else:
            # Normal command processing here
            self.speak(f"Command received: {command}")

        if intent == "set_reminder":
            reminder_text, remind_time = parse_reminder_command(command)
            if reminder_text and remind_time:
                # Clean the reminder text by removing trigger phrases
                clean_text = reminder_text
                for phrase in self.intent_detector.scheduler_phrases:
                    clean_text = clean_text.replace(phrase, "").strip()
                
                # Add to scheduler with special flag
                success = self.scheduler.add_reminder(
                    clean_text,
                    remind_time,
                    is_reminder_command=True
                )
                
                if success:
                    time_str = remind_time.strftime('%I:%M %p').lstrip('0')
                    self.speak(f"Reminder set for {time_str}")
                    self.label.setText(f"Reminder: {clean_text} at {time_str}")
                else:
                    self.speak("Failed to set reminder")
            else:
                self.speak("Please specify both a reminder and time")
                # Visual confirmation in GUI
                self.label.setText(f"Reminder set for {time_str}: {reminder_text}")

        if intent in ["stop", "cancel"]:
            self.stop_task()
            self.label.setText("🟥 Task stopped.")
            self.speak("Stopping current task.")
            return
        if intent == "do_task":
            for trigger in self.intent_detector.task_phrases:
                if trigger in filtered_command:
                    file_name = filtered_command.replace(trigger, '').strip()
                    break
            else:
                file_name = filtered_command

            if file_name:
                file_type = self.ask_file_type(file_name)
                if file_type:
                    self.file_opener.ask_and_launch(file_name, file_type)
                else:
                    self.speak("I could not understand the file type.")
            return
        if intent == "get_weather":
            # Extract location if specified (e.g. "weather in London")
            location = None
            if "weather in" in command.lower():
                location = command.lower().split("weather in")[-1].strip()
            
            # Single function call
            weather_report = get_weather_report(location)
            self.speak(weather_report)
            self.label.setText(weather_report)

        if intent.startswith("open_"):
            app_name = intent.replace("open_", "")
            file_type = self.ask_file_type(app_name)
            if file_type:
                self.file_opener.ask_and_launch(app_name, file_type)
            else:
                self.speak("I could not understand the file type.")
            return
        
        if intent == "chat_ai":
            response = self.llama.chat(filtered_command)
            self.speak(response)
            self.label.setText(response)

        
        elif intent == "search_web":
            query = filtered_command
            for word in self.intent_detector.intent_keywords.get("search_web", []):
                query = query.replace(word, "").strip()
            self.speak(f"Searching the web for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return

        if intent == "open_youtube":
            self.open_youtube()
            return
        if intent == "get_battery_status":
            battery = get_battery_status()
            self.speak(battery)
            return

        elif intent == "get_ram_status":
            ram = get_ram_status()
            self.speak(ram)
            return
        if intent == "none":  # No intent matched
           self.speak("Sir, can you repeat again? Or I am unable to understand the command. Try using some other phrase.")

        elif intent == "get_disk_status":
            disk = get_disk_status()
            self.speak(disk)
            return

        elif intent == "get_system_status":
            full_status = get_system_status()
            self.speak(full_status)
            return
        if intent == "play_song":
            self.ask_for_music_app()
            return
        
        if intent == "play_music":
            if "spotify" in filtered_command:
                song = filtered_command.replace("spotify", "").replace("play", "").strip()
                self.music_player.play_on_spotify(song)
                self.speak(f"Playing {song} on Spotify.")
            else:
                song = filtered_command.replace("play", "").strip()
                self.music_player.play_on_youtube(song)
                self.speak(f"Playing {song} on YouTube.")
        if intent == "control_volume":
            # Check for volume up/down keywords in the original command (case-insensitive)
            if direction == "up":
                volumeup()
                self.speak("Turning volume up")
            elif direction == "down":
                volumedown()
                self.speak("Turning volume down")
            else:
                self.speak("Please specify whether to turn volume up or down")
                return
        if intent == "pause_play":
            keyboard.press_and_release('space')
            self.speak("Video paused" if "post" "pause" in filtered_command else "Video playing")
            return
        if intent == "play_full_screen":
            keyboard.press_and_release('f')
            self.speak("Switching to full screen")
            return
        if intent == "skip":
            keyboard.press_and_release('tab')
            self.speak("Skipping")
            return

    def ask_file_type(self, file_name):
        with sr.Microphone() as source:
            try:
                audio = self.hybrid_recognizer.recognizer.listen(
                    source,
                    timeout=3,
                    phrase_time_limit=3
                )
            except sr.WaitTimeoutError:
                self.speak("I didn't hear the file type.")
                return None
        file_type = self.hybrid_recognizer.recognize(audio)
        print(f"[📂] File type: {file_type}")
        return file_type.lower()

    def ask_for_music_app(self):
        self.speak("Which music player would you like to use?")
        with sr.Microphone() as source:
            try:
                audio = self.hybrid_recognizer.recognizer.listen(
                    source,
                    timeout=3,
                    phrase_time_limit=3
                )
            except sr.WaitTimeoutError:
                self.speak("I didn't hear your choice.")
                return
        music_app = self.hybrid_recognizer.recognize(audio)
        print(f"[🎵] Music app: {music_app}")
        self.file_opener.search_and_launch(music_app)

    def open_youtube(self):
        self.speak("Opening YouTube...")
        webbrowser.open("https://www.youtube.com")

    def filter_input(self, text):
        text = text.lower().strip()
        return text

    def stop_task(self):
        if self.is_task_running:
            self.multitasker.stop_all()
            self.is_task_running = False
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    assistant = VoiceGUIAssistant()
    assistant.show()
    try:
        sys.exit(app.exec_())
    finally:
        assistant.scheduler.stop()  # Clean up the scheduler thread