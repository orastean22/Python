# ----------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 16/10/2024
# -- Update on 04/12/2024 - DRAFT!!!!
# -- Author: AdrianO
# -- Version 0.2 - Read real time temperature for oven based on socket via TCP/IP
# -- Script Task: Remote control LabEvent oven for Burin IN 2 (set and read temperature and humidity)
# -- Oven Brand: Votschtechnik
# -- Oven Model: LabEvent T/210/70/5     
# -- Setting the IP: 192.168.122.50
# -- see pdf doc section 6.2.11 command list
# -- Port 502 (JUMO diraTRON controller communication)

# $01TEMP\n
# $01TEMP\r\n
# $01TEMP

import socket
import time
from datetime import datetime

def read_temperature(ip, port, command):
    try:
        # Create a socket connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))  # Connect to the oven
            print(f"Connected to {ip}:{port}")
            
            # Send the command
            s.sendall(command.encode('ascii'))  # Encode the command
            print(f"Sent command: {command}")
            
            # Receive the response
            response = s.recv(1024).decode('ascii').strip()  # Decode the response
            print(f"Received: {response}")
            return response
    except socket.error as e:
        print(f"Socket error: {e}")
        return None

if __name__ == "__main__":
    # Oven IP and port
    oven_ip = "192.168.122.50"
    oven_port = 502  # 502 for JUMO diraTRON

    # Initialization command (if required)
    initialization_command = "10006 1\r"  # Example command: GET_LNAME
    print("Sending initialization command...")
    response = read_temperature(oven_ip, oven_port, initialization_command)
    print(f"Initialization Response: {response}")

    # ASCII command to request temperature
    temperature_command = "12002 1\r"  # Replace with the correct command format

    # Real-time read temperature with timestamp
    try:
        while True:
            # Read temperature
            temperature = read_temperature(oven_ip, oven_port, temperature_command)
            
            # Get the current timestamp
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Log timestamp and temperature
            if temperature:
                print(f"{current_time} - Temperature: {temperature}")
            else:
                print(f"{current_time} - Failed to read temperature.")
            
            # Wait for a few seconds before the next reading
            time.sleep(5)  # Adjust the interval as needed
    except KeyboardInterrupt:
        print("Real-time logging stopped.")








 
 
   































































