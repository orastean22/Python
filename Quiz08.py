x = { }
y = [1,2]
z = [3,4]
print(x.fromkeys(y, z))

#display {1: [3,4] 2: [3,4]}
#this because for position of y =1 will attribute z [3,4] and for y = 2 assign z [3,4]

#It creates a new dictionary with keys from a specified iterable (such as a list or tuple) and sets 
#all values to a default value provided as an argument.