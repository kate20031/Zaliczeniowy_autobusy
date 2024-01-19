import csv
from datetime import datetime
from itertools import groupby
from constants import *
from utils import *


def calculate_speed(group, id):
    time_diff = (datetime.strptime(group[id]['Time'], DATE_FORMAT) -
                 datetime.strptime(group[id - 1]['Time'], DATE_FORMAT)).total_seconds()

    lat1, lon1 = group[id - 1]['Lat'], group[id - 1]['Lon']
    lat2, lon2 = group[id]['Lat'], group[id]['Lon']
    distance = haversine_distance(lat1, lon1, lat2, lon2)
    speed = distance / time_diff * SPEED_CONVERSION if time_diff > 0 else 0

    return speed


def calculate_max_speed(group):
    max_speed = 0

    for i in range(1, len(group)):
        speed = calculate_speed(group, i)
        if speed > max_speed:
            max_speed = speed
    return max_speed


def get_violation_coordinates(json_data, max_speed):
    violations_coordinates = []

    for key, group in json_data.items():
        for i in range(1, len(group)):
            speed = calculate_speed(group, i)

            if speed > max_speed:
                lat = group[i].get('Lat')
                lon = group[i].get('Lon')
                vehicle_number = group[i].get('VehicleNumber')
                violations_coordinates.append((lat, lon, vehicle_number))

    return violations_coordinates


def format_and_data(file_path):
    json_data = []

    with open(file_path, newline='', encoding=CSV_ENCODING) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=CSV_DELIMITER)

        next(csv_reader, None)
        for row in csv_reader:
            data_str = row[0]
            data_dict = convert_to_dict(data_str)
            time_str = data_dict['Time']
            try:
                d = datetime.strptime(time_str, DATE_FORMAT)
            except ValueError:
                continue

            if file_path == 'bas_output1.csv' or d.hour == 11 or d.hour == 12 and d.day:
                json_data.append(data_dict)
            elif file_path == 'bas_output2.csv' or d.hour == 17 or d.hour == 18 and d.day:
                json_data.append(data_dict)

    sorted_json_data = sorted(json_data, key=lambda x: (x['VehicleNumber'], x['Time']))
    grouped_json_data = {key: list(group) for key, group in groupby(sorted_json_data, key=lambda x: x['VehicleNumber'])}

    return grouped_json_data


def count_vehicles_over_speed_limit(json_data, max_allowed_speed):
    max_speeds = []

    for key, group in json_data.items():
        max_sp = calculate_max_speed(group)
        max_speeds.append(max_sp)

    count_grater_than_50 = sum(1 for speed in max_speeds if speed > max_allowed_speed)
    return count_grater_than_50


def find_violations_places(coordinates, max_dist, bus_count):
    violations_places = []
    result = []

    for value in coordinates:
        found = False
        for cluster in violations_places:
            for point in cluster:
                if haversine_distance(point[0], point[1], value[0], value[1]) <= max_dist:
                    cluster.append(value)
                    found = True
                    break
        if not found:
            violations_places.append([value])

    for cluster in violations_places:
        if len(cluster) > bus_count * BUS_COUNT_THRESHOLD:
            print(len(cluster))
            result.append(cluster)

    return result