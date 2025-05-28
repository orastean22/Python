"""
Definition: The ability of different classes to be treated as instances of the same class through a common interface, usually via method overriding.
Goal: Enable one interface to be used for different underlying data types.
"""

class Cat(Animal):
    def make_sound(self):
        print("Meow!")

animals = [Dog(), Cat()]
for animal in animals:
    animal.make_sound()  # Woof! Meow!
