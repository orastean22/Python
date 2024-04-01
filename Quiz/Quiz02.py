# Geometric Progression in Python
# 1.Take input of a, r and n
a = int(input("Enter the value of a: "))
r = int(input("Enter the value of r: "))
n = int(input("Enter the value of n: "))

# 2.Loop for n terms
for i in range(1, n+1):
    t_n = a * r**(i-1)
    print(t_n)

# Output 
# Enter the value for a =1
# Enter the value for r =2
# 1
# 2
# 4
# 8
# 16
# 32
# 64
#....
    
