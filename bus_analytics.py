from bus_data_calculations import *

json1 = format_and_data(BUS_OUTPUT1_FILE)
json2 = format_and_data(BUS_OUTPUT2_FILE)

bus_count_data1 = len(json1.items())
bus_count_data2 = len(json2.items())


def print_vehicles_over_speed_limit():
    print(count_vehicles_over_speed_limit(json1, MAX_SPEED))
    print(count_vehicles_over_speed_limit(json2, MAX_SPEED))

def print_violations_in_vicinity():
    violations1 = get_violation_coordinates(json1, MAX_SPEED)
    print(len(find_violations_places(violations1, MAX_DISTANCE, bus_count_data1)))
    violations2 = get_violation_coordinates(json2, MAX_SPEED)
    print(len(find_violations_places(violations2, MAX_DISTANCE, bus_count_data2)))