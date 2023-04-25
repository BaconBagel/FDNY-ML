import pandas as pd
import time

# Constants
CONSTANT = 111
counter = [0]
data_size = 2500

# Read csv files
f1 = pd.read_csv("firebox_locations.csv",nrows=data_size)
f2 = pd.read_csv("traffic_matched_big.csv")
THRESHOLD = 5


# Function to perform the calculations


def calculate(row1, f2):
    counter[0] += 1
    start = time.time()
    total_diff = 0
    # Check if columns 1, 2, 4 and 3 in f2 are numeric and below THRESHOLD
    f2 = f2.query('4 > @THRESHOLD')
    print(f2)


    for index in f2.index:
        row2 = f2.loc[index]

        # Calculate the absolute difference for columns 8 and 2, and 9 and 3
        diff_col8_col2 = abs(row1[7] - row2[1])
        diff_col9_col3 = abs(row1[8] - row2[2])

        # Calculate the absolute sum of the differences
        abs_sum = diff_col8_col2 + diff_col9_col3

        # Multiply the sum by the constant and divide by the fifth column of f2
        value = (abs_sum * CONSTANT) / row2[4]

        # Check if the value is smaller than the value in column 4 of f2
        if value < row2[3]:
            total_diff += value
    end = time.time()
    print(total_diff)
    time_left = ((data_size - counter[0]) * (end - start)) / 60
    print(time_left, "minutes to go")

    return total_diff


# Apply the function to each row in f1 and store the result in a new column
f1['total_diff'] = f1.apply(lambda row: calculate(row, f2), axis=1)

# Save the updated f1 DataFrame to a new csv file
f1.to_csv("outcome_location5.csv", index=False)