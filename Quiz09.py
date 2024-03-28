int1 = 10
int2 = 6
if int != int2:
    int2 = ++int1
    print(int1-int2)


   #display 0
    
#In Python, the ++ operator doesn't work as an increment operator. Instead, it's interpreted as two consecutive unary + operators. Therefore, ++int1 doesn't increment int1.
#Let's see how the code executes:

#int1 is assigned the value 10.
#int2 is assigned the value 6.
#The if statement checks if int1 is not equal to int2, which is true (10 != 6).
#Inside the if block:
#int2 is assigned the value of ++int1. However, since ++int1 doesn't actually increment int1, int2 becomes equal to int1.
#Then, it prints the result of subtracting int2 from int1.
#So, after the execution:

#int1 is still 10.
#int2 is updated to 10 as well.
#Therefore, int1 - int2 equals 10 - 10 = 0.