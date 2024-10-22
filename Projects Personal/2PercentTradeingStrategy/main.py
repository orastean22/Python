# main.py
# import necessary function from userinerface.py and percent.py
from userinterface import get_price_input, display_results
from percent import calculate_take_profit, calculate_stop_loss

def main():
    price = get_price_input()
    take_profit = calculate_take_profit(price) # Calculates the take profit as 2% above the input price.
    stop_loss = calculate_stop_loss(price)     #
    display_results(take_profit, stop_loss)

if __name__ == "__main__":
    main()