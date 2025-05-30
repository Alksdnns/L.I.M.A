from datetime import datetime, timedelta
import re

def parse_reminder_command(command):
    try:
        command = command.lower().strip()
        
        # First extract the time part if "at" exists
        if "at" in command:
            parts = command.split("at", 1)  # Split on first "at" only
            task_part = parts[0].strip()
            time_part = parts[1].strip()
        else:
            # Handle cases without "at" (like "in 10 minutes")
            task_part = command
            time_part = ""

        # Extract clean task text by removing trigger phrases
        triggers = [
            "remind me to", 
            "set reminder to",
            "remember to",
            "alert me to",
            "notify me to"
        ]
        task_text = task_part
        for phrase in triggers:
            task_text = task_text.replace(phrase, "").strip()

        # Parse time (handles: 2:45, 2:45am, 14:45, 2pm, in 10 minutes, etc.)
        time_match = re.search(r"(\d{1,2})(?::(\d{2}))?\s*([ap]m)?|in (\d+) (minute|hour)", time_part)
        if time_match:
            if time_match.group(4):  # Handle "in X minutes/hours"
                quantity = int(time_match.group(4))
                unit = time_match.group(5)
                remind_time = datetime.now() + timedelta(
                    minutes=quantity if unit == "minute" else quantity*60
                )
            else:  # Handle absolute times
                hour = int(time_match.group(1))
                minute = int(time_match.group(2) or 0)
                period = (time_match.group(3) or "").lower()
                
                # Convert to 24-hour format
                if 'pm' in period and hour < 12:
                    hour += 12
                elif 'am' in period and hour == 12:
                    hour = 0
                    
                # Create datetime
                remind_time = datetime.now().replace(
                    hour=hour, 
                    minute=minute, 
                    second=0, 
                    microsecond=0
                )
                if remind_time < datetime.now():
                    remind_time += timedelta(days=1)
            
            return task_text, remind_time
            
    except Exception as e:
        print(f"⏰ Reminder parse error: {e}")
    return None, None