# --------------------------------------------------------------------
# -- Python Script File
# -- Created on 04/21/2024 10:30:56
# -- Author: AdrianO
# -- Comment: Decode BitStream B_OUT[14..20] and B_OUT[22..28]
# --------------------------------------------------------------------

def binary_to_decimal(binary_num, start_bit, end_bit):
    # Extract the specific bits range
    binary_segment = binary_num[start_bit:end_bit + 1]

    #Converts this substring to a decimal number.
    decimal_num = 0    #this variable will store the decimal result.

    #which is the exponent for the most significant bit (leftmost bit) of the
    #binary number. Length of the binary number minus one gives the power of the first bit.
    power = len(binary_segment) - 1

    for digit in binary_segment:     #iterate over each digit in the binary number string
        decimal_num += int(digit) * (2 ** power)  #Multiplies the digit by 2 raised to the current power and adds this value to decimal_num
        power -= 1   # Decreases the power by 1 for the next digit (moving right in the binary string).

    # int(digit):Converts the current binary digit (which is a char) to an integer(0 or 1).


    return decimal_num


# The binary number should have 28 bits
binary_num = "1111100100100010000111111110"

#Calls the binary_to_decimal function twice to decode the segments
#from bits 14 to 20 and from bits 22 to 28.

# Decode bits from 14 to 20 (inclusive)
decimal_num_14_20 = binary_to_decimal(binary_num, 14, 20)
print("Decimal representation of bits 14 to 20:", decimal_num_14_20)

# Decode bits from 22 to 28 (inclusive)
decimal_num_22_28 = binary_to_decimal(binary_num, 22, 28)
print("Decimal representation of bits 22 to 28:", decimal_num_22_28)
