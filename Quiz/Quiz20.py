class Fruit:              # class Fruit
    def __init__(self):   # method (the constructor) that prints '1' when an instance of Fruit is created.
        print('1')


class Apple(Fruit):       # Class Apple (Inherits from Fruit)
    def __init__(self):   # __init__ method that prints '2' when an instance of Apple is created.                 
        print('2')        # This __init__ method in Apple overrides the __init__ method in the Fruit class.

obj = Apple()             # obj = Apple(): This line creates an instance of the Apple class.

#display: 2
# When an instance of Apple is created, the __init__ method in the Apple class is called.
# Since the Apple class has its own __init__ method, the __init__ method in the Fruit class is not called.

#--------------------------------------------------------------------------------------------------------------------

