# ----------------------------------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 04/21/2024 10:30:56  update 19.10.2024
# -- Author: AdrianO
# -- V0.5 update script to read bits from 2-12 for NTC temperature.
# -- Comment: Decode BitStream B_OUT[14..20] and B_OUT[22..28]
# -- The extract_and_convert function extracts the specific bits and converts the extracted substring to a decimal number
# -- DecodeB14To20-Bit22To28ATV-V0.3 + inverted bitstream + decode in decimal whole bitstream
# ----------------------------------------------------------------------------------------------------------------------

def invert_bits(binary_num):
    return ''.join('1' if bit == '0' else '0' for bit in binary_num)


def extract_and_convert(binary_num, start, end):
    # Invert the bitstream
    inverted_binary_num = invert_bits(binary_num)

    # Reverse the bitstream to read bits from right to left
    reversed_binary_num = inverted_binary_num[::-1]

    # Extract the specific bits
    extracted_bits = reversed_binary_num[start:end + 1]

    # Count the number of extracted bits
    num_extracted_bits = len(extracted_bits)

    # Convert the extracted substring to a decimal number
    decimal_value = int(extracted_bits, 2)

    # Convert the extracted substring to a decimal number
    decimal_value = int(extracted_bits, 2)

    # Return the binary, decimal values, number of extracted bits, inverted binary, and the reversed binary
    return extracted_bits, decimal_value, num_extracted_bits, inverted_binary_num, reversed_binary_num

def decode_entire_bitstream(binary_num):
    # Convert the entire bitstream to a decimal number
    decimal_value = int(binary_num, 2)
    return decimal_value

# 27-bit bitstream from scope
binary_num_27 = "111111111111000111111000000"

# Counting the bits in bitstream
total_bits = len(binary_num_27)

# Extract bits from 0 to 11 (0-based indexing) which corresponds to bits 1 to 12 (1-based indexing)
binary_1_12_27, decimal_1_12_27, num_bits_1_12_27, _, _ = extract_and_convert(binary_num_27, 0, 11)
print(f"27-bit stream: Bits 1 to 12 (reversed) are: {binary_1_12_27}, Decimal (reversed) is: {decimal_1_12_27}, Number of bits: {num_bits_1_12_27}")

# Extract bits from 12 to 18 (0-based indexing) which corresponds to bits 13 to 19 (1-based indexing)
binary_13_19_27, decimal_13_19_27, num_bits_13_19_27, inverted_binary_num_27, reversed_binary_num_27 = extract_and_convert(
    binary_num_27, 12, 18)
print(f"27-bit stream: Bits 13 to 19 (reversed) are: {binary_13_19_27}, Decimal (reversed) is: {decimal_13_19_27}, Number of bits: {num_bits_13_19_27}")

# Extract bits from 20 to 26 (0-based indexing) which corresponds to bits 21 to 27 (1-based indexing)
binary_21_27_27, decimal_21_27_27, num_bits_21_27_27, _, _ = extract_and_convert(binary_num_27, 20, 26)
print(f"27-bit stream: Bits 21 to 27 (reversed) are: {binary_21_27_27}, Decimal (reversed) is: {decimal_21_27_27}, Number of bits: {num_bits_21_27_27}")

# Decode the entire bitstream to a decimal number
entire_bitstream_decimal = decode_entire_bitstream(binary_num_27)
print(f"27-bit stream: Entire bitstream in decimal is: {entire_bitstream_decimal}")

# Display the inverted binary, reversed binary and count bits in binary_num_27
print(f"Original binary: {binary_num_27}")
print(f"Inverted binary: {inverted_binary_num_27}")
print(f"Reversed binary: {reversed_binary_num_27}")
print(f"Count bits in bitstream:  {total_bits}")









