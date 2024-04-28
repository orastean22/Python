#Write a code to reverse a number

# Taking input from the user
num = int(input("Enter the Number:"))

# Storing the original number for display later
temp = num

# Initializing a variable to store the reversed number
reverse = 0

# Reversing the number
while num > 0:
    # Extracting the last digit
    remainder = num % 10
    # Appending the digit to the reversed number
    reverse = (reverse * 10) + remainder
    # Removing the last digit from the number
    num = num // 10

# Displaying the original and reversed numbers
print("The Given number is {} and Reverse is {}".format(temp, reverse))

#Display: 102 -> become 201
# 1234 -> 4321




""" Initialization:
num = 123: This is the number entered by the user.
temp = 123: This variable stores the original number for later display.
reverse = 0: This variable will hold the reversed number.
Loop Iteration 1:
remainder = num % 10: The last digit of num is 3.
reverse = (0 * 10) + 3 = 3: The digit 3 is appended to the reverse variable.
num = num // 10 = 12: The last digit 3 is removed from num.
So, after the first iteration:
num = 12
reverse = 3
Loop Iteration 2:
remainder = num % 10: The last digit of num is 2.
reverse = (3 * 10) + 2 = 32: The digit 2 is appended to the reverse variable.
num = num // 10 = 1: The last digit 2 is removed from num.
So, after the second iteration:
num = 1
reverse = 32
Loop Iteration 3:
remainder = num % 10: The last digit of num is 1.
reverse = (32 * 10) + 1 = 321: The digit 1 is appended to the reverse variable.
num = num // 10 = 0: The last digit 1 is removed from num.
So, after the third iteration:
num = 0
reverse = 321
Loop Termination:
Since num is now 0, the loop terminates.
Displaying the result:
The original number was 123 (stored in temp).
The reversed number is 321 (stored in reverse). """