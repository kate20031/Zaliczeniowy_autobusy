from ast import literal_eval

import pandas as pd


def read_and_group_by_vehicle_number():
    df = pd.read_csv('output.csv')
    df['result'] = df['result'].apply(lambda data: literal_eval(data))
    all_data_df = []

    for item in df['result']:
        temp_data = pd.DataFrame(item)
        all_data_df.append(temp_data)

    all_data_df = pd.concat(all_data_df)

    if 'VehicleNumber' in all_data_df.columns:
        group_data = all_data_df.groupby('VehicleNumber')

        for name, group in group_data:
            print(name)
            print(group)

read_and_group_by_vehicle_number()