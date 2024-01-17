import csv
from cmath import acos, sin, cos, sqrt, asin
from datetime import datetime
from itertools import groupby
from math import radians


def haversine_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    distance = 6371 * c * 1000

    return int(distance.real)


def convert_to_dict(str_dict):
    return eval(str_dict)


def calculate_average_speed(group):
    total_distance = 0
    total_time = 0
    sum_speed = 0

    for i in range(1, len(group)):
        time_diff = (datetime.strptime(group[i]['Time'], '%Y-%m-%d %H:%M:%S') -
                     datetime.strptime(group[i - 1]['Time'], '%Y-%m-%d %H:%M:%S')).total_seconds()

        lat1, lon1 = group[i - 1]['Lat'], group[i - 1]['Lon']
        lat2, lon2 = group[i]['Lat'], group[i]['Lon']
        distance = haversine_distance(lat1, lon1, lat2, lon2)
        total_distance += distance
        total_time += time_diff

    average_speed = total_distance / total_time * 3.6 if total_time > 0 else 0
    print(average_speed)

    return average_speed


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

sorted_json_data = sorted(json_data, key=lambda x: (x['VehicleNumber'], x['Time']))
grouped_json_data = {key: list(group) for key, group in groupby(sorted_json_data, key=lambda x: x['VehicleNumber'])}

for key, group in grouped_json_data.items():
    avg_speed = calculate_average_speed(group)
    print(f"VehicleNumber {key}: Average Speed = {avg_speed:.2f} meters per second")
