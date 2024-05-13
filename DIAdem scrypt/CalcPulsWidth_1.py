def calculate_pulse_width(signal_data, threshold):
    pulse_widths = []
    pulse_start = 0
    
    # Find pulse edges and calculate pulse widths
    for i in range(1, len(signal_data)):
        if signal_data[i] > threshold and signal_data[i - 1] <= threshold:
            pulse_start = i
        elif signal_data[i] <= threshold and signal_data[i - 1] > threshold and pulse_start > 0:
            pulse_end = i - 1
            # Calculate pulse width
            pulse_width = (pulse_end - pulse_start) / sample_rate()
            pulse_widths.append(pulse_width)
            pulse_start = 0
    
    return pulse_widths

# Example usage
# signal_data = [1, 2, 3, 10, 5, 6, 7, 8, 9, 10, 11, 12, 13, 5, 4, 3, 2, 1]
# threshold = 5

# pulse_widths = calculate_pulse_width(signal_data, threshold)
# print("Pulse widths:", pulse_widths)
