# This is a sample Python script.
# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from time import sleep

import bitstream
import datetime
import logging
import time
import json
import argparse
import sys
import os
import pymeasure

#from pymeasure.instruments.siglent import SPD3303X
#from pymeasure.instruments.siglent import SDM3055
#from pymeasure.instruments.siglent import SDL1020X
#from pymeasure.instruments.siglent import SDG2042X
#from pymeasure.instruments.rigol import MSO5104
from Temperature import resistance_to_celsius_poly
from pymeasure.instruments.rohdeschwarz import HMP4040
from pymeasure.instruments.tektronix import AFG3152C
#from pymeasure.instruments.lecroy import Lecroy_Waverunner
from pymeasure.experiment import Procedure, Results, Worker
from pymeasure.experiment import IntegerParameter, FloatParameter, Parameter
from pymeasure.log import log, console_log
#from pymeasure.instruments.rigol import M300
from appendJSON2 import generate_error_json, save_buffer_to_file, append_error_json

class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
ch1 = logging.StreamHandler()
ch1.setLevel(logging.DEBUG)
ch1.setFormatter(CustomFormatter('%(asctime)s | %(name)10s | %(levelname)8s | %(filename)-10s:%(lineno)-8d '
                               '| %(message)-120s'))
log.addHandler(ch1)


class gettemp():
    def __init__(self):
        self.prev_val1 = None
        self.prev_val2 = None

    def gettemp(self):
        m300.init()
        time.sleep(1)
        m300.trigger()
        a = m300.fetch().split(',')
        if len(a) == 2:
            val1 = float(a[0])
            val2 = float(a[1])
            self.prev_val1 = val1
            self.prev_val2 = val2
            return val1, val2
        else:
            return self.prev_val1, self.prev_val2

class activity:
    def __init__(self):
        self.counter = 0
        self.counter_max = 4
        self.cycle_sym = ['-', '\\', '|', '/']
    def get(self):
        self.counter += 1
        if self.counter >= self.counter_max:
            self.counter = 0
        return f'[{self.cycle_sym[self.counter]}]'

def load_devices(json_path="stlink_serials.json"):
    with open(json_path, "r") as f:
        return json.load(f)["devices"]

def parse_args():
    # Custom parsing to allow `-1` to be used as argument
    parser = argparse.ArgumentParser(description="Select a device by number.")
    parser.add_argument("device_number", type=str, help="Device number like -1 or -2")
    args, unknown = parser.parse_known_args()

    if not args.device_number.startswith("-") or not args.device_number[1:].isdigit():
        print("Usage: script.py -1")
        sys.exit(1)

    device_num = args.device_number[1:]  # strip the '-' to get the number
    return f"Device {device_num}"


if __name__ == '__main__':
    log.info('Started')
    '''m300 = M300('USB0::0x1AB1::0x0C80::MM3A252700282::INSTR')
    m300.reset()
    time.sleep(1)
    m300.abort()
    time.sleep(1)
    m300.config_temp('TC', 'K', '1','(@401,402)')
    m300.rout_scan('(@401:402)')
    m300.trigger_source('BUS')
    '''
    selected_device = parse_args()
    devices = load_devices()

    if selected_device not in devices:
        print(f"{selected_device} not found in stlink_serials.json")
        sys.exit(1)

    device_info = devices[selected_device]
    
    bs = bitstream.Bitstreamreader(device_info=device_info["serial_number"], device_name=device_info["com_port"])
    doit_seconds = 1
    timeout_seconds = 5
    temp_meas_seconds = 1
    timestamp1 = datetime.datetime.now()
    timestamp1b = datetime.datetime.now()
    timestamp2 = datetime.datetime.now()
    timestamp2b = datetime.datetime.now()
    timestamp3 = datetime.datetime.now()
    temp_ldi = 0
    temp_igd = 0
    enable_ch1 = True
    enable_ch2 = False
    a=activity()
    t=gettemp()

    mapping = {
        'S_UV': 'UnderVoltage_viso_b14',
        'S_OV': 'OverVoltage_viso_b15',
        'S_GM': 'GateMonitoring_b16',
        'S_OT2': 'OverTemp2_GD_b17',
        'S_OT1': 'OverTemp1_GD_b18',
        'S_FLOOS': 'SecondarySideOutOfService_b19',
        'S_DESAT': 'GateMonitoring_DESAT_b20',
        'S_PARITY': 'CRC_b21',
        'P_FLOOS': 'PrimarySideOutOfService_b22',
        'P_OT1': 'OverTemp1CDC_b23',
        'P_OT2': 'OverTemp2CDC_b24',
        'P_OC': 'PrimarySideOverCurrent_b25',
        'P_DTI': 'DeadTimeInsertion_b27',
        'P_ILOCK': 'Interlock_b28',
        'SO': 'SO_Error'
    }

    # New file
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%y%m%d_%H%M%S")

    filename = f"SIC2192Log_tempDev{selected_device[-1]}_{timestamp_str}.json"

    # Buffer in memory
    buffer = []
    buffer_flush_threshold = 5  # flush every 5 telegrams
    last_flush_time = time.time()
    flush_time_interval = 5  # also flush every 5 seconds if no activity

    # Add a flag to track initialization
    initial_entry_added = False
    previous_flaglist = None

    while True:
        if datetime.datetime.now() - timestamp3 > datetime.timedelta(seconds=temp_meas_seconds):
            # temp_ldi, temp_igd = t.gettemp()
            timestamp3 = datetime.datetime.now()

        if (telegram := bs.read_buffer('CH1')) and enable_ch1:
            # used only for debug to see if we have differences between 4 and 5 bytes info received.  
            #print(f"--- RAW TELEGRAM READ ---")
            #print(f"🔹 HEX (4 bytes): {hex(telegram._message & 0xFFFFFFFF)}")
            #print(f"🔹 HEX (5 bytes): {hex(telegram._message)}")
            #first_byte = (telegram._message >> 32) & 0xFF
            #print(f"🔹 First Byte: {hex(first_byte)}")
            #print(f"-------------------------")

            # Generate Initialization JSON Once**
            if not initial_entry_added:
                temp_celsius = resistance_to_celsius_poly(telegram.s_temp)
                payload_only = telegram._message & 0xFFFFFFFF  # Mask to keep only 4 bytes
                hex_val = f"{hex(payload_only)[2:].upper()}".zfill(8)
            
                initial_error = generate_error_json(initial_temp=round(temp_celsius, 2),initial_hex=hex_val)       
                if initial_error:
                    buffer.append(initial_error)
                    log.info("Initialization JSON entry added successfully")
                    initial_entry_added = True  # Prevent future calls
                else:
                    log.warning("Initialization failed. Retrying...")            

            timestamp1b = datetime.datetime.now()   
           
            if telegram.anyflag:
                
                # ------------------------- SO EVENT PROCESSING -------------------------
                so_error_detected = False
                so_hex_event_value = None
                if telegram.so_event:
                    # Original message info -> raw_hex (5 bytes)
                    raw_hex = telegram._message & 0xFFFFFFFFFF  # Mask to keep only 5 bytes
           
                    # Convert to hex and fill with leading zeros if necessary -> Ensure that we have 10 char - 5 bytes in hex representation
                    hex_value = f"{hex(raw_hex)[2:].upper()}".zfill(10)
                                
                    # Take the middle 4 bytes only if the original hex is 10 characters long
                    if len(hex_value) == 10:
                        hex_value = hex_value[2:-2]

                    # Ensure it's exactly 8 characters, if not pad with zeros
                    hex_value = hex_value.zfill(8)
                
                    # Calculate temperature
                    temp_celsius = resistance_to_celsius_poly(telegram.s_temp)   

                    # Log the error event
                    log.error(f'{a.get()} CH1: SO Event detected! TEMP = {temp_celsius:.1f} °C - HEX = {hex_value}')
                    so_hex_event_value = hex_value  # Store the formatted SO event HEX value
                    so_error_detected = True

                # ------------------------- DIFFERENT FLAG EVENT PROCESSING -------------------------
                if telegram.flaglist != previous_flaglist:
                    # log.debug(f'Raw NTC resistance: {telegram.s_temp:.2f} kΩ') # use for debug only 
                    temp_celsius = resistance_to_celsius_poly(telegram.s_temp)

                    # New flaglist, log and append
                    #log.warning(f'{a.get()} CH1: {telegram.flaglist} - {telegram.s_temp} - TEMP-LDI = {temp_ldi}, TEMP-IGD = {temp_igd}')
                    #log.warning(f'{a.get()} CH1: {telegram.flaglist} - TEMP = {temp_celsius:.1f} °C - TEMP-LDI = {temp_ldi}, TEMP-IGD = {temp_igd} - HEX = {hex(telegram._message)[2:].upper()}')
                    
                    # Original message info -> raw_hex (5 bytes)
                    payload_only = telegram._message & 0xFFFFFFFF  # Mask to keep only 5 bytes
                    
                    # Convert to HEX, upper case, and zero-fill to 8 characters if necessary
                    hex_value = f"{hex(payload_only)[2:].upper()}".zfill(10)
                    
                     # Take the middle 4 bytes only if the original hex is 10 characters long
                    if len(hex_value) == 10:
                        hex_value = hex_value[2:-2]

                    # Ensure it's exactly 8 characters, if not pad with zeros
                    hex_value = hex_value.zfill(8)

                    # Log the event/value on the screen real time
                    log.warning(f'{a.get()} CH1: {telegram.flaglist} - TEMP = {temp_celsius:.1f} °C - TEMP-LDI = {temp_ldi}, TEMP-IGD = {temp_igd} - HEX = {hex_value}')
                    
                    # Generate the output list
                    output_list = [mapping.get(item, item) for item in telegram.flaglist]
                    
                    #*************************************OLD variant to check SO based on B19 and B20 trigger error ******************************
                    # Check for the specific SO errors
                    #so_error_detected = False
                    #if 'S_FLOOS' in telegram.flaglist or 'S_DESAT' in telegram.flaglist:
                     #   log.error(f"🔴 SO Error Detected! Flags: {telegram.flaglist} - TEMP = {temp_celsius:.1f} °C")
                      #  so_error_detected = True
                    #******************************************************************************************************************************
                        
                    # ------------------------- JSON APPEND -------------------------
                    error_data = append_error_json(
                        flaglist=output_list,
                        count=1,
                        temperature=f"{round(temp_celsius, 1)}",
                        telegram=telegram,
                        so_error=so_error_detected,
                        hex_value=so_hex_event_value if so_error_detected else hex_value
                    )

                    """# Modify the SO field for the two specific errors - debug only
                    for entry in error_data["ErrorLines"]:
                        if entry["Comment"] in ["SecondarySideOutOfService_b19", "GateMonitoring_DESAT_b20"]:
                            entry["SO"] = "Error Detected"  
                    
                    # If no SO error is detected, log as a regular error
                    if not so_error_detected:
                        error_data = append_error_json(
                            flaglist=output_list,
                            count=1,
                            temperature=f"{round(temp_celsius, 1)}",
                            telegram=telegram
                        )
                    """

                    # Append to buffer for writing
                    buffer.append(error_data)

                    # Update the previous flag list to prevent duplicate logging
                    previous_flaglist = telegram.flaglist.copy()
                    timestamp1 = datetime.datetime.now()
                else:
                    print("Unit is in error or received previous error!")

            elif datetime.datetime.now() - timestamp1 > datetime.timedelta(seconds=doit_seconds):
                # log.debug(f'Raw NTC resistance: {telegram.s_temp:.2f} kΩ')    # use for debug only 
                temp_celsius = resistance_to_celsius_poly(telegram.s_temp)
                if temp_celsius is not None:
                    # log.info(f'{a.get()} CH1: {telegram.flaglist} - {telegram.s_temp} - TEMP-LDI = {temp_ldi}, TEMP-IGD = {temp_igd}')
                    log.info(f'{a.get()} CH1: {telegram.flaglist} - TEMP = {temp_celsius:.1f} °C - TEMP-LDI = {temp_ldi}, TEMP-IGD = {temp_igd}')
                else: 
                    log.warning(f'Invalid resistance value in telegram.s_temp: {telegram.s_temp} kΩ')
                timestamp1 = datetime.datetime.now()

        elif enable_ch1:
            if datetime.datetime.now() - timestamp1b > datetime.timedelta(seconds=timeout_seconds):
                log.error(f'{a.get()} CH1: No Data - TEMP-LDI = {temp_ldi}, TEMP-IGD = {temp_igd}')
                timestamp1b = datetime.datetime.now()

        # Flush if threshold reached or timeout
        if len(buffer) >= buffer_flush_threshold or (time.time() - last_flush_time) > flush_time_interval:
            if buffer:
                save_buffer_to_file(buffer, filename)
                buffer.clear()
                last_flush_time = time.time()
