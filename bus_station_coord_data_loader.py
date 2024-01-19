import requests
import csv


def load_data():
    api_key = '44c76d0d-4ca7-456a-a694-3b4dd63dd2d5'

    query_params = {
        'id': '1c08a38c-ae09-46d2-8926-4f9d25cb0630',
        'apikey': api_key,
    }

    output_file_path = 'bus_station_output.csv'
    r = requests.get('https://api.um.warszawa.pl/api/action/dbstore_get/', params=query_params)

    data = r.json()
    print(data)
    records = data['result']

    if records != "Błędna metoda lub parametry wywołania":
        with open(output_file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            for record in records:
                writer.writerow([record])


load_data()
