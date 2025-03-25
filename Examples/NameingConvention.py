# Naming convention for variables, functions, classes, and modules in Python 

# *********************************************************************************************
# Case Styles in General:
    #- camelCase: Common in languages like JavaScript and Java for variable and function names.
    #- PascalCase (or UpperCamelCase): Often used for naming classes in many languages.
    #- snake_case: Frequently used in languages like Python for functions and variables.

 # 1. Use lowercase letters for variable names
 # 2. Use underscores to separate words in a variable name
 # 3. Use descriptive names for variables
 # 4. Use uppercase letters for constants
 # 5. Use capitalization to separate words in a constant name
 # 6. Use verbs for function names and nouns for classes
 # 7. Use camel case to concatenate words in a function name
 # 8. Use camel case to concatenate words in a class name
 # 9. Use lowercase letters for module names
# *********************************************************************************************
# Naming Conventions in Python (as per PEP 8):

#• Variables and Function Names:
    #- Use snake_case (e.g., my_variable, calculate_total()).

#• Class Names:
    #- Use PascalCase (e.g., MyClass, UserAccount).

#• Constants:
    #- Use ALL_CAPS_WITH_UNDERSCORES (e.g., DEFAULT_TIMEOUT).

#• Module and Package Names:
    #- Keep them short, all lowercase, and if needed, use underscores (e.g., utils, data_processing).

#• Private Members:
    #- Prefix with an underscore (e.g., _internal_method) to indicate they are intended for internal use.
# *********************************************************************************************


# Below is a self-contained Python examples that demonstrates the naming conventions for variables, functions, classes, and constants:
# *********************************************************************************************
# *********************************************************************************************
# Naming Convention Example_1

# Constant: ALL_CAPS
MAX_COUNT = 100

# Variable: snake_case
my_number = 42

# Function: snake_case
def add_numbers(num1, num2):
    return num1 + num2

# Class: PascalCase
class SampleClass:
    pass

# Private variable: underscore prefix
_private_value = "hidden"

# Simple usage example
result = add_numbers(my_number, 8)
print("Result:", result)

# ********************************************************************************************* 
# *********************************************************************************************
# Naming Convention Example_2

# Constants (all uppercase with underscores)
MAX_SIZE = 100
DEFAULT_TIMEOUT = 30

# Function names in snake_case
def calculate_total(numbers):
    """Calculate the sum of a list of numbers."""
    total = 0  # Variable in snake_case
    for number in numbers:
        total += number
    return total

# Class names in PascalCase
class UserAccount:
    """A class representing a user account."""

    def __init__(self, username, email):
        # Public instance variables using snake_case
        self.username = username
        self.email = email
        # Private instance variable (prefixed with an underscore)
        self._password_hash = None

    def set_password(self, password):
        """Set the user's password by hashing it."""
        self._password_hash = self._hash_password(password)

    # Private method (prefixed with an underscore)
    def _hash_password(self, password):
        """A dummy private method to simulate password hashing."""
        return hash(password)

    def get_account_info(self):
        """Return formatted account information."""
        return f"Username: {self.username}, Email: {self.email}"


if __name__ == "__main__":
    # Create an instance of UserAccount
    user_account = UserAccount("john_doe", "john@example.com")
    user_account.set_password("secure_password")

    # Calculate total of numbers using the snake_case function
    numbers = [1, 2, 3, 4, 5]
    total = calculate_total(numbers)
    print(f"Total: {total}")
    print(user_account.get_account_info())


# Constants are defined with all uppercase letters.
# Function names (like calculate_total) and variables use snake_case.
# Class names (like UserAccount) use PascalCase.
# Private members (like _password_hash and _hash_password) are prefixed with an underscore.
# This follows Python’s PEP 8 style guidelines for naming conventions.