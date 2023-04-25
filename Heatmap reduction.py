import folium
import pandas as pd
from folium.plugins import HeatMap
from folium.features import MacroElement, Element
# Load CSV data into a pandas DataFrame
data = pd.read_csv('outcome_location_big.csv')

# Create a map centered on New York
ny_map = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

folium.TileLayer('stamentoner').add_to(ny_map)

# Create a HeatMap layer with the latitude, longitude, and weight data
heatmap_layer = HeatMap(
    data[['LATITUDE', 'LONGITUDE', 'total_diff']],
    name='Heatmap',
    control=False, blur=6,min_opacity=0, radius=10
)

# Add the HeatMap layer to the map
heatmap_layer.add_to(ny_map)

# Add a LayerControl to the map so that the HeatMap can be toggled on and off
folium.LayerControl().add_to(ny_map)

# Display the map
ny_map.save('reductions3.html')