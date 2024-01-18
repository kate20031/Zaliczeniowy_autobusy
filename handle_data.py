import csv
from cmath import acos, sin, cos, sqrt, asin
from datetime import datetime
from itertools import groupby
from math import radians
from sklearn.cluster import DBSCAN



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

def calculate_speed(group, id):
    time_diff = (datetime.strptime(group[id]['Time'], '%Y-%m-%d %H:%M:%S') -
                         datetime.strptime(group[id - 1]['Time'], '%Y-%m-%d %H:%M:%S')).total_seconds()

    lat1, lon1 = group[id - 1]['Lat'], group[id - 1]['Lon']
    lat2, lon2 = group[id]['Lat'], group[id]['Lon']
    distance = haversine_distance(lat1, lon1, lat2, lon2)
    speed = distance / time_diff * 3.6 if time_diff > 0 else 0

    return speed

def calculate_max_speed(group):
    max_speed = 0

    for i in range(1, len(group)):
        speed = calculate_speed(group, i)
        if speed > max_speed:
            max_speed = speed
    return max_speed


def merge_coordinates_and_speeds(group):
    coordinates_speeds = []

    for i in range(1, len(group)):
        speed = calculate_speed(group, i)
        lat = group[i].get('Lat')
        lon = group[i].get('Lon')
        coordinates_speeds.append((lat, lon, speed))

    return coordinates_speeds

def format_and_data(file_path):
    json_data = []

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')

        next(csv_reader, None)
        for row in csv_reader:
            data_str = row[0]
            data_dict = convert_to_dict(data_str)
            time_str = data_dict['Time']
            try:
                d = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                continue

            if file_path == 'bas_output1.csv' or d.hour == 11 or d.hour == 12 and d.day:
                json_data.append(data_dict)
            elif file_path == 'bas_output2.csv' or d.hour == 17 or d.hour == 18 and d.day:
                json_data.append(data_dict)

    sorted_json_data = sorted(json_data, key=lambda x: (x['VehicleNumber'], x['Time']))
    grouped_json_data = {key: list(group) for key, group in groupby(sorted_json_data, key=lambda x: x['VehicleNumber'])}

    return grouped_json_data

def find_max_speed(json_data):
    max_speeds = []

    for key, group in json_data.items():
        max_sp = calculate_max_speed(group)
        # print(max_sp)
        max_speeds.append(max_sp)

    count_grater_than_50 = sum(1 for speed in max_speeds if speed > 50)
    return count_grater_than_50

def find_violations_places(coordinates, max_distance):
    clusters = []
    current_cluster = [coordinates[0]]

    for i in range(1, len(coordinates)):
        lat, lon = coordinates[i]
        prev_lat, prev_lon = current_cluster[-1]

        distance = haversine_distance(prev_lat, prev_lon, lat, lon)

        if distance <= max_distance:
            current_cluster.append((lat, lon))
        else:
            clusters.append(current_cluster)
            current_cluster = [(lat, lon)]

    clusters.append(current_cluster)

    return clusters

bus_csv1_file_path = "bus_output1.csv"
bus_csv2_file_path = "bus_output2.csv"

json1 = format_and_data(bus_csv1_file_path)
json2 = format_and_data(bus_csv2_file_path)

print(find_max_speed(json1))
print(find_max_speed(json2))

violations_coordinates = []

max_distance = 50
find_violations_places(violations_coordinates, max_distance)
