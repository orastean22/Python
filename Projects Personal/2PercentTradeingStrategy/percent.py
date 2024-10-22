#percent.py

# Calculates the take profit as 2% above the input price.
def calculate_take_profit(price):
    return price * 1.02

# Calculates the stop loss as 1% below the input price.
def calculate_stop_loss(price):
    return price * 0.99