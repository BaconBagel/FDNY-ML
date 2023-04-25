import folium
import pandas as pd
from folium.plugins import HeatMap
from folium.features import MacroElement, Element

# load the CSV file into a Pandas dataframe
df = pd.read_csv('firetrucks.csv', header=None)

# create a map centered on New York City
ny_map = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

# filter dataframe for negative values in the fifth column
neg_df = df[df[4] < 0]

# convert latitude and longitude points to list of tuples
neg_locations = list(zip(neg_df[1], neg_df[2]))

# filter dataframe for positive values in the fifth column
pos_df = df[df[4] >= 0]

# convert latitude and longitude points to list of tuples
pos_locations = list(zip(pos_df[1], pos_df[2]))

# compute the difference between the two sets of locations
diff_locations = list(set(neg_locations) - set(pos_locations))

# create heatmap layer for the difference between the two sets of locations
diff_heatmap = HeatMap(diff_locations)
pos_heatmap = HeatMap(pos_locations)
neg_heatmap = HeatMap(neg_locations)

# define JavaScript function to toggle between layers
toggle_js = """
            var layer1 = document.getElementById('neg_heatmap');
            var layer2 = document.getElementById('pos_heatmap');
            var layer3 = document.getElementById('diff_heatmap');
            var control = document.getElementById('heatmap_toggle');

            function toggleHeatmap() {
                if (layer1.style.display === 'none') {
                    layer1.style.display = 'block';
                    layer2.style.display = 'none';
                    layer3.style.display = 'none';
                    control.innerHTML = 'Show Positive Temperatures';
                } else if (layer2.style.display === 'none') {
                    layer1.style.display = 'none';
                    layer2.style.display = 'block';
                    layer3.style.display = 'none';
                    control.innerHTML = 'Show Difference';
                } else {
                    layer1.style.display = 'none';
                    layer2.style.display = 'none';
                    layer3.style.display = 'block';
                    control.innerHTML = 'Show Negative Temperatures';
                }
            }
            """

# create MacroElement layer to hold toggle button
toggle_layer = MacroElement()

# create button to toggle between layers
toggle_button = Element(
    """
    <div style="position: fixed; top: 10px; right: 10px; z-index: 9999; background-color: white; padding: 6px; border-radius: 4px; box-shadow: 0 0 4px rgba(0,0,0,0.4);">
        <button onclick="toggleHeatmap()" id="heatmap_toggle">Show Positive Temperatures</button>
    </div>
    """
)

# add toggle button to toggle_layer
toggle_layer.add_children(toggle_button)

# add heatmap layers and toggle button to map
ny_map.add_child(neg_heatmap, name='Negative Temperatures', index=0)
ny_map.add_child(pos_heatmap, name='Positive Temperatures', index=1)
ny_map.add_child(diff_heatmap, name='Temperature Difference', index=2)
ny_map.add_child(toggle_layer)

# save the map as an HTML file
ny_map.save('ny_toggle_heatmap_MULTI.html')
