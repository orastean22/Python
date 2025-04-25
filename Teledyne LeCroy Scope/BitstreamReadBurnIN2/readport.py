import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

for port in ports:
    print("-----------")
    print(f"Device   : {port.device}")
    print(f"Name     : {port.name}")
    print(f"Desc     : {port.description}")
    print(f"HWID     : {port.hwid}")
    print(f"Serial # : {port.serial_number}")  # ← This is usually your STM32 Nucleo ID
