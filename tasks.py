import logging
import json
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from external.client import YandexWeatherAPI
from utils import CITIES
import os
import asyncio
import csv

def __init__(self):
    self.logger = logging.getLogger(__name__)

class DataFetchingTask:
    async def forecast_weather(self):
        logging.info("Старт сбора данных")
        with concurrent.futures.ThreadPoolExecutor() as pool:
            all_forecasts = []
            for key, value in CITIES.items():
                forecast = pool.submit(YandexWeatherAPI.get_forecasting, value)
                all_forecasts.append(forecast)
                logging.info(f"Собираем погоду из города {key}: {value}")
            else:
                logging.info(f"Пропускаем город {key}, так как на URL сработал логгер")
            for forecast, (key, _) in zip(all_forecasts, CITIES.items()):
                resp = forecast.result()
                print(resp)
                file_name = f"data/{key}_raw_response.json"
                with open(file_name, "w") as f:
                    f.write(json.dumps(resp, indent=4))

class DataCalculationTask:
    async def analyze_outputs(self, key):
        logging.info(f"Загружаем погоду из {key}")
        input_file = f"data/{key}_raw_response.json"
        output_file = f"data/{key}_output.json"
        command = f"python external/analyzer.py -i {input_file} -o {output_file}"
        logging.info(f"Выполнение скрипта для {key}")
        os.system(command)

class DataAggregationTask:
    async def roundup(self, input_folder, output_csv):
        logging.info("Анализ и свод ключевых данных")
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['file_name', 'temp_avg', 'relevant_cond_hours_avg']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            files = [file_name for file_name in os.listdir(input_folder) if file_name.endswith(".json")]
            async def process_file(file_name):
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
                        writer.writerow(
                            {'file_name': input_file, 'temp_avg': temp_avg,
                             'relevant_cond_hours_avg': relevant_cond_hours_avg})
                    except:
                        pass
            tasks = [process_file(file_name) for file_name in files]
            await asyncio.gather(*tasks)

class DataAnalyzingTask:
    async def best_city(self, file_path):
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
        print(f"Наилучшие условия: {conditions}")

if __name__ == "__main__":
    logging.basicConfig(filename='weather_logs.txt', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    async def main():
        forecast = DataFetchingTask()
        await forecast.forecast_weather()

        calculation = DataCalculationTask()
        for key, _ in CITIES.items():
            await calculation.analyze_outputs(key)

        aggregation = DataAggregationTask()
        await aggregation.roundup("data", "output_avg.csv")

        analyzer = DataAnalyzingTask()
        await analyzer.best_city('output_avg.csv')

    asyncio.run(main())
