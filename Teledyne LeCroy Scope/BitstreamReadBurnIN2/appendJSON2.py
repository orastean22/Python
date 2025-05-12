import json
from datetime import datetime
import os

def generate_error_json():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    error_json = {
        "ErrTimeTick": timestamp,
        "ErrorLines": []
    }
    
    # Add empty line
    error_json["ErrorLines"].append({
        "TimeChange": timestamp.split()[1], 
        "TimeSpan to Error": "-00:00:00.0000000",
        "Count": 9999,
        "SicData[hex]": "",
        "Temperature": "C",
        "Comment": "",
        "SO": "Ok"
    })
    return error_json

def append_error_json(flaglist, timestamp=None, count=0, temperature=0, telegram=None, so_error=False):    
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    error_json = {
        "ErrTimeTick": timestamp,
        "ErrorLines": []
    } 
   
    # If flaglist is empty, return the base structure
    if not flaglist:
        return error_json
    
    # Add an error line for each flag
    for i, flag in enumerate(flaglist):
        error_json["ErrorLines"].append({
            "TimeChange": timestamp.split()[1], 
            "TimeSpan to Error": "00:00:00" if i == 0 else f"00:00:00.{i:03d}0000",
            "Count": count,
            "SicData[hex]": f"{hex(telegram._message)[2:].upper()}" if telegram else "",
            "Temperature": temperature,
            "Comment": flag,
            "SO": "Error" if so_error and flag in ["SecondarySideOutOfService_b19", "GateMonitoring_DESAT_b20"] else "Ok"
        })
    
    return error_json

# Save all buffered entries at once to the JSON file
def save_buffer_to_file(buffer, filename):
    
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_data.extend(buffer)

    with open(filename, 'w') as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)
