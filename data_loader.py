from asyncio import sleep
from datetime import datetime
import time
import requests
import csv


def load_data():
    run_hours1 = {11, 12}
    run_hours2 = {17, 18}

    current_time = datetime.now()
    start_time = time.time()

    while True:
        if time.time() - start_time > 3600:
            break

        api_key = '44c76d0d-4ca7-456a-a694-3b4dd63dd2d5'

        query_params = {
            'resource_id': 'f2e5503e927d-4ad3-9500-4ab9e55deb59',
            'type': 1,
            'apikey': api_key,
        }

        r = requests.get('https://api.um.warszawa.pl/api/action/busestrams_get/', params=query_params)

        data = r.json()
        records = data['result']

        if current_time.hour in run_hours1:
            output_file_path = 'bus_output1.csv'
        elif current_time.hour in run_hours2:
            output_file_path = ('bus_output2.cs'
                                ''
                                '+v')

        if records != "Błędna metoda lub parametry wywołania":
            with open(output_file_path, 'a', newline='') as file:
                writer = csv.writer(file)
                for record in records:
                    writer.writerow([record])

        time.sleep(60)


load_data()
