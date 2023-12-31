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
import pandas

# from tasks import (
#     DataFetchingTask,
#     DataCalculationTask,
#     DataAggregationTask,
#     DataAnalyzingTask,
# )
logger = logging.getLogger(__name__)
# Анализ погодных условий по городам
def forecast_weather():
    logging.info("Старт сбора данных")
    with concurrent.futures.ThreadPoolExecutor() as pool:
        all_forecasts = []
        for key, value in CITIES.items():
            forecast = pool.submit(YandexWeatherAPI.get_forecasting, value)
            all_forecasts.append(forecast)
            logging.info(f"Собираем погоду из города {key}: {value}")
            for forecast in concurrent.futures.as_completed(all_forecasts):
                resp = forecast.result()
                print(resp)
                file_name = f"./my_responses/{key}_response.json"
                with open(file_name, "w") as f:
                    f.write(json.dumps(resp, indent=4))


def analyze_outputs():
    # Вызов скрипта
    for key, value in CITIES.items():
        input_file = f"my_responses/{key}_response.json"
        output_file = f"my_outputs/{key}_output.json"
        command = f"python external/analyzer.py -i {input_file} -o {output_file}"
        print(command)
        os.system(command)
#def round_up():
    # Совмещение результатов работы скрипта в один файл


if __name__ == "__main__":
    logging.basicConfig(filename='weather_forecast.txt', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    forecast_weather()
    analyze_outputs()

