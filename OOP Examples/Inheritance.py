"""
Definition: Mechanism by which one class (child/subclass) inherits the attributes and methods from another class (parent/superclass).
Goal: Reuse code and create a hierarchical relationship between classes.
"""

class Animal:
    def eat(self):
        print("Eating")

class Dog(Animal):
    def bark(self):
        print("Woof!")
