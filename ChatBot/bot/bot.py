# bot/bot.py
import pyttsx3
import requests
from datetime import datetime

def text_to_voice(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f" Error in text-to-voice: {e}")

def get_weather(city):
    api_key = "dd397ff127f49add6a5356970ff20ad1"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}"
    response = requests.get(complete_url)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        weather = data['weather'][0]['description']
        temperature = main['temp'] - 273.15  # Convert temperature from Kelvin to Celsius
        feels_like = main['feels_like'] - 273.15
        temp_min = main['temp_min'] - 273.15
        temp_max = main['temp_max'] - 273.15
        pressure = main['pressure']
        humidity = main['humidity']
        wind_speed = data['wind']['speed']
        wind_deg = data['wind']['deg']
        visibility = data['visibility']
        
        # Convert Unix timestamps to readable format
        sunrise = datetime.utcfromtimestamp(data['sys']['sunrise']).strftime('%Y-%m-%d %H:%M:%S')
        sunset = datetime.utcfromtimestamp(data['sys']['sunset']).strftime('%Y-%m-%d %H:%M:%S')

        # Format the weather information with line separators
        weather_info = (
            f"Weather in {city}:\n\n"
            f"Description: {weather}\n"
            f"---------------------\n"
            f"Temperature: {temperature:.2f}°C\n"
            f"---------------------\n"
            f"Feels like: {feels_like:.2f}°C\n"
            f"---------------------\n"
            f"Min Temperature: {temp_min:.2f}°C\n"
            f"---------------------\n"
            f"Max Temperature: {temp_max:.2f}°C\n"
            f"---------------------\n"
            f"Pressure: {pressure} hPa\n"
            f"---------------------\n"
            f"Humidity: {humidity}%\n"
            f"---------------------\n"
            f"Wind Speed: {wind_speed} m/s\n"
            f"---------------------\n"
            f"Wind Direction: {wind_deg}°\n"
            f"---------------------\n"
            f"Visibility: {visibility} meters\n"
            f"---------------------\n"
            f"Sunrise: {sunrise}\n"
            f"---------------------\n"
            f"Sunset: {sunset}\n"
            f"---------------------"
        )
        return weather_info
    else:
        return "City not found. Please check the city name and try again."
        
def chatbot(user_input):
    response = ""
    if "text to voice" in user_input:
        response = "Enter the text you want to convert to voice: "
    elif "tell weather" in user_input:
        response = "Enter the city name: "
    elif "exit" in user_input:
        response = "Goodbye!"
    else:
        response = "I didn't understand that. Please try again."
    return response
