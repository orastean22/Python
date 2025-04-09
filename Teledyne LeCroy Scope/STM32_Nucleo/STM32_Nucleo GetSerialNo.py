 # pip install pyusb

import usb.core
import usb.util

def get_stlink_serial_number(vendor_id=0x0483, product_id=0x374B):
    # Find the ST-LINK USB device (default ST-LINK/V2-1)
    dev = usb.core.find(idVendor=vendor_id, idProduct=product_id)

    if dev is None:
        raise ValueError("ST-LINK USB device not found. Make sure it is connected.")

    # Retrieve and decode the serial number string from USB descriptor
    serial_number = usb.util.get_string(dev, dev.iSerialNumber)

    return serial_number

if __name__ == "__main__":
    try:
        serial = get_stlink_serial_number()
        print(f"ST-LINK Serial Number: {serial}")
    except Exception as e:
        print(f"Error: {e}")
