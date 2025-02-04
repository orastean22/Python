# ----------------------------------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 04/02/2025
# -- Author: AdrianO
# -- Version 0.10 - connect on the scope via TCPIP and read P1 program
# -- pip install pyvisa

import pyvisa as visa
import time
from contextlib import contextmanager
import csv
from datetime import datetime

# Configuration
SCOPE_ADDRESS = "TCPIP0::10.30.11.37::inst0::INSTR"
TIMEOUT = 10000  # Increased timeout to 10 seconds

# Context manager for proper resource cleanup
@contextmanager
def visa_resource_manager():
    rm = visa.ResourceManager()
    try:
        yield rm
    finally:
        rm.close()


# Establish connection with safety checks"""
def connect_to_oscilloscope(rm):
    try:
        scope = rm.open_resource(SCOPE_ADDRESS)
        scope.timeout = TIMEOUT
        scope.read_termination = '\n'  # Explicitly set termination characters
        scope.write_termination = '\n'
        
        # Verify connection
        idn = scope.query("*IDN?").strip()
        if "WaveRunner 8057HD" not in idn:
            raise ValueError("Connected to unexpected instrument")
            
        print(f"Successfully connected to:\n{idn}")
        return scope
        
    except visa.VisaIOError as e:
        print(f"VISA Connection Error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


# Generic measurement reader with enhanced error handling
def read_measurement(scope, parameter):    
    try:
        cmd = f"VBS? 'return=app.Measure.{parameter}.Out.Result.Value'"
        response = scope.query(cmd).strip()
        
        # Clean response - Handle different response formats
        if response.startswith('VBS '):
            value_str = response[4:].strip().strip('"')  # Remove quotes if present
        else:
            value_str = response
            
        value = float(value_str)
        return value * 1e6  # Convert to microseconds
        
    except visa.VisaIOError as e:
        print(f"VISA IO Error: {e}")
        return None
    except (ValueError, TypeError) as e:
        print(f"Conversion error: {e} | Raw response: {repr(response)}")
        return None


def save_to_csv(data):
    with open('measurements.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat()] + data)

def main():
    with visa_resource_manager() as rm:
        scope = connect_to_oscilloscope(rm)
        if not scope:
            return
            
        try:
            p1_value = read_measurement(scope, "P1")
            if p1_value is not None:
                print(f"P1 Measurement Value: {p1_value:.6f} µs")
                
            # Add CSV creation logic here!!!
            
        finally:
            scope.close()

if __name__ == "__main__":
    main()
