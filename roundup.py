import json
import csv
import os

def roundup(input_folder, output_csv):
    input_file = os.path.join(input_folder, )
    with open(input_file, 'r') as file:
        data = json.load(file)

    temp_avg_sum = 0
    relevant_cond_hours_sum = 0
    num_days = len(data['days'])

    for day in data['days']:
        if day['temp_avg'] is not None:
            temp_avg_sum += day['temp_avg']
        relevant_cond_hours_sum += day.get('relevant_cond_hours', 0)

    temp_avg_avg = temp_avg_sum / num_days if num_days > 0 else 0
    relevant_cond_hours_avg = relevant_cond_hours_sum / num_days if num_days > 0 else 0

    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['file_name', 'temp_avg_avg', 'relevant_cond_hours_avg']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'file_name': input_file, 'temp_avg_avg': temp_avg_avg, 'relevant_cond_hours_avg': relevant_cond_hours_avg})


# Пример вызова функции для файла "DUBAI_output.json"
roundup('my_outputs/ABUDHABI_output.json', 'DUBAI_output_avg.csv')