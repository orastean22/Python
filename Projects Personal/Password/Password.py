import getpass

database = {'Adriano':'976729'}
username = input("Enter your username: ")
password = getpass.getpass("Enter your password: ")

if username in database:
    if password == database[username]:
        password_2 = getpass.getpass("Enter your password again: ")
        if password == password_2:
            print("Login successful!")
        else:
            print("Passwords do not match.")
    else:
        print("Incorrect password.")
else:
    print("Username not found.")