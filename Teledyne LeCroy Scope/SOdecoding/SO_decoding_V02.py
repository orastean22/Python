# pip install termcolor
# Detect SO error based on Bout bit 19 and 20 (index 10 and 11 from the right).
# Color code the bits for better visibility using 5bit binary representation.


from termcolor import colored

def check_so_error(hex_value):
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





# Test with provided examples
check_so_error(0x4E4B7E0305)
check_so_error(0x4E4D7E0205)





























