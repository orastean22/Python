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
    return int(extracted_bits, 2)    # The function returns the decimal value of the extracted bits.

#normal bits
#binary_num = "1111100100100010000111111110"
#binary_num = "1111111111110000000111111110"
#binary_num = "1111100100100010000111111110"


#inverted bits
#binary_num = "0000011011011101111000000001"
#binary_num = "0000000000001111111000000001"
binary_num = "0000011011011101111000000001"





#first bit 0;
# Extract bits from 14 to 20 and convert to decimal
decimal_14_20 = extract_and_convert(binary_num, 13, 19)
print("Decimal representation of bits 14 to 20 is:", decimal_14_20)

# Extract bits from 22 to 28 and convert to decimal
decimal_22_28 = extract_and_convert(binary_num, 21, 27)
print("Decimal representation of bits 22 to 28 is:", decimal_22_28)