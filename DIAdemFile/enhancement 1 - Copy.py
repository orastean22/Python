# --------------------------------------------------------------------
# -- Python Script File
# -- Created on 04/21/2024 10:30:56
# -- Author: AdrianO
# -- Comment: Calculate Pulse Width for signal A and signal B
# --------------------------------------------------------------------

""" declare the encoding of the file. It indicates that the file is encoded using UTF-8"""
from matplotlib import pyplot as plt
# -*- coding: utf-8 -*-
from nptdms import TdmsFile
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

# ----------------------------------------------------------------------------------------------------------------------
""" 
 Calculates the width of each pulse based on its start and end times.
    Args:
        pulse_times (list of tuples): List of tuples containing the start and end times of each pulse.
    Returns: list: A list of pulse widths.
"""
def calculate_pulse_widths(pulse_times):
    pulse_widths = [end - start + 1 for start, end in pulse_times]
    return pulse_widths

# ----------------------------------------------------------------------------------------------------------------------
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

# ----------------------------------------------------------------------------------------------------------------------
def get_high_contribution_numbers(data, threshold):
    # Count contributions using Counter
    contributions = Counter(data)

    # Total count of elements
    total_count = len(data)
    for read_key in contributions.keys():
        contributions[read_key] = contributions[read_key] / total_count * 100
    # Calculate contributions using the previous function
    # contributions = count_unique_contributions(data)

    # Filter numbers based on threshold
    high_contribution_numbers = [number for number, contribution in contributions.items() if contribution > threshold]

    return high_contribution_numbers

# ----------------------------------------------------------------------------------------------------------------------
def get_plotGlitch(signal_data,upperLimit,lowerLimit,start,end,step):

    # Create the plot
    fig, ax = plt.subplots()  # Create figure and axes objects
    ax.plot(signal_data[start-step:end+step])
    ax.plot(upperLimit[start-step:end+step])
    ax.plot(lowerLimit[start-step:end+step])

      # Customize the plot (optional)
      # You can add labels, title, etc. using ax methods like ax.set_xlabel(), ax.set_title()

    return fig  # Return the figure object

# ----------------------------------------------------------------------------------------------------------------------
# Example usage

#file_path = r"\\pictshare01\04_Ops\05_Engineering\05_TestEngineering\02_BoardTest\01_TSLH\01_Framework\TestStrategys\2SP0215F2Q\BurnIN\Documentation\DIAdem files glitch detection criteria\TDMS\Glitch3.tdms"
file_path = "C:/Users/aorastean/Desktop/TDMS/Glitch4.tdms"

group_name = "DUT Data"
channel_names = ["DUT1_Gate_A_Signal"]
threshold = 5

"""
# Get the specified group and channel data
tdms_file = TdmsFile.read(file_path)
group = tdms_file[group_name]
signal_data = group[channel_name][:]

upperLimit_data = group['DUT1_Gate_A_Lim_up'][:]
lowerLimit_data = group[ 'DUT1_Gate_A_Lim_low'][:] 

# Example usage
data = pulse_widths['DUT1_Gate_A_Signal']
Percent_thereshold = 70  # Adjust this value to define the minimum contribution

# Get high contribution numbers
high_contribution_numbers = get_high_contribution_numbers(data, Percent_thereshold) """
pulse_times, pulse_widths = read_tdms_file(file_path, group_name, channel_names, threshold)
for channel_name in channel_names:
    print("All pulses for", channel_name + ":")
    for i, (start, end) in enumerate(pulse_times[channel_name]):
        width = pulse_widths[channel_name][i]
        rise_time = start
        fall_time = end
 
        print("Pulse", i+1, "- Rise time:", rise_time, "- Fall time:", fall_time, "- Width:", width)

    print("\nGlitches detected (width < average width) for", channel_name + ":")
    glitches_detected = [i+1 for i, width in enumerate(pulse_widths[channel_name]) if width < high_contribution_numbers[0]]
    if glitches_detected:    """
        if(abs(glitches_detected[0] - glitches_detected[1])<50):
            plot = get_plotGlitch(signal_data,upperLimit_data,lowerLimit_data,
                           start = pulse_times[channel_name][glitches_detected[0]][0],
                           end = pulse_times[channel_name][glitches_detected[0]][1],
                           step=50)
            print(plot)  """
        print("Pulses with width less than 5:", glitches_detected)
    else:
        print("No glitches detected.")
    print("\n")
