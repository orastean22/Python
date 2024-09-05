#----------------------------------------------------------------------------------------------------------------------
#-- Python Script File
#-- Created on 09/Sept/2024 
#-- Author: AdrianO
#-- Version 2
#-- Comment: extract from Json file all errors and count them + add the time of each error on screen
#-- Load the JSON data from the file
#-- Copy the JSON file in the same folder with the script and run
#----------------------------------------------------------------------------------------------------------------------

import json
from collections import defaultdict
from datetime import datetime

# JSON file name
jsonName = "SIC2192Log_tempDev9_240903_093945.json"

# Load the JSON data from the file
with open(jsonName, 'r') as file:
    data = json.load(file)

# Dictionary to store the count of each unique comment and its corresponding times
comment_counts = defaultdict(list)


# Function to convert time to HH:MM:SS format
def format_time(time_str):
    try:
        # Assuming time_str is a string that can be parsed by datetime
        # Adjust format if necessary depending on the format of "TimeChange"
        dt = datetime.strptime(time_str, "%H:%M:%S.%f")   # Use datetime.strptime if needed
        return dt.strftime("%H:%M:%S")
    except ValueError:
        # If there's an error in parsing, return the original time string
        return time_str


# Iterate through the JSON data and extract "Comment" and "TimeChange" values
for error in data:
    for line in error.get("ErrorLines", []):
        comment = line.get("Comment", "")
        time_change = line.get("TimeChange", "")

        if comment and comment != "CRC_b21":  # Exclude CRC_b21
            # Append the formatted time of this comment occurrence
            formatted_time = format_time(time_change)
            comment_counts[comment].append(formatted_time)

# Print out the comments, their counts, and the corresponding times
for comment, times in comment_counts.items():
    count = len(times)
    if count == 1:
        print(f"Error: {repr(comment)} occurred at {times[0]}")
    else:
        print(f"Error: {repr(comment)} occurred {count} time(s) at the following times:")
        for time in times:
            print(f" - {time}")



