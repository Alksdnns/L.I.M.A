import json
from datetime import datetime
from threading import Lock

# Global lock for thread-safe file operations
REMINDER_LOCK = Lock()

def save_reminder(reminder_text, remind_at, filename="reminders.json"):
    if not isinstance(remind_at, datetime):
        raise ValueError("remind_at must be a datetime object")

    try:
        with REMINDER_LOCK:
            # Load existing reminders
            try:
                with open(filename, "r") as f:
                    reminders = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                reminders = []

            # Avoid duplicates
            new_entry = {
                "text": reminder_text,
                "time": remind_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            if new_entry not in reminders:
                reminders.append(new_entry)
            else:
                return False  # Duplicate ignored

            # Save back to file
            with open(filename, "w") as f:
                json.dump(reminders, f, indent=4)
            return True

    except Exception as e:
        print(f"⚠️ Failed to save reminder: {e}")
        return False