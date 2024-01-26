import logging
import json
import concurrent.futures
import multiprocessing
from external.client import YandexWeatherAPI
from utils import CITIES
import os
import csv
import asyncio
import subprocess


def __init__(self):
    self.logger = logging.getLogger(__name__)
class DataFetchingTask:
    @staticmethod
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
                    file_name = f"./API_responses/{key}_response.json"
                    with open(file_name, "w") as f:
                        f.write(json.dumps(resp, indent=4))


# class DataCalculationTask:
#     async def analyze_outputs(self):
#         logging.info("Выполнение скрипта")
#         for key, value in CITIES.items():
#             input_file = f"API_responses/{key}_response.json"
#             logging.info(f"Загружаем погоду из {key}")
#             output_file = f"script_responses/{key}_output.json"
#             command = f"python external/analyzer.py -i {input_file} -o {output_file}"
#             print("analyze_outputs", command)
#             process = await asyncio.create_subprocess_shell(command)
#             await process.wait()
#
#
# class DataAggregationTask:
#     async def roundup(self, input_folder, output_csv):
#         logging.info("Анализ и свод ключевых данных")
#         with open(output_csv, 'w', newline='') as csvfile:
#             fieldnames = ['file_name', 'temp_avg_avg', 'relevant_cond_hours_avg']
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#             writer.writeheader()
#
#             files = [file_name for file_name in os.listdir(input_folder) if file_name.endswith(".json")]
#             async def process_file(file_name):
#                 input_file = os.path.join(input_folder, file_name)
#                 with open(input_file, 'r') as file:
#                     try:
#                         data = json.load(file)
#                         if not data:
#                             logging.warning(f"File {input_file} is empty")
#                             return
#                         temp_avg_sum = 0
#                         relevant_cond_hours_sum = 0
#                         num_days = len(data['days'])
#                         for day in data['days']:
#                             if day.get('temp_avg') is not None:
#                                 temp_avg_sum += day['temp_avg']
#                             relevant_cond_hours_sum += day.get('relevant_cond_hours', 0)
#                         temp_avg_avg = temp_avg_sum / num_days if num_days > 0 else 0
#                         relevant_cond_hours_avg = relevant_cond_hours_sum / num_days if num_days > 0 else 0
#                         writer.writerow(
#                             {'file_name': input_file, 'temp_avg_avg': temp_avg_avg,
#                              'relevant_cond_hours_avg': relevant_cond_hours_avg})
#                     except json.JSONDecodeError as e:
#                         logging.error(f"Error processing file {input_file}: {e}")
#                     except KeyError as e:
#                         logging.error(f"Error processing file {input_file}: {e}")
#
#             tasks = [process_file(file_name) for file_name in files]
#             await asyncio.gather(*tasks)
#
#
#
# class DataAnalyzingTask:
#     async def best_city(self, file_path):
#         data = []
#         with open(file_path, 'r') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 data.append(row)
#
#         max_both_values_file = max(data,
#                                    key=lambda x: (float(x['temp_avg_avg']), float(x['relevant_cond_hours_avg'])))
#         return max_both_values_file



if __name__ == "__main__":
    logging.basicConfig(filename='weather_logs.txt', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    #async def main():
    forecast = DataFetchingTask()
    forecast.forecast_weather()

        # calculation = DataCalculationTask()
        # await calculation.analyze_outputs()
        #
        # aggregation = DataAggregationTask()
        # await aggregation.roundup("script_responses", "Output_avg.csv")
        #
        # analyzer = DataAnalyzingTask()
        # analyzer.best_city('Output_avg.csv')

    #asyncio.run(main())


