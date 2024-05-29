def decode_bitstream(bitstream):
    # Convert the entire bitstream to decimal before inversion
    decimal_before_inversion = int(bitstream, 2)

    # Step 1: Reverse the bitstream
    reversed_bitstream = bitstream[::-1]

    # Step 2: Extract the relevant bits
    # Bits 14 to 20 after reversing (0-indexed) corresponds to positions 13 to 19
    bits_14_to_20 = reversed_bitstream[13:20]
    # Bits 22 to 28 after reversing (0-indexed) corresponds to positions 21 to 27
    bits_22_to_28 = reversed_bitstream[21:28]

    # Step 3: Convert the extracted bit sequences to decimal
    decimal_14_to_20 = int(bits_14_to_20, 2)
    decimal_22_to_28 = int(bits_22_to_28, 2)

    # Convert the entire reversed bitstream to decimal
    decimal_after_inversion = int(reversed_bitstream, 2)

    return decimal_before_inversion, decimal_after_inversion, decimal_14_to_20, decimal_22_to_28


# Example bitstream
bitstream = "1111100100100010000111111110"

# Decode the bitstream
decimal_before_inversion, decimal_after_inversion, decoded_14_to_20, decoded_22_to_28 = decode_bitstream(bitstream)

print(f"Decimal value of the entire bitstream before inversion: {decimal_before_inversion}")
print(f"Decimal value of the entire bitstream after inversion: {decimal_after_inversion}")
print(f"Binary value of bits 14 to 20: {bitstream[::-1][13:20]}, Decimal value: {decoded_14_to_20}")
print(f"Binary value of bits 22 to 28: {bitstream[::-1][21:28]}, Decimal value: {decoded_22_to_28}")

