# file_c.py
def save_result(result, operation):  # Saves the result to a text file - Using Input Parameters
    with open("results.txt", "a") as file:
        file.write(f"{operation.capitalize()} result: {result}\n")










