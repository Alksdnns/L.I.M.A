# reminder_checker.py
import json
import time
from datetime import datetime
from threading import Thread
from pyttsx3 import init as tts_init

engine = tts_init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

class ReminderChecker(Thread):
    def __init__(self, filename="reminders.json", check_interval=10):
        super().__init__(daemon=True)
        self.filename = filename
        self.check_interval = check_interval
        self.running = True

    def run(self):
        while self.running:
            try:
                with open(self.filename, "r") as f:
                    reminders = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                reminders = []

            now = datetime.now()
            updated_reminders = []

            for r in reminders:
                remind_time = datetime.strptime(r["time"], "%Y-%m-%d %H:%M:%S")
                if now >= remind_time:
                    print(f"[🔔] Reminder: {r['text']}")
                    speak(f"Reminder: {r['text']}")
                else:
                    updated_reminders.append(r)

            # Save back only pending reminders
            with open(self.filename, "w") as f:
                json.dump(updated_reminders, f, indent=4)

            time.sleep(self.check_interval)

    def stop(self):
        self.running = False
