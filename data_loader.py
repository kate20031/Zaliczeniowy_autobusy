from datetime import datetime
import time
import requests


def load_data():

    api_key = '44c76d0d-4ca7-456a-a694-3b4dd63dd2d5'

    query_params = {
        'resource_id': 'f2e5503e927d-4ad3-9500-4ab9e55deb59',
        'type': 1,
        'apikey': api_key,
    }

    run_hours = {6, 16}
    all_data = []

    current_time = datetime.now()

    if current_time.hour in run_hours:
        start_time = time.time()

        while True:
            if time.time() - start_time > 60:
                break

            print(time.time() - start_time)
            response = requests.get('https://api.um.warszawa.pl/api/action/busestrams_get/', params=query_params)
            data = response.json()
            all_data.append(data)
            time.sleep(10)
        #
        else:
            time.sleep(3600)
    return all_data