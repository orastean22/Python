
def binary_to_decimal(binary_num):
    decimal_num = 0
    power = len(binary_num) - 1
    
    for digit in binary_num:
        decimal_num += int(digit) * (2 ** power)
        power -= 1
    
    return decimal_num

# n = int(input("Enter the value of n in binar : "))
binary_num = "1101"
decimal_num = binary_to_decimal(binary_num)
print("Decimal representation of", binary_num, "is:", decimal_num)
