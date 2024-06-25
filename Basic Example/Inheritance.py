
class Animal:              # basic Animal class
    def __init__(self, name):   # It has an __init__ method that initializes an instance with a name.
        self.name = name
    def speak(self):       # method `speak()` that raises a NotImplementedError, indicating that subclasses must implement this method.
        raise NotImplementedError("Subclass must implement abstract method")

class Dog(Animal):         # The `Dog` classes inherit from `Animal` and provide implementation of the `speak()` method.
    def speak(self):       # It overrides the speak method to return a string with the dog’s name and the sound it makes (“Woof!”).
        return f"{self.name} says Woof!"


class Cat(Animal):         # The `Cat` classes inherit from `Animal` and provide implementation of the `speak()` method.
    def speak(self):       # It overrides the speak method to return a string with the cat’s name and the sound it makes (“Meow!”).
        return f"{self.name} says Meow!"

dog = Dog("Buddy")         # An instance of the Dog class named Buddy is created.
cat = Cat("Whiskers")      # create instance of Cat
                           # When you create instances of `Dog` and `Cat`, they can access both their own methods
                           # and the ones inherited from `Animal`
print(dog.speak())  # Output: Buddy says Woof!
print(cat.speak())  # Output: Whiskers says Meow!

