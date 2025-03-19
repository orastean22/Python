# ------------------------------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 19/03/2025
# -- Update on 19/03/2025
# -- Author: AdrianO
# -- Version 0.10 - read bitrate from scope UART table
# -- pip install pyvisa
# ------------------------------------------------------------------------------------------------------------------

import pyvisa

def read_uart_bitrate(decode=1, row=1):
    try:
        rm = pyvisa.ResourceManager()
        scope = rm.open_resource(f'TCPIP0::10.0.0.2::inst0::INSTR')
        scope.timeout = 5000  # timeout 5s

        # Read bitrate from the scope (Column 6)
        vbs_query = f"VBS? 'Return=app.SerialDecode.Decode{decode}.Out.Result.CellValue({row}, 6)'"

        # Print the VBS command
        print(f"VBS command sent: {vbs_query}")

        # Get response from scope
        response = scope.query(vbs_query).strip()

        # Remove the 'VBS ' prefix to isolate numeric value
        if response.startswith("VBS "):
            bitrate_str = response[4:].strip(" '\n\r")
            bitrate_value = float(bitrate_str) / 1000  # Convert from bit/s to kbit/s
            print(f"UART Decode {decode}, Row {row} Bitrate: {bitrate_value:.3f} kbit/s")
        else:
            raise ValueError(f"Unexpected response format: '{response}'")

        scope.close()
        return bitrate_value

    except Exception as e:
        print("Error reading bitrate:", e)
        return None

# Main execution
if __name__ == "__main__":
    bitrate = read_uart_bitrate(decode=1, row=1)
    print("Measured Bitrate:", bitrate)
    print("End of script")