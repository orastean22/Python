#example 1
#***************************************************************************************************************
x = [1,2,3]      # This line creates a list x containing the elements [1, 2, 3].
y = x.copy()     # This line creates a copy of the list x and assigns it to the variable y.

x.append(4)      # This line appends the value 4 to the list x.    After this line, x will be [1, 2, 3, 4].
print(y)         # this line print the list of y; Since y is a copy of x at the time of its creation,
                 # changes made to x after the copy was made will not affect y.
                 
#display: [1,2,3]


#example 2
#***************************************************************************************************************
list_a = [1,2,3]         # list_a containing the elements [1, 2, 3].
list_b = [4,5,6]         # list_b containing the elements [4, 5, 6].
list_a.append(list_b)    # This line appends list_b as a single element to the end of list_a.
                         # After this line, list_a will become [1, 2, 3, [4, 5, 6]].

print(len(list_a))      # This line prints the length of list_a, which is the number of elements in the list.
                        # Since list_a contains one list as an element, the length will be 4.

#display: 4
      

#example 3
#***************************************************************************************************************
empty_list = []           # This line creates an empty list named empty_list
empty_string = ""         # This line creates an empty string named empty_string
empty_tuple = ()          # This line creates an empty tuple named empty_tuple.

is_none1 = empty_list is None        # This line checks if empty_list is None. Since it's not None, is_none1 will be False.
is_none2 = empty_string is None      # This line checks if empty_string is None. Since it's not None, is_none2 will be False.
is_none3 = empty_tuple is None       # This line checks if empty_tuple is None. Since it's not None, is_none3 will be False.

print(is_none1,is_none2,is_none3)    # This line prints the values of is_none1, is_none2, and is_none3. All of them are False.

#display:  False False False

# n Python, an empty container like a list, string, or tuple is not considered None. They are distinct objects that exist 
# and have a type, even though they are empty. So, the comparisons with None in this code result in False for all cases.
