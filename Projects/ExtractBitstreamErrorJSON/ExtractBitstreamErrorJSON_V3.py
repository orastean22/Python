# ----------------------------------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 09/Sept/2024
# -- Author: AdrianO
# -- Version 3.5
# -- Comment: extract from 2 Json files all errors, count them, and display date from ErrTimeTick + TimeChange
# -- Load the JSON data from the file
# -- Copy the JSON file in the same folder with the script and run
# ----------------------------------------------------------------------------------------------------------------------

import json
from collections import defaultdict
from datetime import datetime

# JSON file names
json_files = ["SIC2192Log_tempDev1_240829_120003.json", "SIC2192Log_tempDev9_240903_093945.json"]

# Function to combine the date from ErrTimeTick and time from TimeChange into "YYYY-MM-DD HH:MM:SS" format
def format_full_time(date_str, time_str):
    try:
        # Combine the date (YYYY-MM-DD) from ErrTimeTick and time (HH:MM:SS) from TimeChange
        full_datetime_str = f"{date_str} {time_str}"
        dt = datetime.strptime(full_datetime_str, "%Y-%m-%d %H:%M:%S.%f")  # Parse date and time, assuming milliseconds are present
        return dt.strftime("%Y-%m-%d %H:%M:%S")  # Return in "YYYY-MM-DD HH:MM:SS" format
    except ValueError:
        # If there's an error in parsing, return the original time string
        return f"{date_str} {time_str}"

# Function to extract only the date part from "ErrTimeTick"
def extract_date_from_err_time_tick(err_time_tick):
    try:
        # Assuming "ErrTimeTick" is in "YYYY-MM-DD HH:MM:SS.fff" format, extract only the "YYYY-MM-DD" part
        date_only = err_time_tick.split()[0]  # Split by space and take the first part (date)
        return date_only
    except IndexError:
        # If there's an error in extracting the date, return the original string
        return err_time_tick

# Function to load JSON data, display JSON file name, and then display errors with the date and time
def process_json_data(file_name):
    print(f"\n\033[1;34mProcessing JSON file: {file_name}\033[0m\n")

    with open(file_name, 'r') as file:
        data = json.load(file)

    # Dictionary to store the errors and corresponding times for the current JSON file
    current_file_errors = defaultdict(list)

    # Iterate through the JSON data and extract "ErrTimeTick", "Comment", and "TimeChange" values
    for error in data:
        err_time_tick = error.get("ErrTimeTick", "")  # Extract the ErrTimeTick field (date and time)
        date_only = extract_date_from_err_time_tick(err_time_tick)  # Extract only the date part (YYYY-MM-DD)

        for line in error.get("ErrorLines", []):
            comment = line.get("Comment", "")
            time_change = line.get("TimeChange", "")  # Extract the TimeChange field (time)

            if comment and comment != "CRC_b21":  # Exclude CRC_b21
                # Combine the extracted date (YYYY-MM-DD) with the time from TimeChange
                full_datetime = format_full_time(date_only, time_change)
                current_file_errors[comment].append(full_datetime)

    # Print out the errors and corresponding full timestamps for the current JSON file
    for comment, times in current_file_errors.items():
        count = len(times)
        if count == 1:
            print(f"Error: {repr(comment)} occurred at {times[0]}")
        else:
            print(f"Error: {repr(comment)} occurred {count} time(s) at the following times:")
            for time in times:
                print(f" - {time}")

# Process each JSON file and display its name followed by its errors
for json_file in json_files:
    process_json_data(json_file)
