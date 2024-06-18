# --------------------------------------------------------------------
# -- Python Script File
# -- Created on 04/21/2024 10:30:56
# -- Author: AdrianO
# -- Comment: Decode BitStream B_OUT[14..20] and B_OUT[22..28]
# --------------------------------------------------------------------
"""
    The extract_and_convert function takes three arguments: binary_num (the binary string),
    start (the starting bit position), and end (the ending bit position).
"""
def extract_and_convert(binary_num, start, end):
    # Extract the specific bits
    # Extracts the substring of binary_num from index start to end (inclusive).
    extracted_bits = binary_num[start:end + 1]

    # Convert the extracted substring to a decimal number
    # The second argument (2) tells Python that the input string is in base 2 (binary).
    # The function returns the decimal value of the extracted bits.
    return int(extracted_bits, 2)

#referance normal-32bit(B0-B31) = 0100 0000 0000 0011 1111 1000 0000 0100  (decode B14-20(Dec:127) and B22-28(Dec:0))
#referance normal-29bit(B1-B29) = 0000 0000 0000 0111 1111 1000 0000 0     like in documentation (decode B14-20(Dec:127) and B22-28(Dec:0))
#referance normal-28bit(B1-B28) = 0000 0000 0000 0111 1111 1000 0000       (decode B13-19(Dec:127) and B21-27(Dec:0))

#normal 28 bits
#binary_num = "1111111111110000000111111110"

#inverted 28 bits
#binary_num = "11111111111100000001111111101111"
binary_num = "1111111111110000000111111110"

#first bit is 0;
# Extract bits from 14(or 13) to 20(or 19) and convert to decimal
decimal_14_20 = extract_and_convert(binary_num, 13, 19)
print("Decimal representation of bits 14 to 20 is:", decimal_14_20)

# Extract bits from 22(or 21) to 28(or 27) and convert to decimal
decimal_22_28 = extract_and_convert(binary_num, 21, 27)
print("Decimal representation of bits 22 to 28 is:", decimal_22_28)