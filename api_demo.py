import os
import requests
from dotenv import load_dotenv
from pprint import pprint
from weather import Weather

load_dotenv()

def get_openweathermap(city, country):
    # api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENWEATHER_API_KEY is missing; add it to your .env file.")

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": f'{city},{country}',
        "APPID": api_key,
        "units": "metric"
    }
    w = Weather(city, country)
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Connection Successful!")
            # pprint(data)
            w.load_from_response(response)
            pprint(w.__dict__)
            # print(f"🌡️ Temperature: {data["main"]['temp']}°C")
            # print(f"💨 Wind Speed: {data['wind']['speed']} km/h")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def get_open_meteo_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            current = data["current_weather"]
            print("\n✅ Connection Successful!")
            print(f"🌡️ Temperature: {current['temperature']}°C")
            print(f"💨 Wind Speed: {current['windspeed']} km/h")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Coordinates for Cairo, Egypt area as a placeholder test
    # get_open_meteo_weather(lat=30.0444, lon=31.2357)
    get_openweathermap(city='London', country='uk')
    get_openweathermap(city='Cairo', country='Egypt')
