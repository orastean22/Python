from datetime import datetime, timedelta

def add_time(time_str, hours=0, minutes=0):
    original_time = datetime.strptime(time_str, '%H:%M')
    new_time = original_time + timedelta(hours=hours, minutes=minutes)
    return new_time.strftime('%H:%M')

def subtract_time(time_str, hours=0, minutes=0):
    original_time = datetime.strptime(time_str, '%H:%M')
    new_time = original_time - timedelta(hours=hours, minutes=minutes)
    return new_time.strftime('%H:%M')

def main():
    time_str = input("Enter the time (HH:MM): ")
    operation = input("Enter the operation (add or subtract): ").strip().lower()
    hours = int(input("Enter the number of hours: "))
    minutes = int(input("Enter the number of minutes: "))

    if operation == 'add':
        new_time = add_time(time_str, hours, minutes)
    elif operation == 'subtract':
        new_time = subtract_time(time_str, hours, minutes)
    else:
        print("Invalid operation. Please enter 'add' or 'subtract'.")
        return

    print(f"Original time: {time_str}")
    print(f"New time after {operation}ing {hours} hours and {minutes} minutes: {new_time}")

if __name__ == "__main__":
    main()

