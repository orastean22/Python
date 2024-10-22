# --------------------------------------------------------------------
# -- Python Script File
# -- Created on 04/21/2024 10:30:56
# -- Author: AdrianO
# -- Comment: Calculate Pulse Width for signal A and signal B
# --------------------------------------------------------------------

""" declare the encoding of the file. It indicates that the file is encoded using UTF-8"""
# -*- coding: utf-8 -*-
from nptdms import TdmsFile

from collections import Counter
import matplotlib.pyplot as plt
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

# Function to load data from a tdms file to get channel name
def load_data(file_path):
    tdms_file = TdmsFile.read(file_path)
    group_name = "DUT Data"

    # Iterate over all groups and print their channels
    for group in tdms_file.groups():
        print(f"Group: {group.name}")

        # Get and print the list of channels within the group
        channels = group.channels()
        channel_names = [channel.name for channel in channels]
    
    return channel_names


# --------------------------------------------------------------------
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
""" Reads a TDMS file and extracts pulse information from the specified channels.
    Args:
        file_path (str): Path to the TDMS file.
        group_name (str): Name of the group in the TDMS file.
        channel_names (list of str): Names of the channels in the TDMS file.
        threshold (float): The threshold value to detect pulses.
    Returns: tuple: A tuple containing pulse times and pulse widths for each channel.
 """
def read_tdms_file(file_path, group_name, channel_name, threshold):
    # Load TDMS file using file_path
    tdms_file = TdmsFile.read(file_path)

    pulse_times_dict = {}
    pulse_widths_dict = {}

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

def get_high_contribution_numbers(data, threshold, thresholdLow):

    # Count contributions using Counter
    contributions = Counter(data[1:])

    # Total count of elements
    total_count = len(data)
    for read_key in contributions.keys():
        contributions[read_key] = contributions[read_key]/total_count*100
    # Calculate contributions using the previous function
    #contributions = count_unique_contributions(data)
    print(contributions)
    # Filter numbers based on threshold
    high_contribution_numbers = [number for number, contribution in contributions.items() if contribution > threshold]
    low_contribution_numbers = [number for number, contribution in contributions.items() if contribution < thresholdLow]

    return high_contribution_numbers,low_contribution_numbers

def get_plotGlitch(signal_data, upperLimit, lowerLimit, start, end, step,path = r'\\pictshare01\04_Ops\16_data_science\script\Test_Engineer\GlitchDetection\Output'):
    """
    Generates a plot and returns the corresponding data (x-axis, signal data, upper limit, lower limit).

    Args:
        signal_data: The signal data to plot.
        upperLimit: The upper limit data.
        lowerLimit: The lower limit data.
        start: The starting index for the plot region.
        end: The ending index for the plot region.
        step: The step size for data extraction (optional).

    Returns:
        A tuple containing the x-axis data and the signal, upper limit, and lower limit data for the plot.
    """

    # Extract data for the plot region
    x_axis = range(start - step, end + step + 1)  # Adjust based on step size
    plot_signal_data = signal_data[start - step: end + step + 1]
    plot_upperLimit = upperLimit[start - step: end + step + 1]
    plot_lowerLimit = lowerLimit[start - step: end + step + 1]

    # Create the plot (optional, for debugging or external use)
    fig, ax = plt.subplots()  # Uncomment if needed for debugging
    ax.plot(x_axis, plot_signal_data)
    ax.plot(x_axis, plot_upperLimit)
    ax.plot(x_axis, plot_lowerLimit)
    fig.savefig(path+"\\"+"temp.png", bbox_inches='tight')
    # Return the plot data (x-axis, signal, upper limit, lower limit)
    return x_axis, plot_signal_data, plot_upperLimit, plot_lowerLimit
