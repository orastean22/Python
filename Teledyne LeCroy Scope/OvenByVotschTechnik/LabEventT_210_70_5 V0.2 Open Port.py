# ----------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 16/10/2024
# -- Update on 25/10/2024 - not working yet with inspection elements
# -- Author: AdrianO
# -- Version 0.1 - display on GUI how many glitch were found on each scope - counter
# -- Script Task: Remote control LabEvent oven for Burin IN 2 (set and read temperature and humidity)
# -- Oven Brand: Votschtechnik
# -- Oven Model: LabEvent T/210/70/5     
# -- Setting the IP: 192.168.122.50

import time
import socket

def communicate_with_device(ip, port, command):
    try:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"Attempting to connect to IP: {ip}, Port: {port}")
            # Connect to the device
            s.connect((ip, port))  # Pass as a tuple
            print(f"Connected to {ip}:{port}")

            # Send the command
            s.sendall(command.encode("ascii"))
            print(f"Sent: {command}")

            # Wait for the response
            response = s.recv(1024).decode("ascii").strip()  # Decode using "ascii"
            print(f"Received: {response}")
            return response

    except socket.error as e:
        print(f"Socket error: {e}")
        return None

# Main function
if __name__ == "__main__":
    device_ip = "192.168.122.50"
    device_port = 7777
    ascii_command = "$01I\r"
    response = communicate_with_device(device_ip, device_port, ascii_command)
    if response:
        print(f"Device response: {response}")
    else:
        print("Failed to communicate with the device.")
































































