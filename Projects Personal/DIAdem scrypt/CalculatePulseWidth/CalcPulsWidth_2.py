def calculate_pulse_width(signal_name, threshold):
    signal = Data.Root.ChannelGroups.Item(signal_name).Channels(1)
    signal_data = signal.Values
    sample_rate = signal.Properties("wfSampleRate").Value  # Assuming your waveform has a sample rate property
    
    pulse_widths = []
    pulse_start = 0
    
    # Find pulse edges and calculate pulse widths
    for i in range(1, len(signal_data)):
        if signal_data[i] > threshold and signal_data[i - 1] <= threshold:
            pulse_start = i
        elif signal_data[i] <= threshold and signal_data[i - 1] > threshold and pulse_start > 0:
            pulse_end = i - 1
            # Calculate pulse width
            pulse_width = (pulse_end - pulse_start) / sample_rate
            pulse_widths.append(pulse_width)
            pulse_start = 0
    
    return pulse_widths

 
# Example usage
# signal_name = "YourSignalName" - Waveform signal in the DIAdem Data Portal.

# signal = Data.Root.ChannelGroups.Item(signal_name).Channels(1) retrieves the signal channel from the Data Portal.

# threshold = 5

# pulse_widths = calculate_pulse_width(signal_name, threshold)
# print("Pulse widths:", pulse_widths)
