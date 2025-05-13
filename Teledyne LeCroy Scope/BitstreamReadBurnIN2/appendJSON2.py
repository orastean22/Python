import json
from datetime import datetime
import os

# Generates the initialization entry for JSON with temperature and hex value
def generate_error_json(initial_temp=None, initial_hex=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    error_json = {
        "ErrTimeTick": timestamp,
        "ErrorLines": []
    }
    
    temper_str = f"{initial_temp} \u00B0C"  # Unicode for °
    hex_str = initial_hex if initial_hex else "N/A"

    # Add the initial entry with real temperature and hex
    error_json["ErrorLines"].append({
        "TimeChange": timestamp.split()[1], 
        "TimeSpan to Error": "-00:00:00.0000000",
        "Count": 9999,
        "SicData[hex]": hex_str,
        "Temperature": f"{temper_str} " if initial_temp else "N/A",
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

        temp_str = f"{temperature} \u00B0C"  # Unicode for °
        
        # Compute the 4-byte payload
        payload_only = telegram._message & 0xFFFFFFFF  # Masking out the first byte
        
        error_json["ErrorLines"].append({
            "TimeChange": timestamp.split()[1], 
            "TimeSpan to Error": "00:00:00" if i == 0 else f"00:00:00.{i:03d}0000",
            "Count": count,
            "SicData[hex]": f"{hex(payload_only)[2:].upper()}" if telegram else "",
            "Temperature": temp_str,
            "Comment": flag,
            "SO": "Error" if so_error and flag in ["SecondarySideOutOfService_b19", "GateMonitoring_DESAT_b20"] else "Ok"
        })
    
    return error_json

# Save all buffered entries at once to the JSON file
def save_buffer_to_file(buffer, filename):
    
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_data.extend(buffer)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)
