def decimal_to_binary(decimal_num):
    binary_num = ""
    
    while decimal_num > 0:
        remainder = decimal_num % 2
        binary_num = str(remainder) + binary_num
        decimal_num = decimal_num // 2
    
    return binary_num

# Example:
n = int(input("Enter the value of n: "))
decimal_num = n
binary_num = decimal_to_binary(decimal_num)
print("Binary representation of", decimal_num, "is:", binary_num)