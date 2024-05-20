#Example: Dictionary for Fruit Prices
# Define a dictionary with fruit names as keys and their prices as values
fruit_prices = {     # fruit_prices: This dictionary contains fruit names as keys and their corresponding prices as values.
    "Apple": 1.20,
    "Banana": 0.50,
    "Cherry": 2.50,
    "Date": 3.00,
    "Elderberry": 1.75
}

# Function to get the price of a fruit
def get_fruit_price(fruit_name):    # This function takes a fruit name as input and returns the price of the fruit.
    return fruit_prices.get(fruit_name, "Fruit not found")
# It uses the .get() method of the dictionary, which returns the value associated with the key fruit_name.
# If the fruit is not found in the dictionary, it returns the default value "Fruit not found".

# Example usage
fruit = input("Enter fruit name: ")
price = get_fruit_price(fruit)       # This line calls the get_fruit_price function with the user's input and stores the result in the variable price.
print(f"The price of {fruit} is {price}")   # This line prints the price of the fruit. It uses an f-string to format the output.

#display; The price of Apple is 1.2
# dictionaries and functions in Python to create a simple lookup tool.


#-------------------------------------------------------------------------------------------------------------------
#Example with Additional Features:
# Nested dictionary with fruits and their attributes
fruit_info = {      # This dictionary contains fruit names as keys. Each key is associated with another dictionary
                    # that holds attributes of the fruit, such as its price and color.
    "Apple": {"price": 1.20, "color": "Red"},
    "Banana": {"price": 0.50, "color": "Yellow"},
    "Cherry": {"price": 2.50, "color": "Red"},
    "Date": {"price": 3.00, "color": "Brown"},
    "Elderberry": {"price": 1.75, "color": "Purple"}
}

# Function to get the information of a fruit
def get_fruit_info(fruit_name):   # This function takes a fruit name as input and returns the dictionary of attributes for that fruit.
    return fruit_info.get(fruit_name, "Fruit not found")
# .get() method of the dictionary, which returns the value associated with the key fruit_name.
# If the fruit is not found in the dictionary, it returns the default value "Fruit not found".

# Example usage
fruit = input("Enter fruit name: ")
info = get_fruit_info(fruit)
if info != "Fruit not found":   # This line checks if the returned information is not "Fruit not found".
    print(f"The price of {fruit} is {info['price']} and its color is {info['color']}")
    # This line prints the price and color of the fruit in a formatted string.
else:
    print(info)  # If the fruit is not found, it prints "Fruit not found".

