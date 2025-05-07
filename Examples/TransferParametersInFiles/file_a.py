# file_a.py
from file_b import subtract_numbers     #file_a.py imports the subtract_numbers function from file_b.py.
from file_c import save_result          #file_a.py imports the save_result function from file_c.py.
from file_d import divide_numbers       #file_a.py imports the divide_numbers function from file_d.py.

# Function to add two numbers - Using Input Parameters
def add_numbers(a, b):  
    result = a + b
    save_result(result, "addition")  # Save the result of addition to a file - call save_result function from file_c.py
    return result


# Function to multiply two numbers - Using Input Parameters
def multiply_numbers(a, b):
    result = a * b
    save_result(result, "multiplication")  # Save the result of multiplication to a file - call save_result function from file_c.py
    return result


# Main function to demonstrate the use of functions
if __name__ == "__main__":
    x, y = 10, 5
    print(f"Addition of {x} and {y}: {add_numbers(x, y)}")                 # file_a call function add_numbers       => function a+b
    print(f"Multiplication of {x} and {y}: {multiply_numbers(x, y)}")      # file_a call function multiply_numbers  => function a*b
    print(f"Subtraction of {x} and {y}: {subtract_numbers(x, y)}")         # file_b call function subtract_numbers  => function a-b
    
    division_result = divide_numbers(x, y)  # file_d function a/b
    print(f"Division of {x} and {y}: {division_result}")                   # file_d call function divide_numbers => function a/b
    save_result(division_result, "division")  # Save the result of division to a file - call save_result function from file_c.py