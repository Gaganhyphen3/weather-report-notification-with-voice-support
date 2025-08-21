import requests
from plyer import notification
import pyttsx3   # 🔊 for text-to-speech

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_weather(city):
    # 1. Get coordinates
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_params = {"name": city, "count": 1}
    geo_res = requests.get(geo_url, params=geo_params).json()

    if not geo_res.get("results"):
        print("❌ City not found!")
        return

    lat = geo_res["results"][0]["latitude"]
    lon = geo_res["results"][0]["longitude"]

    # 2. Get weather data
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {"latitude": lat, "longitude": lon, "current_weather": True}
    weather_res = requests.get(weather_url, params=weather_params).json()

    if "current_weather" not in weather_res:
        print("❌ Weather data not found!")
        return

    temp = weather_res["current_weather"]["temperature"]
    wind = weather_res["current_weather"]["windspeed"]

    weather_info = f"{city}: {temp}°C, Wind {wind} km/h"

    print("✅ Weather:", weather_info)

    # Show desktop notification
    notification.notify(
        title="Weather Update",
        message=weather_info,
        timeout=5
    )

    # Speak the weather
    speak(f"Today in {city}: {temp} degrees Celsius with wind speed {wind} kilometers per hour.")

if __name__ == "__main__":
    city = input("Enter city name: ")
    get_weather(city)
