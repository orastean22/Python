# ----------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 16/10/2024
# -- Update on 15/10/2024
# -- Author: AdrianO
# -- Version 0.1 - display on GUI how many glitch were found on each scope - counter
# -- Script Task: Remote control LabEvent oven for Burin IN 2 (set and read temperature and humidity)
# -- Oven Brand: Votschtechnik
# -- Oven Model: LabEvent T/210/70/5
# -- Setting the IP: 10.30.11.30
# -- Serial Interface ASCII; Address: 1: Baud rate: 9600; Modbus: TCP
# -- pip install pymodbus requests pyvisa

'''
import socket

# IP address and port of the oven
OVEN_IP = '10.30.11.30'
PORT = 5025  # port for SCPI commands

# Create a socket connection to the oven
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((OVEN_IP, PORT))

# SCPI command to set the temperature
scpi_command = f'SET:TEMP {85}\n'  # Temperature in degree

# Send the SCPI command to the oven
sock.sendall(scpi_command.encode('utf-8'))

# Optionally, you can receive a response
response = sock.recv(1024)
print(f"Response: {response.decode('utf-8')}")

# Close the connection
sock.close()

'''
from pymodbus.client import ModbusTcpClient

# IP address and port of the oven controller
OVEN_IP = '10.30.11.30'
PORT = 502  # Standard Modbus port, check the manual

# Modbus register for setting temperature (this must be provided by the manual)
TEMPERATURE_REGISTER = 40001  # Example register, replace with actual

# Create a client connection
client = ModbusTcpClient(OVEN_IP, port=PORT)

# Function to set temperature (in °C)
def set_temperature(temperature):
    # Assuming the temperature value is an integer in degrees Celsius
    client.write_register(TEMPERATURE_REGISTER, temperature)
    print(f"Temperature set to {temperature}°C")

# Set the desired temperature
desired_temperature = 85  # Replace with the desired temperature
set_temperature(desired_temperature)

# Close the client connection
client.close()


# END
# Update 17.10.2024 

















