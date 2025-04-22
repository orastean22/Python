#----------------------------------------------------------------------------------------------------------------------
#-- Python Script File
#-- Created on 22/April/2025
#-- Author: AdrianO
#-- Version 0.1
#-- Script Task:  Log in JSON file all the errors from Bitstream
#-- Comment Vers 0.1: Generate JSON file structure for errors
#-- pip install pandas
#----------------------------------------------------------------------------------------------------------------------

import json
from datetime import datetime
import argparse
import os

# === Configuration: output directory for JSON file ===
OUTPUT_DIR = r"C:\\Python\\Teledyne LeCroy Scope\\StreamViewerbyPython\\Output"

# Simply throw the list of events at this function to generate a JSON file.
def generate_json(events, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(events, f, indent=2)
    print(f"Wrote {len(events)} event(s) to {output_path}")

# Generates a filename like SIC2192Log_tempDev1_250416_132252.json where the timestamp is YYMMDD_HHMMSS
def make_filename(prefix="SIC2192Log_tempDev", index=1):
    ts = datetime.now().strftime("%y%m%d_%H%M%S")
    return f"{prefix}{index}_{ts}.json"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate SIC2192Log JSON from a Python-defined list of events.")
    parser.add_argument("--index", "-i", type=int, default=1,help="Numeric suffix for the file (e.g. tempDev1, tempDev2, ...)")
    parser.add_argument("--out", "-o", default=None,help="Explicit output path. If omitted, a name is auto‑generated.")
    args = parser.parse_args()

    # === Define your input events here ===
    events = []

    # No error case
    base_event = {
        "ErrTimeTick": "2025-04-17 12:30:36.537",
        "ErrorLines": [
            {
                "TimeChange": "12:30:26.538",
                "TimeSpan to Error": "-00:00:09.9989423",
                "Count": 21083,
                "SicData[hex]": "4003F804",
                "Temperature": "81°C",
                "Comment": "",
                "SO": "Ok"
            }
        ]
    }
    events.append(base_event)

    # Sample error events (expand or modify as needed)
    events.append({
        "ErrTimeTick": "2025-04-08 14:20:35.543",
        "ErrorLines": [
            {
                "TimeChange": "14:20:25.544",
                "TimeSpan to Error": "-00:00:09.9991260",
                "Count": 17325,
                "SicData[hex]": "44E3F804",
                "Temperature": "82.88°C",
                "Comment": "",
                "SO": "Ok"
            },
            {
                "TimeChange": "14:20:35.543",
                "TimeSpan to Error": "00:00:00",
                "Count": 1,
                "SicData[hex]": "44E9FC04",
                "Temperature": "83.11°C",
                "Comment": "CRC_b21",
                "SO": "Ok"
            },
            {
                "TimeChange": "14:20:35.547",
                "TimeSpan to Error": "00:00:00.0038492",
                "Count": 95,
                "SicData[hex]": "44EBFC04",
                "Temperature": "83.11°C",
                "Comment": "",
                "SO": "Ok"
            },
            {
                "TimeChange": "14:20:35.598",
                "TimeSpan to Error": "00:00:00.0550875",
                "Count": 1,
                "SicData[hex]": "44E9FC04",
                "Temperature": "83.11°C",
                "Comment": "CRC_b21",
                "SO": "Ok"
            },
            {
                "TimeChange": "14:20:35.599",
                "TimeSpan to Error": "00:00:00.0562659",
                "Count": 3465,
                "SicData[hex]": "44EBFC04",
                "Temperature": "83.11°C",
                "Comment": "",
                "SO": "Ok"
            }
        ]
    })

    # Compute output path
    if args.out:
        output = args.out
    else:
        filename = make_filename(index=args.index)
        output = os.path.join(OUTPUT_DIR, filename)

    generate_json(events, output)
