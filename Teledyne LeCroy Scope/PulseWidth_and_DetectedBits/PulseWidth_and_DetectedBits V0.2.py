import pyvisa
import numpy as np

# Connect to scope
scope_ip = "192.168.142.120"
rm = pyvisa.ResourceManager()
scope = rm.open_resource(f"TCPIP0::{scope_ip}::INSTR")
scope.timeout = 10000

# Configure scope to measure rising and falling edges on channel C3
scope.write("VBS 'App.Measure.P1.Source = \"C3\"'")
scope.write("VBS 'App.Measure.P1.ParamEngine = \"Edge\"'")
scope.write("VBS 'App.Measure.P1.Edge.Direction = \"Falling\"'")
scope.write("VBS 'App.Measure.P1.NumValues = 100'")
scope.write("VBS 'App.Measure.P1.Enable = True'")

scope.write("VBS 'App.Measure.P2.Source = \"C3\"'")
scope.write("VBS 'App.Measure.P2.ParamEngine = \"Edge\"'")
scope.write("VBS 'App.Measure.P2.Edge.Direction = \"Rising\"'")
scope.write("VBS 'App.Measure.P2.NumValues = 100'")
scope.write("VBS 'App.Measure.P2.Enable = True'")

# Read back edge times
falling = scope.query("VBS? 'Return=App.Measure.P1.Values.Text'").strip().replace("\"", "")
rising = scope.query("VBS? 'Return=App.Measure.P2.Values.Text'").strip().replace("\"", "")

# Parse timestamps
falling_edges = np.array([float(x) for x in falling.split(',') if x])
rising_edges  = np.array([float(x) for x in rising.split(',') if x])

# Align and calculate pulse widths
n = min(len(falling_edges), len(rising_edges))
pulse_widths_us = rising_edges[:n] - falling_edges[:n]  # in µs

# Threshold from datasheet
tBIT_us = 2.35
threshold_us = 0.625 * tBIT_us

# Decode bits
bits = [1 if pw < threshold_us else 0 for pw in pulse_widths_us]

# Bitrate calculation
avg_bit_us = np.mean(pulse_widths_us)  # in µs
bitrate_kbps = 1000 / avg_bit_us       # convert to kbps

# Display
print(f"Decoded bits ({len(bits)}):", bits)
print(f"Average bit duration: {avg_bit_us:.3f} µs")
print(f"Estimated bitrate: {bitrate_kbps:.3f} kbit/s")

input("Press Enter to exit...")





