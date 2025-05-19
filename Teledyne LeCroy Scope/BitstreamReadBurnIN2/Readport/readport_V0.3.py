import serial.tools.list_ports
import json
import os

def get_stlink_serial_info():
    HardwareID = "USB VID:PID=0483:374B"
    ports = serial.tools.list_ports.comports()
    devices = {}
    device_counter = 1
    
    for port in ports:
        if HardwareID in port.hwid:
            device_name = f"Device {device_counter}"
            devices[device_name] = {
                "com_port": port.device,
                "serial_number": port.serial_number
            }
            device_counter += 1
    
    return devices

def create_json_config():
    serial_infos = get_stlink_serial_info()
    
    if serial_infos:
        # Save JSON configuration file in the same folder as the running script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(current_dir, "stlink_serials.json")
        
        data = {"devices": serial_infos}
        
        with open(save_path, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"Saved {len(serial_infos)} devices to {save_path}")
    else:
        print("No ST-LINK devices found.")

# Call the function to create the JSON config
create_json_config()