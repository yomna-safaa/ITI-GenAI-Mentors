from pprint import pprint

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

