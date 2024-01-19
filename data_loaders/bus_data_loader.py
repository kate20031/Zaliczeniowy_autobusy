from datetime import datetime
from constants import *
from utils import process_data
import time
import requests


def load_bus_tracking_data():
    current_time = datetime.now()
    start_time = time.time()
    output_file_path = ''

    while True:
        if time.time() - start_time > 3600:
            break

        query_params = {
            'resource_id': BUS_TRACKER_API_RESOURCE_ID,
            'type': 1,
            'apikey': API_KEY,
        }

        r = requests.get(BUS_TRACKER_API_URL, params=query_params)

        if current_time.hour in EARLY_RUN_HOURS:
            output_file_path = 'output/bus_output1.csv'
        elif current_time.hour in LATE_RUN_HOURS:
            output_file_path = ('bus_output2.cs'
                                ''
                                '+v')

        process_data(r, output_file_path)

        time.sleep(60)


def load_bus_stations_coordinates():
    output_file_path = 'bus_station_output.csv'
    r = requests.get('https://api.um.warszawa.pl/api/action/dbstore_get/', params=BUS_STATION_API_PARAMS)

    process_data(r, output_file_path)