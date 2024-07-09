# Loan calculation
P = 68000  # Principal 68k CHF
annual_rate = 0.04  # interest 4% / year 4/100 = 0.04
r = annual_rate / 12  # Monthly interest rate
n = 60  # Number of payments

# Monthly payment calculation
M = (P * r * (1 + r)**n) / ((1 + r)**n - 1)
print(f"for a total of:  {P} CHF with annual interest of: {annual_rate*100}% the loan credit per month is: {M}")

# display : 1252.32 CHF / month