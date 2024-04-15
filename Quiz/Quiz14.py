class Bird:                  #class Bird
    def printsize(self):     #method_1 (self is a reference to the instance of the class. 
                             #It's a convention in Python to use self as the first parameter of instance methods.)
        print('small')       #print small when call method_1

class Eagle(Bird):           #class Eagle (inherits from the Bird class)
    def printsize(self):     #It overrides the printsize(self) method from the Bird class.
        print('large')       #inside the method, it prints the string 'large'.

bird = Bird()                #bird object-an instance of the Bird class is created and assigned to the variable bird.
bird.printsize()             #'bird' is an object with access to the methods defined in the Bird class.

#display small

#The printsize() method of the Bird class is called on the bird object.
#Since the printsize() method is not overridden in the Bird class, it prints 'small'.