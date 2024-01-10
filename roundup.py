import json
import csv
import os
import logging

logging.basicConfig(filename='logfile.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def roundup(input_folder, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['file_name', 'temp_avg_avg', 'relevant_cond_hours_avg']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for file_name in os.listdir(input_folder):
            if file_name.endswith(".json"):  # проверяем, что файл имеет расширение .json
                input_file = os.path.join(input_folder, file_name)
                with open(input_file, 'r') as file:
                    try:
                        data = json.load(file)
                        if not data:
                            logging.warning(f"File {input_file} is empty")
                            continue
                        temp_avg_sum = 0
                        relevant_cond_hours_sum = 0
                        num_days = len(data['days'])
                        for day in data['days']:
                            if day.get('temp_avg') is not None:
                                temp_avg_sum += day['temp_avg']
                            relevant_cond_hours_sum += day.get('relevant_cond_hours', 0)
                        temp_avg_avg = temp_avg_sum / num_days if num_days > 0 else 0
                        relevant_cond_hours_avg = relevant_cond_hours_sum / num_days if num_days > 0 else 0
                        writer.writerow(
                            {'file_name': input_file, 'temp_avg_avg': temp_avg_avg,
                             'relevant_cond_hours_avg': relevant_cond_hours_avg})
                    except json.JSONDecodeError as e:
                        logging.error(f"Error processing file {input_file}: {e}")
                    except KeyError as e:
                        logging.error(f"Error processing file {input_file}: {e}")


roundup('my_outputs', 'Output_avg.csv')