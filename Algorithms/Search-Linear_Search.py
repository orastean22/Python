#AdrianO  23.05.2024

#Example 1
#----------------------------------------------------------------------------------------------------------------------
"""
    Perform a linear search for the target in the given list.

    Parameters:
    arr (list): The list to search within.
    target: The element to search for.

    Returns:
    int: The index of the target if found, otherwise -1.
    """
def linear_search(arr, target):

    for index, element in enumerate(arr):    # enumerate(arr) - This func returns index and the element as it iterates over arr.
        if element == target:
            return index    # If the current element matches the target, the function returns the index of the element.
    return -1               # If the element is not find return -1

# Example usage
numbers = [3, 5, 2, 4, 9, 7, 1]     # This sets up a list numbers
target_value = 4                    # target_value to search for.

result = linear_search(numbers, target_value)    # Calls linear_search with the list and target value.

if result != -1:    # If result is not -1, it prints the index where the target was found (index in array - means position).
    print(f"Element found at index: {result}")
    # Output: Element found at index: 3
else:
    print("Element not found in the list")

#display:  Element found at index: 3  because index start from 0 and no 4 is on position 3 in the list


#Example 2 -  simplyfied version
#----------------------------------------------------------------------------------------------------------------------
def linear_search(arr, target):
    for i in range(len(arr)):   # Uses a for loop to iterate over the indices of arr.
        if arr[i] == target:    # Compares each element in arr to target. If a match is found, returns the index i.
            return i            # index means position of the target in the list (list start with position 0 for 1st element
    return -1                   # Return -1 if the target is not found:

# Example usage - Sets up a list numbers and a target_value to search for.
numbers = [3, 5, 2, 4, 9, 7, 1]
target_value = 9

result = linear_search(numbers, target_value)   # Calls linear_search with the list and target value.

if result != -1:
    print(f"Element found at index: {result}")
else:
    print("Element not found in the list")
# Prints the result, indicating whether the target was found and at which index.

#display:  Element found at index: 4