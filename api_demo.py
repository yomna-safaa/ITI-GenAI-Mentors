import os
import requests
from dotenv import load_dotenv
from pprint import pprint

# k = "39322a6ac5c99a2539e12c914f1d86f8"

load_dotenv()

class Weather:
    def __init__(self, city, country):
        self.city = city
        self.country = country
        self.temperature = None
        self.temperature_max = None
        self.temperature_min = None
        self.wind_speed = None
        self.humidity = None
        self.description = None

    def load_from_response(self, response):
        data = response.json()
        # pprint(data)
        '''{'base': 'stations',
        'clouds': {'all': 40},
        'cod': 200,
        'coord': {'lat': 30.0626, 'lon': 31.2497},
        'dt': 1794217427,
        'id': 360630,
        'main': {'feels_like': 21.84,
                'grnd_level': 1023,
                'humidity': 43,
                'pressure': 1024,
                'sea_level': 1024,
                'temp': 22.42,
                'temp_max': 22.42,
                'temp_min': 21.9},
        'name': 'Cairo',
        'sys': {'country': 'EG',
                'id': 2514,
                'sunrise': 1794197703,
                'sunset': 1794236557,
                'type': 1},
        'timezone': 7200,
        'visibility': 10000,
        'weather': [{'description': 'scattered clouds',
                    'icon': '03d',
                    'id': 802,
                    'main': 'Clouds'}],
        'wind': {'deg': 50, 'speed': 8.23}}
        '''
        self.city += f'-{data["name"]}'
        self.country += f'-{data["sys"]["country"]}'
        self.temperature = data["main"]["temp"]
        self.temperature_max = data["main"]["temp_max"]
        self.temperature_min = data["main"]["temp_min"]
        self.wind_speed = data["wind"]["speed"]
        self.humidity = data["main"]["humidity"]
        self.description = data["weather"][0]["description"]

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
