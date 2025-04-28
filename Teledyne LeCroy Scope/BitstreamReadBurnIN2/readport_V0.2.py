import serial.tools.list_ports

def get_stlink_serial_number():
    HardwareID = "USB VID:PID=0483:374B"
    ports = serial.tools.list_ports.comports()
    
    for port in ports:
        if HardwareID in port.hwid:
            return port.serial_number  # Return the serial number immediately

    return None  # If no matching device found


serial_no = get_stlink_serial_number()
print(f"Found Serial Number: {serial_no}")
