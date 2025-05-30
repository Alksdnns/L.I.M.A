import os
import subprocess
import pyttsx3
import speech_recognition as sr
import webbrowser

class Open:
    def __init__(self):
        self.tts = pyttsx3.init()
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        print(f"[TTS] {text}")
        self.tts.say(text)
        self.tts.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            print("[🎧 Listening] Please say the file type (e.g., application, pdf, image)...")
            audio = self.recognizer.listen(source)

        try:
            result = self.recognizer.recognize_google(audio).lower()
            print(f"[🗣️ Recognized] {result}")
            return result
        except Exception as e:
            print(f"[❌ Recognition Error] {str(e)}")
            return ""

    def get_extensions_for_type(self, file_type):
        mapping = {
            "application": [".exe", ".lnk", ".bat", ".app"],
            "pdf": [".pdf"],
            "document": [".docx", ".txt", ".rtf", ".pdf"],
            "excel": [".xlsx", ".xls"],
            "image": [".jpg", ".png", ".jpeg", ".bmp"],
            "photo": [".jpg", ".png", ".jpeg"],
            "file": [".exe", ".lnk", ".bat", ".app", ".pdf", ".docx", ".txt", ".rtf", ".xlsx", ".xls", ".jpg", ".png", ".jpeg", ".bmp"]
        }
        return mapping.get(file_type, None)

    def search_file(self, keyword, file_extensions=None):
        print(f"[🔍 Search] Looking for '{keyword}'...")
        found_files = []
        keyword = keyword.lower()

        for root, dirs, files in os.walk("C:\\"):
            for file in files:
                file_lower = file.lower()
                if keyword in file_lower:
                    if not file_extensions or any(file_lower.endswith(ext) for ext in file_extensions):
                        found_files.append(os.path.join(root, file))
                        print(f"[✅ Found] {os.path.join(root, file)}")
                if len(found_files) >= 10:
                    break
            if len(found_files) >= 10:
                break

        return found_files

    def launch(self, paths):
        for path in paths:
            try:
                if os.path.exists(path):
                    subprocess.Popen([path], shell=True)
                    self.speak(f"Opening {os.path.basename(path)}")
                    return
            except Exception as e:
                self.speak(f"Error launching file: {str(e)}")
        self.speak("Sorry, I could not open any of the matched files.")

    def ask_and_launch(self, original_name="unknown", *args, **kwargs):
        self.speak(f"Sir, what type of file is '{original_name}'?")
        file_type = self.listen()
        if not file_type:
            self.speak("Sorry, I couldn't understand the file type.")
            return

        file_extensions = self.get_extensions_for_type(file_type)
        if not file_extensions:
            self.speak(f"I didn't recognize the type '{file_type}', so I'll search all types.")
            file_extensions = None

        matches = self.search_file(original_name, file_extensions)
        if not matches:
            self.speak(f"No matching files found for '{original_name}' with type '{file_type}'.")
        else:
            self.launch(matches)

    def ask_music_app_and_launch(self):
        self.speak("Which music app would you like to use?")
        self.speak("Say Spotify, YouTube, or Media Player.")

        choice = self.listen()
        if "spotify" in choice:
            matches = self.search_file("spotify", [".exe"])
            if matches:
                self.launch(matches)
            else:
                self.speak("Spotify is not installed on your system.")
        elif "youtube" in choice or "utube" in choice:
            # YouTube app likely not installed, open browser instead
            self.speak("Opening YouTube in your web browser.")
            webbrowser.open("https://www.youtube.com")
        elif "media" in choice or "player" in choice:
            for media_player in ["vlc", "wmplayer", "media player"]:
                matches = self.search_file(media_player, [".exe"])
                if matches:
                    self.launch(matches)
                    return
            self.speak("Media player not found.")
        else:
            self.speak("Sorry, I didn’t catch which music app you want.")

    # Added wrapper method for compatibility
    def search_and_launch(self, original_name="unknown", *args, **kwargs):
        # Just call ask_and_launch internally
        self.ask_and_launch(original_name=original_name, *args, **kwargs)
