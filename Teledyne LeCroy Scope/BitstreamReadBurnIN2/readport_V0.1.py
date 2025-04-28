
import serial.tools.list_ports

def list_stlink_devices():
    HardwareID = "USB VID:PID=0483:374B"
    ports = serial.tools.list_ports.comports()
    
    for port in ports:
        if HardwareID in port.hwid:
            print("-----------")
            print(f"Device   : {port.device}")
            print(f"Name     : {port.name}")
            print(f"Desc     : {port.description}")
            print(f"HWID     : {port.hwid}")
            print(f"Serial # : {port.serial_number}")


list_stlink_devices()
