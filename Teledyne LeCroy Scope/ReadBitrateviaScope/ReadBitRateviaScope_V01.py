# ------------------------------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 19/03/2025
# -- Update on 19/03/2025
# -- Author: AdrianO
# -- Version 0.10 - read bitrate from scope UART table
# -- pip install pyvisa
# ------------------------------------------------------------------------------------------------------------------

import pyvisa
import time

def read_uart_bitrate(scope_ip, decode=1, row=1):
    try:
        rm = pyvisa.ResourceManager()
        scope = rm.open_resource(f'TCPIP0::{scope_ip}::inst0::INSTR')
        scope.timeout = 5000  # timeout 5s

        # Proper VBS query (use query() to write and read)
        vbs_query = f"VBS? 'Return=app.SerialDecode.Decode{decode}.Out.Result.CellValue({row},4)'"

        # Use query to directly obtain the response
        response = scope.query(vbs_query).strip()

        # Check raw response
        print(f"Raw response from scope: '{response}'")

        # Remove "VBS" prefix and quotes, parse to float
        if response.startswith("VBS '") and response.endswith("'"):
            bitrate_str = response[5:-1].replace("kbit/s", "").strip()
            bitrate_value = float(bitrate_str)
            print(f"UART Decode {decode}, Row {row} Bitrate: {bitrate_value} kbit/s")
        else:
            raise ValueError(f"Unexpected response format: '{response}'")

        scope.close()
        return bitrate_value

    except Exception as e:
        print("Error reading bitrate:", e)
        return None


# Main execution
if __name__ == "__main__":
    scope_ip = '10.0.0.2'
    bitrate = read_uart_bitrate(scope_ip, decode=1, row=1)
    print("Measured Bitrate:", bitrate)




