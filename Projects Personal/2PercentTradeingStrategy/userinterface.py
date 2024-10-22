# userinterface.py

# Prompts the user to enter a price and ensures the input is a valid numeric value.
def get_price_input():
    try:
        price = float(input("Enter the initial price: "))
        return price
    except ValueError:
        print("Invalid input. Please enter a numeric value.")
        return get_price_input()

# Displays the calculated take profit and stop loss values.
def display_results(take_profit, stop_loss):
    print(f"2% Take Profit: {take_profit}")
    print(f"1% Stop Loss: {stop_loss}")