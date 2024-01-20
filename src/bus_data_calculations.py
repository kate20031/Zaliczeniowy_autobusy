"""
This module contains functions that are used to analyze,
including calculating speed, determining maximum speed,
finding violation coordinates,
formatting data, counting vehicles that are over speed limit
 and finding violations places.
"""
import csv
from datetime import datetime
from itertools import groupby
from pprint import pprint

from utils import convert_to_dict, haversine_distance
from config.constants import SPEED_CONVERSION, DATE_FORMAT, CSV_DELIMITER
from config.constants import EARLY_HOURS, LATE_HOURS, BUS_COUNT_THRESHOLD
from config.constants import BUS_OUT2_FILE, BUS_OUT1_FILE, CSV_ENCODING


def calculate_speed(vehicle, index):
    """
    Returns the calculated speed from coordinates.
    """

    time_diff = (
            datetime.strptime(vehicle[index]["Time"], DATE_FORMAT)
            - datetime.strptime(vehicle[index - 1]["Time"], DATE_FORMAT)
    ).total_seconds()

    lat1, lon1 = vehicle[index - 1]["Lat"], vehicle[index - 1]["Lon"]
    lat2, lon2 = vehicle[index]["Lat"], vehicle[index]["Lon"]
    distance = haversine_distance(lat1, lon1, lat2, lon2)
    speed = distance / time_diff * SPEED_CONVERSION if time_diff > 0 else 0

    return speed


def calculate_max_speed(vehicle):
    """
    Returns the maximum speed for the vehicle.
    """

    max_speed = 0

    for i in range(1, len(vehicle)):
        speed = calculate_speed(vehicle, i)
        if speed > max_speed:
            max_speed = speed
    return max_speed


def get_violation_coordinates(json_data, max_speed):
    """
    Returns list of the coordinates of
     violations that exceed max speed.
    """

    violations_coordinates = []

    for _, vehicle in json_data.items():
        for i in range(1, len(vehicle)):
            speed = calculate_speed(vehicle, i)

            if speed > max_speed:
                lat = vehicle[i].get("Lat")
                lon = vehicle[i].get("Lon")
                vehicle_number = vehicle[i].get("VehicleNumber")
                violations_coordinates.append((lat, lon, vehicle_number))

    return violations_coordinates


def get_bus_data(file_path):
    """
    Parse and format the data in the file.
    Returns the grouped json data.
    """

    json_data = []

    with open(file_path, newline="", encoding=CSV_ENCODING) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=CSV_DELIMITER)

        next(csv_reader, None)
        for row in csv_reader:
            data_str = row[0]
            data_dict = convert_to_dict(data_str)
            time_str = data_dict["Time"]
            try:
                d = datetime.strptime(time_str, DATE_FORMAT)
            except ValueError:
                continue

            early_run = d.hour in EARLY_HOURS and d.day == 18
            rush_hours_run = d.hour in LATE_HOURS and d.day == 18

            if file_path == BUS_OUT1_FILE and early_run:
                json_data.append(data_dict)
            elif file_path == BUS_OUT2_FILE and rush_hours_run:
                json_data.append(data_dict)

    sorted_json_data = sorted(
        json_data, key=lambda x: (
            x["VehicleNumber"], x["Time"]))
    grouped_json_data = {
        key: list(group)
        for key, group in groupby(sorted_json_data, key=lambda x: x["VehicleNumber"])
    }

    return grouped_json_data


def get_stops_data(file_path):
    json_data = []

    with open(file_path, newline="", encoding=CSV_ENCODING) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=CSV_DELIMITER)

        next(csv_reader, None)
        for row in csv_reader:
            data_str = row[0]
            data_dict = convert_to_dict(data_str)
            json_data.append(data_dict)

    return json_data


def count_vehicles_over_speed_limit(json_data, max_allowed_speed):
    """
    Count and return the number of vehicles
     that exceed the allowed maximum speed.
    """

    max_speeds = []

    for _, vehicle in json_data.items():
        max_sp = calculate_max_speed(vehicle)
        max_speeds.append(max_sp)

    count_grater_than_50 = sum(
        1 for speed in max_speeds if speed > max_allowed_speed)
    return count_grater_than_50


def find_violations_places(coordinates, max_dist, bus_count):
    """
    Find and return the list of violations
    that occurred within a specific distance.
    """

    violations_places = []
    result = []

    for value in coordinates:
        found = False
        for cluster in violations_places:
            for point in cluster:
                if (
                        haversine_distance(point[0], point[1], value[0], value[1])
                        <= max_dist
                ):
                    cluster.append(value)
                    found = True
                    break
        if not found:
            violations_places.append([value])

    for cluster in violations_places:
        if len(cluster) > bus_count * BUS_COUNT_THRESHOLD:
            result.append(cluster)

    return result


def find_stop(lat, lon, stops_data):
    for stop in stops_data:
        for item in stop['values']:
            if item['key'] == 'szer_geo':
                print('Szerokość geograficzna: ', item['value'])
        # stop_lat = stop["szer_geo"]
        # stop_lon = stop["dług_geo"]
        # distance = haversine_distance(lat, lon, stop_lat, stop_lon)
        # if distance <= 50:
        #     return True, stop

    return False, None


def check_vehicle_accuracy(vehicle_json, stops_data):
    for i in range(1, len(vehicle_json)):
        lat = vehicle_json[i].get("Lat")
        lon = vehicle_json[i].get("Lon")

        found, stop = find_stop(lat, lon, stops_data)

        if found:
            print(f"Pojazd znajduje się w pobliżu przystanku: {stop['nazwa_zespolu']}")
        else:
            print("Brak przystanku w okolicy pojazdu.")


def check_punctuality_accuracy(json_data, stops_data):
    for _, vehicle in json_data.items():
        check_vehicle_accuracy(vehicle, stops_data)
        break
