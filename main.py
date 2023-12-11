
import csv
from datetime import time, datetime
from collections import defaultdict

def process_file(filename):
    stations_dict = defaultdict(int)
    with open(filename, encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        origin_column_name = valid_date_column(file)
        for row in csv_reader:
            time_object = datetime.strptime(row[origin_column_name][-8:], "%H:%M:%S").time()
            if time_object >= time(6, 0) and time_object <= time(11, 59):
                stations_dict[row['nombre_estacion_origen']] += 1
    
    top3_hotspots = sorted(stations_dict.items(), key=lambda x: x[1], reverse=True)[:3]
    print("Las estaciones con más actividad son:", top3_hotspots)
def valid_date_column(file):
    original_position = file.tell()
    csv_reader = csv.reader(file)
    column_names = next(csv_reader, None)
    first_row = next(csv_reader, None)
    date_columns = list()

    for index, element in enumerate(first_row):
        if is_valid_date(element):
            date_columns.append((column_names[index], index))

    valid_date_values = [first_row[index[1]] for index in date_columns]

    oldest_date_index = find_oldest_date(valid_date_values)
    file.seek(original_position)

    return date_columns[oldest_date_index][0]

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False
    
def find_oldest_date(date_list):
    return min(range(len(date_list)), key=lambda i: datetime.strptime(date_list[i], "%Y-%m-%d %H:%M:%S"))

process_file("trips_2023.csv")