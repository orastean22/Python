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

"""
    The invert_binary function takes a binary string as input and returns its inverted version.
"""
def invert_binary(binary_num):
    # Invert the binary string
    inverted_binary = ''.join('1' if bit == '0' else '0' for bit in binary_num)
    return inverted_binary

#binary_num = "1111 1001 0010 0010 0001 1111 1110"
#binary_num = "1111111111111111111111111111"
#binary_num = "1111100100100010000111111110"
binary_num = "1111111111110000000001111111"      # 127 & 0 - OK
#binary_num = "1111100100100010000111111110"

# Invert the binary number before extracting and converting
binary_num = invert_binary(binary_num)
#print("Inverted binary number is:", binary_num)

# First bit 0;
# Extract bits from 14 to 20 and convert to decimal
decimal_14_20 = extract_and_convert(binary_num, 14, 20)
print("Decimal representation of bits 14 to 20 is:", decimal_14_20)

# Extract bits from 22 to 28 and convert to decimal
decimal_22_28 = extract_and_convert(binary_num, 22, 28)
print("Decimal representation of bits 22 to 28 is:", decimal_22_28)
