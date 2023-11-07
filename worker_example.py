from external.client import YandexWeatherAPI
from utils import CITIES
import json

def worker():
    for key, value in CITIES.items():
        try:
            resp = YandexWeatherAPI.get_forecasting(value)
            print(resp)
        except:
            #continue
            with open("my_response.json", "a") as f:
                f.write(json.dumps(resp))
            break
worker()

