"""
This is a module for loading bus tracking
 data and bus stations' coordinates.
"""
import time
from datetime import datetime
import requests
from config.constants import (
    BUS_TRACKER_API_RESOURCE_ID,
    API_KEY,
    BUS_TRACKER_API_URL,
    BUS_OUT1_FILE,
    EARLY_HOURS,
    LATE_HOURS,
    BUS_OUT2_FILE,
    BUS_STATION_API_PARAMS,
)

from utils import process_data


def load_bus_tracking_data():
    """
    Function to load bus tracking data.
    """
    current_time = datetime.now()
    start_time = time.time()

    while True:
        if time.time() - start_time > 3600:
            break

        query_params = {
            "resource_id": BUS_TRACKER_API_RESOURCE_ID,
            "type": 1,
            "apikey": API_KEY,
        }

        r = requests.get(BUS_TRACKER_API_URL, params=query_params, timeout=5)

        if current_time.hour in EARLY_HOURS:
            output_file_path = BUS_OUT1_FILE
        elif current_time.hour in LATE_HOURS:
            output_file_path = BUS_OUT2_FILE
        else:
            return
        process_data(r, output_file_path)

        time.sleep(60)


def load_bus_stations_coord():
    """
    Function to load bus stations' coordinates.
    """
    output_file_path = "bus_station_output.csv"
    r = requests.get(
        "https://api.um.warszawa.pl/api/action/dbstore_get/",
        params=BUS_STATION_API_PARAMS,
        timeout=5,
    )

    process_data(r, output_file_path)
