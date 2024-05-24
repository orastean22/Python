import random   #  Imports the random module, which contains functions for generating random numbers and making random choices
import string   #  Imports the string module, which contains a collection of string constants like ascii_letters, digits, and punctuation.

def generate_password(length):
    # Creates a string characters that includes all lowercase and uppercase letters (ascii_letters), digits (digits), and punctuation characters
    characters = string.ascii_letters + string.digits + string.punctuation
    # Randomly selects one character from the characters string.
    password = ''.join(random.choice(characters) for _ in range(length))
    # (_) is a conventional placeholder indicating that the loop variable is not used.
    # .joins all the selected characters into a single string to form the password.
    return password

password_length = 12  # Sets the desired password length to 12 characters
# Calls the generate_password function with the password_length as an argument and stores the result in the generated_password variable.
generate_password = generate_password(password_length)
print("Generated password: " , generate_password)

#display:  Generated password:  $nue\K{m"\Rt