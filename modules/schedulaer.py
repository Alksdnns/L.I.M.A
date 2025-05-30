import json
import threading
import time
from datetime import datetime
from threading import Lock

class AssistantScheduler:
    def __init__(self, speak_callback, filename="reminders.json", check_interval=10):
        self.speak = speak_callback
        self.filename = filename
        self.check_interval = check_interval
        self.running = False
        self.thread = None
        self.reminders = []
        self.lock = Lock()
        self._load_reminders()

    def _load_reminders(self):
        """Load existing reminders from file"""
        with self.lock:
            try:
                with open(self.filename, 'r') as f:
                    reminders = json.load(f)
                    # Convert string times back to datetime objects
                    for r in reminders:
                        try:
                            r['time'] = datetime.strptime(r['time'], "%Y-%m-%d %H:%M:%S")
                            self.reminders.append({
                                'text': r['text'],
                                'time': r['time'],
                                'callback': lambda t=r['text']: self.speak(f"🔔 Reminder: {t}")
                            })
                        except:
                            continue
            except (FileNotFoundError, json.JSONDecodeError):
                pass

    def add_reminder(self, text, time, is_reminder_command=False):
        """Add and persist a new reminder"""
        with self.lock:
            try:
                # Create appropriate callback based on command type
                if is_reminder_command:
                    callback = lambda t=text: self.speak(f"Sir, you need to {t}")
                else:
                    callback = lambda t=text: self.speak(f"Reminder: {t}")
                
                # Add to active reminders
                self.reminders.append({
                    'text': text,
                    'time': time,
                    'callback': callback
                })
                
                # Save to file
                with open(self.filename, 'w') as f:
                    json.dump([{
                        'text': r['text'],
                        'time': r['time'].strftime("%Y-%m-%d %H:%M:%S")
                    } for r in self.reminders], f, indent=4)
                    
                return True
            except Exception as e:
                print(f"⏰ Scheduler error: {e}")
                return False

    def _run(self):
        """Check for due reminders"""
        while self.running:
            with self.lock:
                now = datetime.now()
                for reminder in self.reminders[:]:  # Iterate over copy
                    if now >= reminder['time']:
                        reminder['callback']()
                        self.reminders.remove(reminder)
                        # Update file
                        with open(self.filename, 'w') as f:
                            json.dump([{
                                'text': r['text'],
                                'time': r['time'].strftime("%Y-%m-%d %H:%M:%S")
                            } for r in self.reminders], f, indent=4)
            
            time.sleep(self.check_interval)

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()