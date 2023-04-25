import pandas as pd
import numpy as np
import time
from numba import jit

# Define constant for calculations
CONSTANT = 111
counter = [0]
data_size = 13000

# Read in the data
f1 = pd.read_csv("firebox_locations.csv")
f2 = pd.read_csv("traffic_matched_big.csv")

# Filter f2 based on threshold
THRESHOLD = 5
f2_filtered = f2



# Define the calculation function
@jit
def calculate(row1, f2_filtered):
    counter[0] += 1
    start = time.time()
    total_diff = 0

    # Vectorize the calculations
    diff_col8_col2 = np.abs(row1[7] - f2_filtered.iloc[:,1])
    diff_col9_col3 = np.abs(row1[8] - f2_filtered.iloc[:,2])
    abs_sum = diff_col8_col2 + diff_col9_col3

    # Calculate the values and filter by threshold
    values = (abs_sum * CONSTANT) / f2_filtered.iloc[:,4]
    mask = values < f2_filtered.iloc[:,3]
    filtered_values = values[mask]

    # Calculate the total difference
    total_diff = np.sum(filtered_values)

    end = time.time()
    print(total_diff)
    time_left = ((data_size - counter[0]) * (end - start)) / 60
    print(time_left, "minutes to go")

    return total_diff

# Apply the function to each row in f1 and store the result in a new column
f1['total_diff'] = f1.apply(lambda row: calculate(row, f2_filtered), axis=1)

# Save the updated f1 DataFrame to a new csv file
f1.to_csv("outcome_location_big.csv", index=False)
