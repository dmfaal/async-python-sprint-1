import concurrent.futures
import csv
import json
import os
import logging
import time

from external.client import YandexWeatherAPI
from concurrent.futures import ThreadPoolExecutor
from logs import my_logs

logger = my_logs()


class DataFetchingTask:

    # Создаю конструктор класса для инициализации атрибута с данными
    def __init__(self, CITIES):
        self.CITIES = CITIES

    # Создаю пул потоков, собираю задачу и ключ в очередь
    def forecast_weather(self, queue):
        logging.info("Старт сбора данных")
        with concurrent.futures.ThreadPoolExecutor() as pool:
            for key, value in self.CITIES.items():
                try:
                    forecast = pool.submit(YandexWeatherAPI.get_forecasting, value)
                    queue.put((key, forecast))
                    logging.info(f"Собираем погоду из города {key}: {value}")
                    time.sleep(0.1)
                except TimeoutError:
                    logging.error(f"Сбор данных для {key}: timeout")

        # Обрабатываю элементы пока они есть
        while not queue.empty():
            key, forecast = queue.get()
            resp = forecast.result()
            file_name = f"data/{key}_raw_response.json"
            with open(file_name, "w") as f:
                f.write(json.dumps(resp, indent=4))


class DataCalculationTask:
    # Выполнение ф-ции независимо от атрибутов экземпляров класса
    @staticmethod
    def analyze_outputs(key):
        logging.info(f"Загружаем погоду из {key}")
        input_file = f"data/{key}_raw_response.json"
        output_file = f"data/{key}_output.json"
        command = f"python external/analyzer.py -i {input_file} -o {output_file}"
        logging.info(f"Выполнение скрипта для {key}")
        os.system(command)
        time.sleep(0.1)


class DataAggregationTask:
    def roundup(self, input_folder: str, output_csv: str):
        logging.info("Анализ и свод ключевых данных")
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['file_name', 'temp_avg', 'relevant_cond_hours_avg']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            files = [file_name for file_name in os.listdir(input_folder) if file_name.endswith(".json")]
            with ThreadPoolExecutor() as executor:
                results = executor.map(lambda file_name: self.process_file(input_folder, file_name), files)
                for result in results:
                    if result:
                        writer.writerow(result)
                    time.sleep(0.1)

    def process_file(self, input_folder, file_name):
        input_file = os.path.join(input_folder, file_name)
        with open(input_file, 'r') as file:
            try:
                data = json.load(file)
                temp_avg_sum = 0
                relevant_cond_hours_sum = 0
                num_days = len(data['days'])
                for day in data['days']:
                    if day.get('temp_avg') is not None:
                        temp_avg_sum += day['temp_avg']
                    relevant_cond_hours_sum += day.get('relevant_cond_hours', 0)
                    logging.info(f"Температура {file_name}: {relevant_cond_hours_sum}")
                temp_avg = temp_avg_sum / num_days if num_days > 0 else 0
                relevant_cond_hours_avg = relevant_cond_hours_sum / num_days if num_days > 0 else 0
                return {'file_name': input_file, 'temp_avg': temp_avg,
                        'relevant_cond_hours_avg': relevant_cond_hours_avg}
            except BaseException:
                pass
            time.sleep(0.1)


class DataAnalyzingTask:
    def best_city(self, file_path):
        logging.info("Старт сбора данных")
        data = []
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
                logging.info(f"Перебираем: {data}")
            temp_avg_max = max(data, key=lambda x: float(x['temp_avg']))
            relevant_cond_hours_max = max(data, key=lambda x: float(x['relevant_cond_hours_avg']))
            conditions = [item['file_name'] for item in data if
                          float(item['temp_avg']) == float(temp_avg_max['temp_avg'])] + [item['file_name'] for item
                                                                                         in data if float(
                    item['relevant_cond_hours_avg']) == float(relevant_cond_hours_max['relevant_cond_hours_avg'])]
        logging.info(f"Наилучшие условия: {conditions}")
        time.sleep(0.1)
