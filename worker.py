from utils import CITIES
from external.client import YandexWeatherAPI
import json


def worker():
    for key, value in CITIES.items():
        rep = YandexWeatherAPI.get_forecasting(value)
        print(rep)
        file_name = f"./my_responses/{key}_response.json"
        with open(file_name, "w") as f:
            f.write(json.dumps(rep, indent=4))
            #f.write(json.dumps(rep, indent=4).rstrip('null{}null')) -- убирает null если это один файл

worker()


# previous dump
# def worker():
#     for key, value in CITIES.items():
#         try:
#             resp = YandexWeatherAPI.get_forecasting(value)
#             print(resp)
#         except:
#             #continue
#             with open("my_response.json", "a") as f:
#                 f.write(json.dumps(resp))
#             break
# worker()
