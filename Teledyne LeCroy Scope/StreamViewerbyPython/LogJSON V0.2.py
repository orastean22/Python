#----------------------------------------------------------------------------------------------------------------------
#-- Python Script File
#-- Created on 22/April/2025
#-- Author: AdrianO
#-- Version 0.2
#-- Script Task:  Log in JSON file all the errors from Bitstream
#-- Comment Vers 0.1: Generate JSON file structure for errors
#-- Comment Vers 0.2: Dynamic generation of error events based on input parameters
#-- pip install pandas
#----------------------------------------------------------------------------------------------------------------------

import json
from datetime import datetime
import os

# === Configuration: output directory for JSON file ===
OUTPUT_DIR = r"C:\\Python\\Teledyne LeCroy Scope\\StreamViewerbyPython\\Output"

#----------------------------------------------------------------------------------------------------------------------
# Simply throw the list of events at this function to generate a JSON file.
def generate_json(events, output_path=None, index=1):
    if output_path is None:
        filename = make_filename(index=index)
        output_path = os.path.join(OUTPUT_DIR, filename)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(events, f, indent=2)
    print(f"Wrote {len(events)} event(s) to {output_path}")


#----------------------------------------------------------------------------------------------------------------------
# Generates a filename like SIC2192Log_tempDev1_250416_132252.json where the timestamp is YYMMDD_HHMMSS
def make_filename(prefix="SIC2192Log_tempDev", index=1):
    ts = datetime.now().strftime("%y%m%d_%H%M%S")
    return f"{prefix}{index}_{ts}.json"

#----------------------------------------------------------------------------------------------------------------------
# Create a base event (no errors)
def create_base_event(err_time, time_change, time_span, count, sic_hex, temperature, comment, so):
    return {
        "ErrTimeTick": err_time,
        "ErrorLines": [
            {
                "TimeChange": time_change,
                "TimeSpan to Error": time_span,
                "Count": count,
                "SicData[hex]": sic_hex,
                "Temperature": temperature,
                "Comment": comment,
                "SO": so
            }
        ]
    }

#----------------------------------------------------------------------------------------------------------------------
# Create an error event with multiple error lines
def create_error_event(err_time, error_lines):
    return {
        "ErrTimeTick": err_time,
        "ErrorLines": error_lines
    }

#----------------------------------------------------------------------------------------------------------------------
# Create an individual error line
def create_error_line(time_change, time_span, count, sic_hex, temperature, comment, so):
    return {
        "TimeChange": time_change,
        "TimeSpan to Error": time_span,
        "Count": count,
        "SicData[hex]": sic_hex,
        "Temperature": temperature,
        "Comment": comment,
        "SO": so
    }

#----------------------------------------------------------------------------------------------------------------------
# Example usage as standalone or from another script
def example():
    events = []

    # No error case
    base_event = create_base_event(
        err_time="2025-04-17 12:30:36.537",
        time_change="12:30:26.538",
        time_span="-00:00:09.9989423",
        count=21083,
        sic_hex="4003F804",
        temperature="°C",
        comment="",
        so="Ok"
    )
    events.append(base_event)

#----------------------------------------------------------------------------------------------------------------------
    # Error case with multiple error lines
    error_lines = [
        create_error_line("14:25:25.544", "-00:00:09.9991260", 17325, "44E3F804", "82.88°C", "", "Error"),
        create_error_line("14:25:35.543", "00:00:00", 1, "44E9FC04", "83.11°C", "CRC_b21", "Error"),
        create_error_line("14:25:35.547", "00:00:00.0038492", 95, "44EBFC04", "83.11°C", "", "Error"),
        create_error_line("14:25:35.598", "00:00:00.0550875", 1, "44E9FC04", "85.11°C", "CRC_b21", "Error"),
        create_error_line("14:25:35.599", "00:00:00.0562659", 3465, "44EBFC04", "86.11°C", "", "Error")
    ]
    events.append(create_error_event("2025-04-08 14:25:35.543", error_lines))

    # Generate the JSON file
    generate_json(events)


#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
# Only runs example when script is executed directly
if __name__ == "__main__":
    example()

