import folium
import pandas as pd
from folium.plugins import HeatMap

# load the CSV file into a Pandas dataframe
df = pd.read_csv('firetrucks .csv', header=None)

# create a map centered on New York City
ny_map = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

# convert latitude and longitude points to list of tuples
locations = list(zip(df[1], df[2]))

# add heatmap overlay to the map
HeatMap(locations).add_to(ny_map)

# save the map as an HTML file
ny_map.save('ny_heatmap.html')
