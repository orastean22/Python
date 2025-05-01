import numpy as np
import pandas as pd
from tkinter import Tk, filedialog

# === Open file browser to select CSV ===
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

# === Load CSV (skip LeCroy header) ===
try:
    df = pd.read_csv(file_path, skiprows=5, names=["Time_s", "Voltage_V"])
except Exception as e:
    print("Error loading CSV:", e)
    exit()

# === Convert and clean ===
try:
    time_us = pd.to_numeric(df["Time_s"], errors='coerce') * 1e6
    voltage = pd.to_numeric(df["Voltage_V"], errors='coerce')
    mask = ~time_us.isna() & ~voltage.isna()
    time_us = time_us[mask].values
    voltage = voltage[mask].values
except Exception as e:
    print("Conversion error:", e)
    exit()

# === Detect rising/falling edges ===
threshold = (np.max(voltage) + np.min(voltage)) / 2
above = voltage > threshold
falling_edges = np.where((above[:-1] == True) & (above[1:] == False))[0]
rising_edges = np.where((above[:-1] == False) & (above[1:] == True))[0]

falling_times = time_us[falling_edges]
rising_times  = time_us[rising_edges]

# === Match falling → next rising edge, with width filtering ===
valid_pairs = []
for f in falling_times:
    candidates = rising_times[rising_times > f]
    if len(candidates) == 0:
        continue
    r = candidates[0]
    width = r - f
    if 0.8 < width < 2.8:  # µs, valid range for B_OUT
        valid_pairs.append((f, r))

pulse_widths_us = np.array([r - f for f, r in valid_pairs])

# === Bit decoding ===
tBIT = 2.35
#threshold_us = 0.625 * tBIT
threshold_us = (1.175 + 1.76) / 2  # ≈ 1.467 µs
bits = [1 if w < threshold_us else 0 for w in pulse_widths_us]

# === Bitrate ===
avg_bit_us = np.mean(pulse_widths_us)
bitrate_kbps = 1000 / avg_bit_us if avg_bit_us > 0 else 0

# === Export CSV with bits + widths ===
export_df = pd.DataFrame({
    "StartTime_us": [f for f, _ in valid_pairs],
    "PulseWidth_us": pulse_widths_us,
    "Bit": bits
})
export_path = file_path.replace(".csv", "_decoded.csv")
export_df.to_csv(export_path, index=False)

print(f"Pulse widths detected: {pulse_widths_us}")

# === Display results ===
print("\n--- Bitstream Analysis ---")
print(f"Detected bits: {bits}")
print(f"Total bits   : {len(bits)}")
print(f"Avg bit width: {avg_bit_us:.3f} µs")
print(f"Bitrate      : {bitrate_kbps:.3f} kbit/s")
print(f"Results saved to: {export_path}")

input("\nPress Enter to exit...")
# === End of script ===