import pandas as pd
import os
import openpyxl

class Generator:
    @staticmethod
    def generator():
        # Получаем список файлов с данными
        files_path = ".\my_outputs"
        files = [f for f in os.listdir(files_path) if f.endswith(".json")]
        print(files)

        # Создаем dataframe
        data_frames = []
        print(data_frames)

        # Обработка каждого из файлов
        for my_responses_file in files:
            json_path = os.path.join(files_path, my_responses_file)
            print(json_path)
            with open(json_path, "r") as f:
                json_data = pd.read_json(f)
                data_frames.append(json_data)

        # Запись в xls
        merged_data = pd.concat(data_frames, ignore_index=True)
        xlsx_file = "merged_data.xlsx"
        merged_data.to_excel(xlsx_file, index=False)
