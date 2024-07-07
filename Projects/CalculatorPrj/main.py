# main.py
# import functions from files below:
from add import Add
from substract import Subtract
from multiply import Multiply
from divide import Divide

def main():
    x,y = 10,5
    print(f"Adding {x} and {y} give result =  {Add(x,y)}")
    print(f"Multiplying {x} and {y} gives result = {Multiply(x, y)}")
    print(f"Subtracting {y} from {x} gives result = {Subtract(x, y)}")
    print(f"Dividing {x} by {y} gives result = {Divide(x, y)}")

if __name__ == "__main__":
    main()

# Display
# Adding 10 and 5 give result =  15
# Multiplying 10 and 5 gives result = 50
# Subtracting 5 from 10 gives result = 5
# Dividing 10 by 5 gives result = 2.0
