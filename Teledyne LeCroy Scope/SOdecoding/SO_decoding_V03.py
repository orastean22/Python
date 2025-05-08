# pip install termcolor
# Detect SO error based on Bout bit 19 and 20 (index 10 and 11 from the right).
# Color code the bits for better visibility using 5bit binary representation.
# in this variant we check the 4-byte representation of the hex value.
    # We check the bits 22 and 23 (index 21 and 22 from the right).

from termcolor import colored

def check_so_error(hex_value):
    """
    Function to detect SO Error in 5-byte representation (40 bits)
    It checks bits 30 and 31 for errors.
    """
    # Convert to binary string and pad with leading zeros for 40-bit representation
    bin_rep = f"{hex_value:040b}"
    
    # Display hex value and formatted binary representation
    print(f"Check {hex(hex_value)} | Binary Representation: ", end="")

    # Loop through the bits and color bit 30 and 31
    for index, bit in enumerate(bin_rep):
        # Bit 30 (index 29) and Bit 31 (index 30) color-coded
        if index == 29:  # Bit 30
            if bit == '1':
                print(colored(bit, 'red'), end='')
            else:
                print(colored(bit, 'green'), end='')
        elif index == 30:  # Bit 31
            if bit == '1':
                print(colored(bit, 'red'), end='')
            else:
                print(colored(bit, 'green'), end='')
        else:
            print(bit, end='')

    # Check for SO Error
    bit_30 = bin_rep[29]
    bit_31 = bin_rep[30]

    if bit_30 == '1' or bit_31 == '1':
        print(f" | ❌ SO Error Detected!")
    else:
        print(f" | ✅ No SO Error.")
    print("-" * 100)


def check_so_error_4byte(four_byte_hex):
    """
    New Function for 4-byte decoding
    Accepts exactly 4 bytes of data, like 0x4B7E0305
    Checks bits 22 and 23 (index 21 and 22)
    """
    # Convert to binary string and pad with leading zeros for 32-bit representation
    bin_rep = f"{four_byte_hex:032b}"
    
    # Display hex value and formatted binary representation
    print(f"Check (4-byte) {hex(four_byte_hex)} | Binary Representation: ", end="")

    # Loop through the bits and color bit 22 and 23
    for index, bit in enumerate(bin_rep):
        # Bit 22 (index 21) and Bit 23 (index 22) color-coded
        if index == 21:  # Bit 22
            if bit == '1':
                print(colored(bit, 'red'), end='')
            else:
                print(colored(bit, 'green'), end='')
        elif index == 22:  # Bit 23
            if bit == '1':
                print(colored(bit, 'red'), end='')
            else:
                print(colored(bit, 'green'), end='')
        else:
            print(bit, end='')

    # Check for SO Error
    bit_22 = bin_rep[21]
    bit_23 = bin_rep[22]

    if bit_22 == '1' or bit_23 == '1':
        print(f" | ❌ SO Error Detected!")
    else:
        print(f" | ✅ No SO Error.")
    print("-" * 100)

# Test with provided examples
print("5-Byte Decoding:")
check_so_error(0x4E4B7E0305)
check_so_error(0x4E4D7E0205)

print("\n4-Byte Decoding:")
check_so_error_4byte(0x4B7E0305)
check_so_error_4byte(0x4D7E0205)





















