import csv
from datetime import datetime
from itertools import groupby


def convert_to_dict(str_dict):
    return eval(str_dict)


csv_file_path = "output.csv"
json_data = []

with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')

    next(csv_reader, None)
    for row in csv_reader:
        data_str = row[0]
        data_dict = convert_to_dict(data_str)
        time_str = data_dict['Time']
        d = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

        if d.hour == 19 and d.day:
            json_data.append(data_dict)

sorted_json_data = sorted(json_data, key=lambda x: x['VehicleNumber'])

grouped_json_data = {key: list(group) for key, group in groupby(sorted_json_data, key=lambda x: x['VehicleNumber'])}
