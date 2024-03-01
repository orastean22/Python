def decimal_to_binary_32(decimal):
    # Ensure the input is within the range of a 32-bit signed integer
    if decimal < -2**31 or decimal > 2**31 - 1:
        return "Out of range"

    # Handle negative numbers by converting to 32-bit two's complement representation
    if decimal < 0:
        decimal += 2**32

    # Convert decimal to binary string
    binary_string = bin(decimal)[2:]

    # Pad the binary string with leading zeros to ensure it's 32 bits long
    binary_string = binary_string.zfill(32)

    return binary_string

# Test the function
decimal_number = 123
binary_representation = decimal_to_binary_32(decimal_number)
print("Binary representation of", decimal_number, "is:", binary_representation)
