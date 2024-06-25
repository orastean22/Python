# ----------------------------------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 04/21/2024 10:30:56  update 24.06.2024
# -- Author: AdrianO
# -- Comment: Decode BitStream B_OUT[14..20] and B_OUT[22..28]
# -- The extract_and_convert function extract the specific bits and convert the extracted substring to a decimal number
# -- in this version read the bits from right to left
# ----------------------------------------------------------------------------------------------------------------------
def extract_and_convert(binary_num, start, end):
    # Reverse the bitstream to read bits from right to left
    reversed_binary_num = binary_num[::-1]

    # Extract the specific bits
    extracted_bits = reversed_binary_num[start:end + 1]

    # Count the number of extracted bits
    num_extracted_bits = len(extracted_bits)

    # Convert the extracted substring to a decimal number
    decimal_value = int(extracted_bits, 2)

    # Return the binary, decimal values, number of extracted bits, and the reversed binary
    return extracted_bits, decimal_value, num_extracted_bits, reversed_binary_num

# 27-bit bitstream from scope
binary_num_27 = "111111100000000111010011111"

# Counting the bits in bitstream
total_bits = len(binary_num_27)

# Extract bits from 12 to 18 (0-based indexing) which corresponds to bits 13 to 19 (1-based indexing)
binary_13_19_27, decimal_13_19_27, num_bits_13_19_27, reversed_binary_num_27 = extract_and_convert(binary_num_27, 12, 18)
print(f"27-bit stream: Bits 13 to 19 (reversed) are: {binary_13_19_27}, Decimal (reversed) is: {decimal_13_19_27}, Number of bits: {num_bits_13_19_27}")

# Extract bits from 20 to 26 (0-based indexing) which corresponds to bits 21 to 27 (1-based indexing)
binary_21_27_27, decimal_21_27_27, num_bits_21_27_27, _ = extract_and_convert(binary_num_27, 20, 26)
print(f"27-bit stream: Bits 21 to 27 (reversed) are: {binary_21_27_27}, Decimal (reversed) is: {decimal_21_27_27}, Number of bits: {num_bits_21_27_27}")

# Display the reversed binary and count bits in binary_num_27
print(f"Reversed binary: {reversed_binary_num_27}")
print(f"Count bits in bitstream:  {total_bits}")







