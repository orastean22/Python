def fun (a,b):
    if a == 1:
        return b
    else:
        return fun(a-1, a *b )
print(fun(4,2))
    
#display 48
#1st iteration = 3, 4*2
#2nd iteration = 2, 3*4*2
#3rd iteration = 1, 2*3*4*2
#At this point, a is 1, so the function returns b, which is 2*3*4*2 evaluated to 48
#Therefore, the output of print(fun(4,2)) is 48.