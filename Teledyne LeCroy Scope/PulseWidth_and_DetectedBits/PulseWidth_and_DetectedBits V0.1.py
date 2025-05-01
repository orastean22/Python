import numpy as np

# Simulated edge timestamps in µs (for example purposes)
falling_edges = np.array([0, 2.5, 5.0, 7.6, 10.1])    # falling edge timestamps
rising_edges  = np.array([1.2, 4.2, 6.7, 9.3, 11.7])  # corresponding rising edge timestamps

# Calculate pulse widths (µs)
pulse_widths = rising_edges - falling_edges

# Known tBIT from datasheet
tBIT = 2.35
threshold = 0.625 * tBIT  # mid-point between 50% and 75% of tBIT (~1.47 µs)

# Determine logic level: 1 = high (short), 0 = low (long)
bits = [1 if width < threshold else 0 for width in pulse_widths]

print("Pulse widths (µs):", pulse_widths)
print("Detected bits:", bits)
