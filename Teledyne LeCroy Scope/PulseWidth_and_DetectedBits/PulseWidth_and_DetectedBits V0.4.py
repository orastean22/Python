
import numpy as np
import pandas as pd
from tkinter import Tk, filedialog

def load_waveform():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select waveform CSV file",
        filetypes=[("CSV files", "*.csv")]
    )
    if not file_path:
        print("No file selected. Exiting.")
        exit()
    print(f"Loaded file: {file_path}")
    df = pd.read_csv(file_path, skiprows=5, names=["Time_s", "Voltage_V"])
    time_us = pd.to_numeric(df["Time_s"], errors='coerce') * 1e6
    voltage = pd.to_numeric(df["Voltage_V"], errors='coerce')
    mask = ~time_us.isna() & ~voltage.isna()
    return time_us[mask].values, voltage[mask].values, file_path

def decode_by_width(time_us, voltage, file_path):
    threshold = (np.max(voltage) + np.min(voltage)) / 2
    above = voltage > threshold
    falling_edges = np.where((above[:-1] == True) & (above[1:] == False))[0]
    rising_edges = np.where((above[:-1] == False) & (above[1:] == True))[0]
    falling_times = time_us[falling_edges]
    rising_times = time_us[rising_edges]

    valid_pairs = []
    for f in falling_times:
        candidates = rising_times[rising_times > f]
        if len(candidates) == 0:
            continue
        r = candidates[0]
        width = r - f
        if 0.8 < width < 2.8:
            valid_pairs.append((f, r))

    pulse_widths_us = np.array([r - f for f, r in valid_pairs])
    threshold_us = (1.175 + 1.76) / 2
    bits = [1 if w < threshold_us else 0 for w in pulse_widths_us]
    avg_bit_us = np.mean(pulse_widths_us)
    bitrate_kbps = 1000 / avg_bit_us if avg_bit_us > 0 else 0

    export_df = pd.DataFrame({
        "StartTime_us": [f for f, _ in valid_pairs],
        "PulseWidth_us": pulse_widths_us,
        "Bit": bits
    })
    export_path = file_path.replace(".csv", "_decoded.csv")
    export_df.to_csv(export_path, index=False)

    print(f"Pulse widths detected: {pulse_widths_us}")
    print("\n--- Bitstream Analysis (Width) ---")
    print(f"Detected bits: {bits}")
    print(f"Total bits   : {len(bits)}")
    print(f"Avg bit width: {avg_bit_us:.3f} µs")
    print(f"Bitrate      : {bitrate_kbps:.3f} kbit/s")
    print(f"Results saved to: {export_path}")

def decode_by_falling_edges(time_us, voltage, file_path):
    threshold = (np.max(voltage) + np.min(voltage)) / 2
    above = voltage > threshold
    falling_edges = np.where((above[:-1] == True) & (above[1:] == False))[0]
    falling_times = time_us[falling_edges]
    bit_intervals = np.diff(falling_times)
    valid_intervals = bit_intervals[(bit_intervals > 1.5) & (bit_intervals < 4.0)]
    avg_bit_us = np.mean(valid_intervals)
    bitrate_kbps = 1000 / avg_bit_us if avg_bit_us > 0 else 0

    bit_df = pd.DataFrame({
        "StartTime_us": falling_times[:-1],
        "BitInterval_us": bit_intervals
    })
    output_path = file_path.replace(".csv", "_falling2falling.csv")
    bit_df.to_csv(output_path, index=False)

    print("\n--- Bitstream Analysis (Falling-to-Falling) ---")
    print(f"Valid falling intervals: {len(valid_intervals)}")
    print(f"Avg bit time: {avg_bit_us:.3f} µs")
    print(f"Bitrate     : {bitrate_kbps:.3f} kbit/s")
    print(f"Results saved to: {output_path}")

# === Script entry ===
print("Choose decoding method:")
print("1 - Width-based pulse decoding")
print("2 - Falling-to-falling interval bitrate")
method = input("Enter choice (1 or 2): ")

time_us, voltage, file_path = load_waveform()

if method == "1":
    decode_by_width(time_us, voltage, file_path)
elif method == "2":
    decode_by_falling_edges(time_us, voltage, file_path)
else:
    print("Invalid selection.")

input("\nPress Enter to exit...")
