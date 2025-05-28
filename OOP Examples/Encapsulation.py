"""
Definition: Bundling data (attributes) and methods (functions) that operate on that data into a single unit (class). It restricts direct access to some of the object's components.
Goal: Protect the internal state of an object and only allow modification through defined methods
"""


#***************************************************************************************************************************************
# Section 1: Classic Encapsulation with Methods
# The first block demonstrates the classic approach (and the error if you try direct access).
class Car:
    def __init__(self):
        self.__speed = 0  # private attribute

    def set_speed(self, speed):
        if speed >= 0:
            self.__speed = speed

    def get_speed(self):
        return self.__speed


if __name__ == "__main__":
    car = Car()
    car.set_speed(50)
    print(car.get_speed())  # Output: 50

    # Attempting to access the private attribute directly will raise an error
    # print(my_car.__speed)  # Uncommenting this line will raise an AttributeError

    car.set_speed(-10)      # This will NOT change the speed because of your check
    print(car.get_speed())  # Output: 50

    # Direct access is blocked:
    try:
        print(car.__speed) # This will raise an AttributeError!
    except AttributeError as e:
        print("AttributeError:", e)

    print("\nPythonic Way with @property:")

    
    """
    50
    50
    AttributeError: 'Car' object has no attribute '__speed'.

    
    ERROR: Attempting to access a private attribute directly will raise an AttributeError.
    Traceback (most recent call last):
    File "c:\Python\OOP Examples\Encapsulation.py", line 30, in <module>
    print(car.__speed)      # This will raise an AttributeError
          ^^^^^^^^^^^
    AttributeError: 'Car' object has no attribute '__speed'. Did you mean: 'get_speed'?
    """

#***************************************************************************************************************************************
    # Section 2: Using @property Decorators
    # The second block shows the property approach and the same encapsulation protection.

    class Car2:
        def __init__(self):
            self.__speed = 0

        @property
        def speed(self):
            return self.__speed

        @speed.setter
        def speed(self, value):
            if value >= 0:
                self.__speed = value

    car2 = Car2()
    car2.speed = 100   # Calls the setter
    print(car2.speed)  # Calls the getter

    # Try to set an invalid value
    car2.speed = -5    # Will NOT set speed
    print(car2.speed)  # Still 100

    # Try direct access (should fail)
    try:
        print(car2.__speed)
    except AttributeError as e:
        print("AttributeError:", e)

    """
    Pythonic Way with @property:
    100
    100
    AttributeError: 'Car2' object has no attribute '__speed'.
    ERROR: Attempting to access a private attribute directly will raise an AttributeError.
    """