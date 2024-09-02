#----------------------------------------------------------------------------------------------------------------------
#-- Python Script File
#-- Created on 09/Sept/2024
#-- Author: AdrianO
#-- Comment: Draw teperature graphic based on all errors from JSON file correlated with the time of BI events.
#----------------------------------------------------------------------------------------------------------------------

import json
from collections import defaultdict

import matplotlib.pyplot as plt

# Example data: Time (in hours) and corresponding temperature (in Celsius)
time = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Time in hours
temperature = [15, 16, 18, 21, 20, 19, 17, 16, 15, 14, 13]  # Temperature in Celsius

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(time, temperature, marker='o', linestyle='-', color='blue')

# Add title and labels
plt.title('Temperature Profile Over Time')
plt.xlabel('Time (hours)')
plt.ylabel('Temperature (°C)')

# Add grid
plt.grid(True)

# Show the plot
plt.show()
