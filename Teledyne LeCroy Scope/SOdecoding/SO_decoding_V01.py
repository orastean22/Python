def check_so_error(hex_value):
    # Convert to binary string and pad with leading zeros for 40-bit representation
    bin_rep = f"{hex_value:040b}"
    print(f"Check {hex(hex_value)}:")
    print(f"Binary Representation: {bin_rep}")

    # Check Bit 19 (position 9) and Bit 20 (position 10) from the right
    bit_19 = bin_rep[-20]  # Position -20 because we read from right to left
    bit_20 = bin_rep[-19]  # Position -19 because we read from right to left
    
    if bit_19 == '1' or bit_20 == '1':
        print("❌ SO Error Detected!")
    else:
        print("✅ No SO Error.")
    print("-" * 50)


# Test with provided examples
check_so_error(0x797B004007)
check_so_error(0x4008014007)
check_so_error(0x43217F0305)
check_so_error(0x43207E0005)

































