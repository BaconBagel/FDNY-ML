import pandas as pd

# load the original ambulance data csv file
ambulance_data = pd.read_csv('dispatch_data.csv', chunksize=1000)

# filter the data for February 2021 only and concatenate the chunks
start_date = '2021-02-01'
end_date = '2021-03-01'
feb_2021_data_chunks = []
for chunk in ambulance_data:
    print(chunk)
    # convert the date/time column to datetime format
    chunk['INCIDENT_DATETIME'] = pd.to_datetime(chunk['INCIDENT_DATETIME'], format='%m/%d/%Y %I:%M:%S %p')
    # filter the data for February 2021 only
    mask = (chunk['INCIDENT_DATETIME'] >= start_date) & (chunk['INCIDENT_DATETIME'] < end_date)
    feb_2021_data_chunk = chunk.loc[mask]
    # append the filtered chunk to the list of chunks
    feb_2021_data_chunks.append(feb_2021_data_chunk)

# concatenate the filtered chunks into one dataframe
feb_2021_data = pd.concat(feb_2021_data_chunks)

# save the filtered data to a new csv file
feb_2021_data.to_csv('feb_2021_ambulance_data.csv', index=False)
