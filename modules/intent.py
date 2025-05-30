class IntentDetector:
    def __init__(self):
        self.task_phrases = [
            "open", "launch", "start", "run", "execute", "fire up", "boot up", "load",
            "open up", "initiate", "activate", "bring up", "shoot up", "trigger", "engage",
            "please open", "can you open", "could you launch", "will you start", "i want to run",
            "let's start", "start the", "launch the", "open the", "execute the", "trigger the"
        ]

        self.registration_phrases = [
            "register", "add user", "new voice", "sign up", "create profile"
        ]

        self.volume_up_phrases = [
            "volume up", "turn up the volume", "increase the volume", "raise volume",
            "volume increase", "turn volume up"
        ]

        self.volume_down_phrases = [
            "volume down", "turn down the volume", "decrease the volume",
            "lower the volume", "volume decrease", "turn volume down"
        ]

        self.system_status_phrases = [
            "system status", "show me system status", "read me system status", "device status",
            "show me device status", "system info", "system health", "how is my system",
            "system report", "system overview", "system condition", "system diagnostics",
            "system performance", "system metrics", "system details", "system summary",
            "check system", "system checkup", "system analysis", "system state",
            "what's my system status", "how's the system", "system health check",
            "diagnose system", "system resources", "system vitals", "system monitor",
            "system inspection", "system evaluation", "system assessment"
        ]

        self.battery_phrases = [
            "battery", "battery status", "how much battery", "battery level",
            "what's my battery status", "charge left", "check battery", "remaining charge",
            "battery percentage", "battery health", "battery condition", "battery life",
            "power level", "charge status", "battery remaining", "battery capacity",
            "how's my battery", "battery check", "battery report", "battery info",
            "battery details", "battery summary", "battery state", "battery charge",
            "current battery", "battery reading", "battery meter", "battery gauge",
            "power remaining", "charge level", "battery consumption", "battery usage"
        ]

        self.ram_phrases = [
            "ram", "memory usage", "how much ram", "ram status", "ram info",
            "check ram", "memory status", "available memory", "ram usage",
            "ram consumption", "ram details", "ram report", "memory info",
            "memory details", "memory report", "ram statistics", "memory statistics",
            "ram metrics", "memory metrics", "ram allocation", "memory allocation",
            "ram performance", "memory performance", "ram check", "memory check",
            "ram health", "memory health", "ram condition", "memory condition",
            "ram available", "memory available", "ram used", "memory used",
            "ram utilization", "memory utilization", "ram overview", "memory overview"
        ]

        self.disk_phrases = [
            "disk space", "storage", "hard drive", "check disk", "disk usage",
            "how much storage", "space left", "disk info", "available storage",
            "disk capacity", "storage status", "disk status", "storage info",
            "disk details", "storage details", "disk report", "storage report",
            "disk summary", "storage summary", "disk check", "storage check",
            "disk health", "storage health", "disk condition", "storage condition",
            "free space", "available space", "disk consumption", "storage consumption",
            "disk utilization", "storage utilization", "disk metrics", "storage metrics",
            "disk statistics", "storage statistics", "disk analysis", "storage analysis",
            "disk overview", "storage overview", "disk state", "storage state"
        ]

        self.web_search_phrases = [
            "google", "search", "look up", "find", "browse", "lookup", "check", "explore",
            "seek", "investigate", "scan", "research", "query", "look for", "hunt", "dig up",
            "track down", "retrieve", "get info on", "look into", "examine", "probe",
            "find out", "discover", "search for", "search about", "search the web for",
            "search online for", "internet search for", "web search for", "google search for",
            "find information about", "look up information on", "find details about",
            "search the internet for", "look it up", "search up", "find online",
            "web lookup", "online search", "internet lookup", "search the net",
            "search the web", "search online", "search the internet", "do a search for",
            "perform a search for", "conduct a search for", "make a search for",
            "i need information about", "i want to know about", "tell me about",
            "what is", "who is", "where is", "when was", "why does", "how does",
            "can you find", "could you search", "would you look up", "please search"
        ]

        self.pause_play_phrases = [
            "pause", "continue", "pause video", "play video", "pause playback", "post", "post video",
            "resume playback", "toggle play", "pause music", "play music", "pause the video", "wait"
        ]

        self.fullscreen_phrases = [
            "full screen", "play full screen", "fullscreen", "maximize",
            "go fullscreen", "enter fullscreen mode"
        ]

        self.skip_phrases = [
            "skip", "skip forward", "next", "jump", "skip ahead",
            "next item", "skip this", "move forward"
        ]

        self.weather_phrases = [
            "weather", "temperature", "forecast", "weather report", "tell me about the weather today",
            "give me weather forecast", "is it raining", "weather update", "weather today", "weather now"
        ]

        self.scheduler_phrases = [
            "remind me to", "set reminder", "set a reminder", "create reminder",
            "alert me at", "notify me at", "reminder at", "remind at",
            "schedule at", "remember to", "remember that", "wake me at",
            "ping me at", "set alarm for", "set timer for", "at"
        ]

        self.time_phrases = [
            "at", "by", "on", "in", "for", "around", "about", "sharp"
        ]

        self.intent_keywords = {
            "search_web": self.web_search_phrases,
            "pause_play": self.pause_play_phrases,
            "play_full_screen": self.fullscreen_phrases,
            "skip": self.skip_phrases,
            "get_weather": self.weather_phrases,
            "register_user": self.registration_phrases,
            "control_volume_up": self.volume_up_phrases,
            "control_volume_down": self.volume_down_phrases,
            "do_task": self.task_phrases,
            "get_system_status": self.system_status_phrases,
            "get_battery_status": self.battery_phrases,
            "get_ram_status": self.ram_phrases,
            "get_disk_status": self.disk_phrases,
            "set_reminder": self.scheduler_phrases,
        }

    def classify(self, command: str):
        command = command.lower()

        if any(phrase in command for phrase in self.system_status_phrases):
            return "get_system_status"
        if any(phrase in command for phrase in self.battery_phrases):
            return "get_battery_status"
        if any(phrase in command for phrase in self.ram_phrases):
            return "get_ram_status"
        if any(phrase in command for phrase in self.disk_phrases):
            return "get_disk_status"

        has_time_word = any(word in command for word in self.time_phrases)
        has_reminder_verb = any(word in command for word in ["remind", "alert", "notify", "wake", "alarm", "set"])
        has_scheduler_phrase = any(phrase in command for phrase in self.scheduler_phrases)

        if has_scheduler_phrase and has_time_word and has_reminder_verb:
            return "set_reminder"

        if any(greet in command for greet in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]):
            return "greet"
        if any(phrase in command for phrase in self.pause_play_phrases):
            return "pause_play"
        if any(phrase in command for phrase in self.fullscreen_phrases):
            return "play_full_screen"
        if any(phrase in command for phrase in self.skip_phrases):
            return "skip"
        if any(phrase in command for phrase in self.task_phrases):
            return "do_task"
        if any(phrase in command for phrase in self.weather_phrases):
            return "get_weather"
        if any(phrase in command for phrase in self.registration_phrases):
            return "register_user"
        if any(phrase in command for phrase in self.volume_up_phrases):
            return "control_volume", "up"
        if any(phrase in command for phrase in self.volume_down_phrases):
            return "control_volume", "down"
        if "play" in command:
            return "play_music"

        known_apps = ["spotify", "chrome", "notepad", "vlc", "calculator", "word", "excel", "powerpoint"]
        for app in known_apps:
            if app in command:
                return f"open_{app}"

        chat_keywords = [
            "who", "what", "when", "where", "why", "how", "explain", "define", "meaning", "time", "date",
            "capital", "president", "minister", "location", "country", "planet", "earth", "universe",
            "joke", "story", "fact", "name", "talk", "chat", "question", "conversation", "summarize",
            "translate", "science", "physics", "chemistry", "history", "invented",
            "intelligent", "dream", "purpose", "do", "can", "tell", "give", "help", "describe",
            "life", "exist", "age", "year", "tomorrow", "now", "calculate", "math", "problem",
            "technology", "robot", "machine", "learning", "ai", "computer", "internet", "cpu", "memory",
            "gravity", "speed", "light", "travel", "mars", "moon"
        ]

        if any(phrase in command for phrase in chat_keywords):
            return "chat_ai"
        
        if any(phrase in command for phrase in self.web_search_phrases):
            return "search_web"

        return "none"
