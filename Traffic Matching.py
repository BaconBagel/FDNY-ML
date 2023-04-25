import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import csv

fire_data = pd.read_csv("firetrucks_big2.csv", nrows=50000)
traffic_data = pd.read_csv("traffic_with_cords.csv")


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in km
    dlat = abs(abs(lat1) - abs(lat2))
    dlon = abs(abs(lon1) - abs(lon2))

    tot = dlon + dlat

    return tot

def find_nearest_traffic_data(incident_row):
    incident_time = pd.to_datetime(incident_row[0], unit='s')
    incident_lat = incident_row[1]
    incident_lon = incident_row[2]


    # Filter traffic data to keep only rows within a certain time window (e.g., +/- 1 hour)
    time_window = timedelta(hours=1)
    traffic_data_filtered = traffic_data[
        (traffic_data["DATA_AS_OF"] >= (incident_time - time_window)) &
        (traffic_data["DATA_AS_OF"] <= (incident_time + time_window))
    ]

    # Calculate distances for each traffic data point and find the index of the nearest one
    distances = haversine_distance(
        incident_lat,
        incident_lon,
        traffic_data_filtered["avg_latitude"],
        traffic_data_filtered["avg_longitude"]
    )

    counter[0] += 1
    print(counter)
    if len(distances) > 0:
        nearest_index = distances.idxmin()

        return traffic_data_filtered.loc[nearest_index]
    else:
        counter2[0] += 1
        print(counter2)
        return "nan"


counter = [0]
counter2 = [0]
pd.set_option('display.max_columns', None)
traffic_data["DATA_AS_OF"] = pd.to_datetime(traffic_data['DATA_AS_OF'], format='%m/%d/%Y %I:%M:%S %p').dt.strftime('%Y-%m-%d %H:%M:%S')
traffic_data["DATA_AS_OF"] = pd.to_datetime(traffic_data['DATA_AS_OF'])
matched_traffic_data = fire_data.apply(find_nearest_traffic_data, axis=1)
result = pd.concat([fire_data, matched_traffic_data[["SPEED", "avg_longitude", "avg_latitude"]]], axis=1)
result.to_csv('traffic_matched_lat3 .csv', index=False)
print(result)

