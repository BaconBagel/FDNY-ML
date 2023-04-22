import pandas as pd
import torch
import numpy as np
import time
torch.set_printoptions(edgeitems=10, threshold=10000)

print("starting")
# read in the ambulance deployment data
ambulance_df = pd.read_csv('feb_2021_ambulance_data.csv')

# read in the fire alarm box location data
fire_alarm_df = pd.read_csv('firebox_locations.csv')

# merge the two dataframes based on the street intersection
print("Fetching the alarm boxes and finding locations")
merged_df = pd.merge(ambulance_df, fire_alarm_df, left_on='ALARM_BOX_LOCATION', right_on='LOCATION')



# select the relevant columns for the tensor
time_deployed = merged_df['INCIDENT_DATETIME'].values.astype('datetime64[s]').astype(float).reshape(-1, 1)  # convert to float and reshape
latitude = merged_df['LATITUDE'].values.astype(float).reshape(-1, 1)
longitude = merged_df['LONGITUDE'].values.astype(float).reshape(-1, 1)
response_time = merged_df['INCIDENT_TRAVEL_TM_SECONDS_QY'].values.astype(float).reshape(-1, 1)

# extract weather data
weather_df = pd.read_csv('feb_weather_data.csv')
weather_df['datetime'] = pd.to_datetime(weather_df['datetime'])  # remember to convert to standard format
merged_df['datetime'] = pd.to_datetime(merged_df['INCIDENT_DATETIME'])
merged_df = pd.merge_asof(merged_df.sort_values('datetime'), weather_df.sort_values('datetime'),
                          on='datetime', direction='nearest')

# select the relevant columns for the tensor
temperature = merged_df['temp'].values.astype(float).reshape(-1, 1)
humidity = merged_df['humidity'].values.astype(float).reshape(-1, 1)
precipitation = merged_df['precip'].values.astype(float).reshape(-1, 1)
print(temperature)


# concatenate the columns to create the final tensor
t = torch.from_numpy(np.concatenate([time_deployed, latitude, longitude, humidity, temperature,
                                                precipitation, response_time], axis=1))

mask = t[:, -1] > 0.1

# Filtered tensor
t_filtered = t[mask]

print(t)


# save the tensor to a file

torch.save(t, 'ambulance_tensor4.pt')

