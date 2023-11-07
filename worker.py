from utils import CITIES
from external.client import YandexWeatherAPI
import json

def worker():
    for key, value in CITIES.items():
        rep = YandexWeatherAPI.get_forecasting(value)
        print(rep)
        with open("my_response.json", "a") as f:
            f.write(json.dumps(rep))
worker()

