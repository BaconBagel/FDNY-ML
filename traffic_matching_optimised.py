import pandas as pd
from datetime import datetime, timedelta
import time
import numpy as np
import csv
from numba import njit

data_size = 150000

fire_data = pd.read_csv("firetrucks_big2.csv")
traffic_data = pd.read_csv("traffic_with_cords.csv")



@njit
def haversine_distance(lat1, lon1, lat2_arr, lon2_arr):
    R = 6371  # Earth's radius in km
    dlat = np.abs(np.abs(lat1) - np.abs(lat2_arr))
    dlon = np.abs(np.abs(lon1) - np.abs(lon2_arr))

    tot = dlon + dlat

    return tot



def find_nearest_traffic_data(incident_row):
    start = time.time()
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
        traffic_data_filtered["avg_latitude"].to_numpy(),
        traffic_data_filtered["avg_longitude"].to_numpy(),
    )

    counter[0] += 1
    end = time.time()
    time_left = ((data_size - counter[0]) * (end - start)) / 60
    print(time_left, "minutes to go")
    if len(distances) > 0:
        nearest_index = np.argmin(distances)
        nearest_traffic_row = traffic_data_filtered.iloc[nearest_index]
        return pd.Series([nearest_traffic_row["SPEED"], nearest_traffic_row["avg_longitude"], nearest_traffic_row["avg_latitude"]])
    else:
        return pd.Series([np.nan, np.nan, np.nan])


counter = [0]
counter2 = [0]
pd.set_option('display.max_columns', None)
traffic_data["DATA_AS_OF"] = pd.to_datetime(traffic_data['DATA_AS_OF'], format='%m/%d/%Y %I:%M:%S %p').dt.strftime('%Y-%m-%d %H:%M:%S')
traffic_data["DATA_AS_OF"] = pd.to_datetime(traffic_data['DATA_AS_OF'])
matched_traffic_data = fire_data.apply(find_nearest_traffic_data, axis=1)
result = pd.concat([fire_data, matched_traffic_data], axis=1)
result.to_csv('traffic_matched_big2.csv', index=False)
print(result)
