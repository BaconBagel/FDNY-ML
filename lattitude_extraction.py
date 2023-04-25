import pandas as pd
import numpy as np

# Read the CSV file
df = pd.read_csv("DOT_Traffic_Speeds_NBE.csv")

# Define a function to parse the "LINK_POINTS" column
def parse_link_points(link_points):
    if isinstance(link_points, str):
        points = link_points.strip('[]').split(' ')
        latitudes = []
        longitudes = []
        for point in points:
            try:
                latitude, longitude = point.split(',')
                latitudes.append(float(latitude))
                longitudes.append(float(longitude))
            except ValueError:
                pass
            except IndexError:
                pass
        if len(latitudes) > 0 and len(longitudes) > 0:
            return pd.Series({'avg_latitude': sum(latitudes) / len(latitudes),
                              'avg_longitude': sum(longitudes) / len(longitudes)})
        else:
            return pd.Series({'avg_latitude': np.nan,
                              'avg_longitude': np.nan})
    else:
        return pd.Series({'avg_latitude': np.nan,
                          'avg_longitude': np.nan})

# Apply the function to the "LINK_POINTS" column and create two new columns
df[['avg_latitude', 'avg_longitude']] = df['LINK_POINTS'].apply(parse_link_points)

# Save the result to a new CSV file
df.to_csv('traffic_with_cords.csv', index=False)
