class User:    #Class User
    def __init__(self):      # This code defines a class User with a class variable count and a constructor method __init__.
                             # It also initializes User.count to 0 outside the class definition.
        User.count += 1

#Initialization of class variable count
User.count = 0 

# Creating three instances of the User class
obj1 = User() #Then, three instances of the User class are created:
obj2 = User()
obj3 = User() #Each time an instance is created, the __init__ method is called, incrementing User.count by 1.
              #Since three instances of the User class have been created, the output will be: 3

# Printing the count of instances
print(User.count) 

#---------------------------------------------------------------------------------------
#Display 0 if we have _init_ 

#The output of this code will be 0.
#The reason is that the __init__ method is not correctly defined, so it doesn't increment the count when 
#objects are created. Instead, it tries to increment User.count, but User.count does not exist as an instance variable.

#To correct the code, you should change _init_ to __init__:

#Display 3 if we have __init__ 