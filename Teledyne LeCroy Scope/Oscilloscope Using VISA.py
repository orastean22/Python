import pyvisa
from tkinter import *

# Function to connect to the oscilloscope
def connect_to_oscilloscope():
    try:
        rm = pyvisa.ResourceManager()
        scope = rm.open_resource("TCPIP0::127.0.0.1::INSTR")
        return scope
    except Exception as e:
        print(f"Failed to connect to oscilloscope: {e}")
        return None

# Function to create the main window
def create_main_window(data_payload_str):
    my_window = Tk()
    my_window.title("Data Decoding")
    my_window.geometry('810x500')

    Label(my_window, width=50, text="Field Name", font=("Courier New", 15), fg='black', bg='grey').grid(column=0, row=0)
    Label(my_window, width=15, text="Field Value", font=("Courier New", 15), fg='black', bg='grey').grid(column=1, row=0)
    Button(my_window, width=10, text="Exit", command=my_window.destroy).grid(column=2, row=0)

    labels = [
        "Digitized Temp Signal", "Under Voltage Warning", "Over Voltage Warning",
        "Gate Monitoring Warning", "OT2_GD Over Temperature Warning",
        "OT1_GD Over Temperature Warning", "Secondary Side FluxLink out-of-service Warning",
        "Short Circuit Detection Fault", "Parity Bit of Secondary-to-Primary side Communication",
        "Primary Side FluxLink out-of-service Warning", "OT1_DCDC Over Temperature Warning",
        "OT2_DCDC Over Temperature Warning", "Primary Side DC/DC Controller Over-Current Warning",
        "Not Used", "Dead-Time Insertion Warning", "Interlock Warning"
    ]

    for i, label_text in enumerate(labels, start=1):
        fg_color = 'black' if i % 2 == 0 else 'white'
        bg_color = 'white' if i % 2 == 0 else 'blue'
        Label(my_window, width=50, text=label_text, font=("Courier New", 15), fg=fg_color, bg=bg_color).grid(column=0, row=i, sticky="w")

        if i <= len(data_payload_str) - 3:
            value_fg_color = 'black' if i % 2 == 0 else 'white'
            value_bg_color = 'white' if i % 2 == 0 else 'blue'
            Label(my_window, width=15, text=data_payload_str[i + 2], font=("Courier New", 15), fg=value_fg_color, bg=value_bg_color).grid(column=1, row=i, sticky="w")

    my_window.mainloop()

# Main function
def main():
    scope = connect_to_oscilloscope()
    if scope is None:
        return

    try:
        scope.write("vbs 'Cells = app.SerialDecode.Decode1.Out.Result.CellValue(1, 6) '")
        scope.write("vbs? 'Return = Cells(0,0)'")
        data_payload_str = bin(int(scope.read_raw()) + 2**28)
        create_main_window(data_payload_str)
    except Exception as e:
        print(f"Failed to process data: {e}")
    finally:
        scope.close()

if __name__ == "__main__":
    main()
