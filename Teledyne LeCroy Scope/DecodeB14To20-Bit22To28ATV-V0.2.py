# ----------------------------------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 04/21/2024 10:30:56  update 19.06.2024
# -- Author: AdrianO
# -- Comment: Decode BitStream B_OUT[14..20] and B_OUT[22..28]
# -- The extract_and_convert function extract the specific bits and convert the extracted substring to a decimal number
# reference 32bit(B0-B31) = 0100 0000 0000 0011 1111 1000 0000 0100  (decode B14-20(Dec:127) and B22-28(Dec:0))
# reference 29bit(B1-B29) = 0000 0000 0000 0111 1111 1000 0000 0     like in documentation (decode B14-20(Dec:127) and B22-28(Dec:0))
# reference 28bit(B1-B28) = 0000 0000 0000 0111 1111 1000 0000       (decode B13-19(Dec:127) and B21-27(Dec:0))
# reference 27bit(B1-B27) = 0000 0000 0000 1111 1111 1000 000"       (decode Bit 14-20 position B13-19(Dec:127) and B21-27(Dec:0))
# ----------------------------------------------------------------------------------------------------------------------
def extract_and_convert(binary_num, start, end):
    # Extract the specific bits
    extracted_bits = binary_num[start:end + 1]

    # Convert the extracted substring to a decimal number
    return int(extracted_bits, 2)

# 27-bit bitstream and 28-bit bitstream example
binary_num_27 = "000000000000111111111000000"
binary_num_28 = "0000000000001111111110000000"

# Extract bits from 13 to 19 and convert to decimal for 27-bit bitstream
decimal_13_19_27 = extract_and_convert(binary_num_27, 14, 20)
print("27-bit stream: Decimal representation of bits 13 to 19 is:", decimal_13_19_27)

# Extract bits from 21 to 27 and convert to decimal for 27-bit bitstream
decimal_21_27_27 = extract_and_convert(binary_num_27, 22, 28)
print("27-bit stream: Decimal representation of bits 21 to 27 is:", decimal_21_27_27)

# Extract bits from 14 to 20 and convert to decimal for 28-bit bitstream
decimal_14_20_28 = extract_and_convert(binary_num_28, 14, 20)
print("28-bit stream: Decimal representation of bits 14 to 20 is:", decimal_14_20_28)

# Extract bits from 22 to 28 and convert to decimal for 28-bit bitstream
decimal_22_28_28 = extract_and_convert(binary_num_28, 22, 28)
print("28-bit stream: Decimal representation of bits 22 to 28 is:", decimal_22_28_28)


