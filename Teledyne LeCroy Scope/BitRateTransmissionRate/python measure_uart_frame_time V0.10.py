# ----------------------------------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 19/02/2025
# -- Author: AdrianO
# -- Version 0.10 - Draft version
# -- Script Task: read time for bit frame transmission rate using teledyne scope model LeCroy WR8058HD
# --    time between 1st telegram till receive the 2nd telegram for bit stream
# --    to connect to the scope you need to install on your machine -pip install pyvisa or to upgrade with
# --    command python.exe -m pip install --upgrade pip
# ----------------------------------------------------------------------------------------------------------------------

import pyvisa   # Used for communication with the Teledyne LeCroy WR8058HD via SCPI commands.
import time     # delays and timestamp
import csv      # log data into a CSV

# Constants
SCOPE_IP = "192.168.1.100"   # Actual IP address of the oscilloscope
MEASURE_CHANNEL = "C1"       # Channel where the UART signal is connected
FRAME_THRESHOLD_MIN = 588    # Min frame interval (µs)
FRAME_THRESHOLD_MAX = 631    # Max frame interval (µs)
LOG_FILE = "bit_frame_transmission_log.csv"

# Connect to oscilloscope
rm = pyvisa.ResourceManager()
scope = rm.open_resource(f"TCPIP::{SCOPE_IP}::INSTR")
scope.timeout = 5000  # Timeout to 5s

# Function to set up measurement
#---------------Configures the oscilloscope to measure UART frame timing---------------
def setup_measurement():
    scope.write(f"MEASUrement:PARameter:SOURCE {MEASURE_CHANNEL}")  # Set source channel C1 in our case -selects the input channel
    scope.write("MEASUrement:PARameter:TYPE PER")  # Period measurement (frame rate) -Sets the measurement type to Period, which gives the bit frame transmission rate
    scope.write("MEASUrement:STATistics:STATE ON")  # Enable statistics - helps with averaging and tracking variations.
    print("Measurement setup completed.")


# Function to get frame interval measurement
#---------------Reads the frame transmission interval from the oscilloscope---------------
def get_frame_transmission_time():
    response = scope.query("MEASUrement:PARameter:CURRent:MEAN?")  # Queries the oscilloscope for the current mean period measurement.
    try:
        frame_time = float(response) * 1e6  # Convert to microseconds
        return frame_time
    except ValueError:   # Handles cases where the oscilloscope does not return a valid number.
        print("Invalid response from oscilloscope:", response)
        return None

# Function to log data
#---------------Logs the data in a CSV file for analysis---------------
def log_data(frame_time):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")    # Generates a timestamp for each measurement
    with open(LOG_FILE, mode="a", newline="") as file:  #  Opens the CSV file in append mode ("a") -you can add more data
        writer = csv.writer(file)
        writer.writerow([timestamp, frame_time])   #  Saves the timestamp and frame interval into the CSV file.
    print(f"Logged: {timestamp} | Frame Interval: {frame_time:.2f} µs")


# Main loop
#---------------Displays warnings if transmission times exceed expected limits---------------
#---------------Runs continuously, allowing real-time monitoring---------------
def main():
    setup_measurement()   # Call function to config the scope
    
    # Opens the CSV file in write mode and writes the column headers(time stamp and frame transmission time)
    with open(LOG_FILE, mode="w", newline="") as file:  
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Frame Transmission Time (µs)"])

    while True: 
        frame_time = get_frame_transmission_time() # read the current frame transmission time.
        if frame_time:
            log_data(frame_time)   # log the values
            if frame_time < FRAME_THRESHOLD_MIN or frame_time > FRAME_THRESHOLD_MAX:  # Checks if the value is out of range (below 588 µs or above 631 µs)
                print(f"⚠ Warning: Frame transmission time out of range! ({frame_time:.2f} µs)")
        time.sleep(1)  # Adjust this based on your required logging interval

# Run the script
if __name__ == "__main__":   # Ensures that the script runs only if executed directly.
    try:
        main()      # run the main function
    except KeyboardInterrupt:   # Allows the user to stop the script with CTRL + C without crashing.
        print("\nMeasurement stopped by user.")
    finally:
        scope.close()   # Ensures the connection to the oscilloscope is properly closed when the script stops.

# END 19.02.2025