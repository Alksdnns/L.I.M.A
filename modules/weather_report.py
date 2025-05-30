import requests
import geocoder
import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say your location...")
        speak("Sir, can you give me your current location?")
        audio = recognizer.listen(source)
    try:
        location = recognizer.recognize_google(audio)
        print(f"You said: {location}")
        return location
    except sr.UnknownValueError:
        speak("Sorry, I did not catch that.")
        return None
    except sr.RequestError:
        speak("Sorry, speech service is down.")
        return None

def get_weather_report(location=None):
    try:
        # If location not provided, ask user
        if not location:
            location = listen()
            if not location:
                return "Could not get your location from voice."

        # Get coordinates using geocoder
        g = geocoder.arcgis(location)
        if not g.ok:
            return f"Could not find coordinates for '{location}'."

        lat, lon = g.latlng

        # Fetch weather from Open-Meteo
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "timezone": "auto"
        }
        response = requests.get(url, params=params)
        data = response.json()

        if "current_weather" in data:
            cw = data["current_weather"]
            temp = cw["temperature"]
            windspeed = cw["windspeed"]
            weathercode = cw["weathercode"]
            weather_desc = {
                0: "Clear sky",
                1: "Mainly clear",
                2: "Partly cloudy",
                3: "Overcast",
                45: "Foggy",
                48: "Depositing rime fog",
                51: "Light drizzle",
                53: "Moderate drizzle",
                55: "Dense drizzle",
                61: "Slight rain",
                63: "Moderate rain",
                65: "Heavy rain",
                71: "Slight snow",
                73: "Moderate snow",
                75: "Heavy snow",
                80: "Slight rain showers",
                81: "Moderate rain showers",
                82: "Violent rain showers",
            }
            desc = weather_desc.get(weathercode, "Unknown weather")

            report = (f"Weather at {location}:\n"
                      f"{desc}, Temperature: {temp}°C, Wind Speed: {windspeed} km/h")
            print(report)
            speak(report)
            return report
        else:
            speak("Sorry, no weather data available.")
            return "Sorry, no weather data available."

    except Exception as e:
        err_msg = f"Error retrieving weather: {str(e)}"
        speak(err_msg)
        return err_msg

if __name__ == "__main__":
    get_weather_report()
