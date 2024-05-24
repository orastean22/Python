from nptdms import TdmsFile
from collections import Counter

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

def calculate_pulse_widths(pulse_times):
    pulse_widths = [end - start + 1 for start, end in pulse_times]
    return pulse_widths

def calculate_average_pulse_width(pulse_widths):
    average_width = sum(pulse_widths) / len(pulse_widths)
    return average_width


def detect_dut_signal_names(tdms_file, group_name):
    group = tdms_file[group_name]

    # Check if group is callable (a function object) and call it if needed
    if callable(group):
        group = group()

    # Get all channel names in the group
    channel_names = group.channels.keys()

    # Extract DUT signal names based on the naming convention
    dut_signal_names = [channel_name for channel_name in channel_names if channel_name.endswith("_Gate_A_Signal") or channel_name.endswith("_Gate_B_Signal")]

    return group, dut_signal_names


def read_tdms_file(file_path, group, threshold):
    pulse_times_dict = {}
    pulse_widths_dict = {}
    for channel_name in group.channels.keys():
        signal_data = group[channel_name][:]
        pulse_times = calculate_pulse_times(signal_data, threshold)
        pulse_times_dict[channel_name] = pulse_times
        pulse_widths = calculate_pulse_widths(pulse_times)
        pulse_widths_dict[channel_name] = pulse_widths
    return pulse_times_dict, pulse_widths_dict

file_path = "C:/Users/aorastean/Desktop/TDMS/mask reset/MaskReset7.tdms"
group_name = "DUT Data"
threshold = 5

tdms_file = TdmsFile.read(file_path)
group, dut_signal_names = detect_dut_signal_names(tdms_file, group_name)
pulse_times, pulse_widths = read_tdms_file(file_path, group, threshold)

for channel_name in pulse_times.keys():
    print("All pulses for", channel_name + ":")
    for i, (start, end) in enumerate(pulse_times[channel_name]):
        width = pulse_widths[channel_name][i]
        rise_time = start
        fall_time = end
        print("Pulse", i+1, "- Rise time:", rise_time, "- Fall time:", fall_time, "- Width:", width)

    print("\nGlitches detected (width < average width) for", channel_name + ":")
    average_width = calculate_average_pulse_width(pulse_widths[channel_name])
    glitches_detected = [i+1 for i, width in enumerate(pulse_widths[channel_name]) if width < average_width]
    if glitches_detected:
        print("Pulses with width less than average:", glitches_detected)
    else:
        print("No glitches detected.")
    print("\n")
