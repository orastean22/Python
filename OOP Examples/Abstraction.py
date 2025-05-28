"""
Definition: Hiding complex implementation details and showing only the necessary features of an object.
Goal: Reduce complexity and allow the programmer to focus on interactions at a higher level.
"""

from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        pass

class Dog(Animal):
    def make_sound(self):
        print("Woof!")




if __name__ == "__main__":
    d = Dog()
    d.make_sound()