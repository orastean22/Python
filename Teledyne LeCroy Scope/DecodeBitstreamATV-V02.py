# --------------------------------------------------------------------
# -- Python Script File
# -- Created on 04/22/2024 10:35:56
# -- Author: AdrianO
# -- Comment: Decode BitStream B_OUT[14..20] and B_OUT[22..28] add inverted fct
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
    # The function returns the decimal value and binary representation of the extracted bits.
    return int(extracted_bits, 2), extracted_bits

"""
    The invert_binary function takes a binary string as input and returns its inverted version.
"""
def invert_binary(binary_num):
    # Invert the binary string
    inverted_binary = ''.join('1' if bit == '0' else '0' for bit in binary_num)
    #inverted_binary = binary_num
    return inverted_binary


#binary_num = "1111111111110000000001111111"      # 127 & 0 - OK
binary_num = "0000000000001111111000000001"


# Convert the entire bitstream to decimal before inversion
decimal_before_inversion = int(binary_num, 2)
print("Decimal value before inversion of (Binary: ", binary_num , ") is", decimal_before_inversion)

# Invert the binary number before extracting and converting
binary_num_inverted = invert_binary(binary_num)

# Convert the entire inverted bitstream to decimal
decimal_after_inversion = int(binary_num_inverted, 2)
#print("Decimal value after inversion:", decimal_after_inversion)
print("Decimal value after inversion of  (Binary: " ,binary_num_inverted , ") is", decimal_after_inversion)

# Extract bits from 14 to 20 and convert to decimal
# Function "extract_and_convert" It returns two values: the decimal representation of the extracted bits
# and the binary representation of the extracted bits.
# These two values are assigned to the variables decimal_14_20 and binary_14_20, respectively, using tuple unpacking.
decimal_14_20, binary_14_20 = extract_and_convert(binary_num_inverted, 13, 19)
print("Decimal representation of bits 14 to 20 for (Binary: ", binary_14_20, ") is ", decimal_14_20 )

# Extract bits from 22 to 28 and convert to decimal
decimal_22_28, binary_22_28 = extract_and_convert(binary_num_inverted, 21, 27)
print("Decimal representation of bits 22 to 28 for (Binary:", binary_22_28 , ") is ",  decimal_22_28)
