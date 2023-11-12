import logging
import threading
import subprocess
import multiprocessing
import queue
import json
import concurrent.futures
from external.client import YandexWeatherAPI
from utils import CITIES
import os
# from tasks import (
#     DataFetchingTask,
#     DataCalculationTask,
#     DataAggregationTask,
#     DataAnalyzingTask,
# )

def forecast_weather():
    #Анализ погодных условий по городам
    with concurrent.futures.ThreadPoolExecutor() as pool:
        all_forecasts = []
        for key, value in CITIES.items():
            forecast = pool.submit(YandexWeatherAPI.get_forecasting, value)
            all_forecasts.append(forecast)
            for forecast in concurrent.futures.as_completed(all_forecasts):
                resp = forecast.result()
                print(resp)
                # Запись в файлы
                file_name = f"./my_responses/{key}_response.json"
                with open(file_name, "w") as f:
                   f.write(json.dumps(resp, indent=4))
forecast_weather()

def outputs():
    for key, value in CITIES.items():
        input_file = f"my_responses/{key}_response.json"
        output_file = f"my_outputs/{key}_output.json"
        command = f"python external/analyzer.py -i {input_file} -o {output_file}"
        print(command)
        os.system(command)
outputs()
