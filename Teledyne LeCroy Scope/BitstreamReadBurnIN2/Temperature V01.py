
import math
import datetime

def ntc_to_temperature(R_ntc_kohm, a=26.732, b=-0.033):
    return math.log(R_ntc_kohm / a) / b

temperature = ntc_to_temperature(10.0)  # Resistance in kΩ   display 29.80C
#temperature = ntc_to_temperature(52.0)  # Resistance in kΩ   display -20.16C
#temperature = ntc_to_temperature(100.0)  # Resistance in kΩ   display -39.98.0C
print(f"Temperature: {temperature:.2f} °C")











