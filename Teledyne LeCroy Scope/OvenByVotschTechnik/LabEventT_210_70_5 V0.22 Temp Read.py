# ------------------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 16/10/2024;  Update on 04/12/2024 - First Version that read Temperature and display
# -- Author: AdrianO
# -- Version 0.2 - Read real-time temperature for oven based on socket via TCP/IP
# -- Script Task: Remote control LabEvent oven for Burin IN 2 (set and read temperature + humidity)
# -- Oven Brand: Votschtechnik
# -- Oven Model: LabEvent T/210/70/5
# -- IP: 192.168.122.50
# -- See pdf doc section 6.2.11 command list
# -- Port 7777 or 502 (JUMO diraTRON controller communication) for communication

import socket
import time
from datetime import datetime
import csv

# 
def send_command(ip, port, command):
    """Send a command to the oven and receive a response."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            print(f"Connected to {ip}:{port}")
            s.sendall(command.encode('latin-1'))  # Use 'latin-1' encoding for extended ASCII
            response = s.recv(1024)
            clean_response = response.decode('latin-1').strip()  # Strip unwanted characters
            print(f"Response: {clean_response}")
            return clean_response
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    oven_ip = "127.0.0.1"  # Update with your oven's IP address
    oven_port = 7777  # Port number for communication

    # Separator character (ASCII 182)
    separator = chr(182)

    # Command to fetch temperature using 11002
    temperature_command = f"11002{separator}1{separator}1\r\n"  # Chamber ID = 1, Parameter 1 = 1

    print("Starting real-time temperature monitoring...")

    # Open a CSV file for logging
    with open("temperature_log.csv", "a", newline="") as file:
        writer = csv.writer(file)
        
        # Write headers only if the file is empty
        file.seek(0, 2)  # Move to end of file
        if file.tell() == 0:  # If file is empty
            writer.writerow(["Timestamp", "Temperature"])

        try:
            while True:
                # Send the command to fetch the temperature
                temp_response = send_command(oven_ip, oven_port, temperature_command)

                # Add a timestamp to the response
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Log the result
                if temp_response:
                    writer.writerow([current_time, temp_response])  # Log to CSV
                    file.flush()  # Ensure data is written to the file immediately
                    print(f"{current_time} - Temperature: {temp_response}")
                else:
                    print(f"{current_time} - Failed to fetch temperature.")

                # Wait for a short interval before the next reading
                time.sleep(5)  # Adjust the interval (e.g., 5 seconds)
        except KeyboardInterrupt:
            print("\nReal-time monitoring stopped.")

 # end 20:02 PM