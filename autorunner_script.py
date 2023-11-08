import os
from utils import CITIES

for key, value in CITIES.items():
    input_file = f"my_responses/{key}_response.json"
    output_file = f"my_outputs/{key}_output.json"

    command = f"python external/analyzer.py -i {input_file} -o {output_file}"
    os.system(command)