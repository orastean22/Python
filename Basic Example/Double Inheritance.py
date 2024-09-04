class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError("Subclass must implement abstract method")

class Pet:
    def __init__(self, owner):
        self.owner = owner

    def owner_info(self):
        return f"Owner: {self.owner}"

class Dog(Animal, Pet):
    def __init__(self, name, owner):
        Animal.__init__(self, name)
        Pet.__init__(self, owner)

    def speak(self):
        return f"{self.name} says Woof!"

# Creating an instance of Dog
dog = Dog("Buddy", "Alice")

# Accessing methods from both parent classes
print(dog.speak())         # Output: Buddy says Woof!
print(dog.owner_info())    # Output: Owner: Alice