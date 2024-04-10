import os
import sys
import csv
from pathlib import Path
from extraction import extract_data


def processing(textfile, path):
    data = extract_data(textfile)
    filename = os.path.basename(path)
    if data != []:
        print(f'{filename} успешно обработан...')
        create_csv(data)
    else:
        print(f'{filename} содержит некорректные данные...')

def create_csv(data):
    root_path = Path(sys.modules['__main__'].__file__).resolve().parents[0]
    upload_path = os.path.join(root_path, 'csv/')
    os.makedirs(upload_path, exist_ok=True) 
    with open(f'{upload_path}/results.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for i in range(len(data)):
            writer.writerow(
                [data[i][0], data[i][1]],
            )