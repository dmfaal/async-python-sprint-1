import csv

def best_city(file_path):
    # Загрузка данных из CSV-файла
    data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

    # Находим файл с максимальными значениями для обоих параметров
    max_both_values_file = max(data, key=lambda x: (float(x['temp_avg_avg']), float(x['relevant_cond_hours_avg'])))
    return max_both_values_file

# Пример использования функции
file_path = 'Output_avg.csv'
result = best_city(file_path)
print(f'Город с наилучшими условиями: {result["file_name"]}')