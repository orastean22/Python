# --------------------------------------------------------------------
# -- Python Script File
# -- Created on 04/21/2024 10:30:56
# -- Author: AdrianO
# -- Comment: Calculate Pulse Width for signal A and signal B
# --------------------------------------------------------------------

""" declare the encoding of the file. It indicates that the file is encoded using UTF-8"""
# -*- coding: utf-8 -*-
from nptdms import TdmsFile
from matplotlib import pyplot as plt
from collections import Counter

# --------------------------------------------------------------------
""" 
Calculates the start and end times of pulses in the signal data.
    Args:
    signal_data (array-like): The signal data.
    threshold (float): The threshold value to detect pulses.
Returns: list: A list of tuples containing the start and end times of each pulse.
"""
def calculate_pulse_times(signal_data, threshold):

    pulse_start = None
    pulse_times = []

    for i, value in enumerate(signal_data):
        # Detect rising edge
        if value > threshold and pulse_start is None:
            pulse_start = i
        # Detect falling edge
        elif value <= threshold and pulse_start is not None:
            pulse_end = i - 1
            pulse_times.append((pulse_start, pulse_end))
            pulse_start = None

    return pulse_times

""" 
 Calculates the width of each pulse based on its start and end times.
    Args:
        pulse_times (list of tuples): List of tuples containing the start and end times of each pulse.
    Returns: list: A list of pulse widths.
"""
def calculate_pulse_widths(pulse_times):
    pulse_widths = [end - start + 1 for start, end in pulse_times]
    return pulse_widths


# --------------------------------------------------------------------
""" this function takes a list of pulse widths as input, calculates the average width 
of the pulses, and returns this average width as the output of the function"""

def calculate_average_pulse_width(pulse_widths):
    average_width = sum(pulse_widths) / len(pulse_widths)
    return average_width
""" returns the calculated average width as the output of the function"""

# --------------------------------------------------------------------
""" Reads a TDMS file and extracts pulse information from the specified channels.
    Args:
        file_path (str): Path to the TDMS file.
        group_name (str): Name of the group in the TDMS file.
        channel_names (list of str): Names of the channels in the TDMS file.
        threshold (float): The threshold value to detect pulses.
    Returns: tuple: A tuple containing pulse times and pulse widths for each channel.
    """
def read_tdms_file(file_path, group_name, channel_names, threshold):
    # Load TDMS file using file_path
    tdms_file = TdmsFile.read(file_path)

    pulse_times_dict = {}
    pulse_widths_dict = {}

    for channel_name in channel_names:
        # Get the specified group and channel data
        group = tdms_file[group_name]
        signal_data = group[channel_name][:]  # Directly access the data like: DUT1_Gate_A_Signal", "DUT1_Gate_B_Signal

        # Calculate pulse times for all pulses
        pulse_times = calculate_pulse_times(signal_data, threshold)
        pulse_times_dict[channel_name] = pulse_times

        # Calculate pulse widths for all pulses
        pulse_widths = calculate_pulse_widths(pulse_times)
        pulse_widths_dict[channel_name] = pulse_widths

    return pulse_times_dict, pulse_widths_dict

# Example usage
file_path = "C:/Users/aorastean/Desktop/TDMS/Glitch3.tdms"
group_name = "DUT Data"
channel_names = ["DUT1_Gate_A_Signal", "DUT1_Gate_B_Signal"]
threshold = 5

pulse_times, pulse_widths = read_tdms_file(file_path, group_name, channel_names, threshold)

# Calculate the average pulse width once and Print
average_width = calculate_average_pulse_width(pulse_widths[channel_names[0]])
print("Average pulse width for", channel_names[0] + ":", average_width,"\n")

for channel_name in channel_names:
    print("All pulses for", channel_name + ":")
    for i, (start, end) in enumerate(pulse_times[channel_name]):
        width = pulse_widths[channel_name][i]
        rise_time = start
        fall_time = end
        print("Pulse", i+1, "- Rise time:", rise_time, "- Fall time:", fall_time, "- Width:", width)

    print("\nGlitches detected (width < average width) for", channel_name + ":")
    glitches_detected = [i+1 for i, width in enumerate(pulse_widths[channel_name]) if width < average_width]
    if glitches_detected:
        print("Pulses with width less than 5:", glitches_detected)
    else:
        print("No glitches detected.")
    print("\n")
