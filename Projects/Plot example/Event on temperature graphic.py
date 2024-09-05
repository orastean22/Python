import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Example data
time = [datetime(2023, 9, 1, 12, 0), datetime(2023, 9, 1, 13, 0), datetime(2023, 9, 1, 14, 0), datetime(2023, 9, 1, 15, 0)]
temperature = [22, 24, 23, 25]

# Event data
event_times = [datetime(2023, 9, 1, 12, 30), datetime(2023, 9, 1, 14, 30)]
event_temperatures = [23, 24]
event_labels = ["error1", "error2"]

# Plotting the temperature data
plt.figure(figsize=(10, 6))
plt.plot(time, temperature, label="Temperature", marker='o')

# Marking events with bigger red dots (adjust the 's' parameter to make the dots larger)
plt.scatter(event_times, event_temperatures, color='red', s=100, zorder=5, label="Events")

# Annotating the dots with labels, time, and temperature values
for i, (event_time, event_temp, event_label) in enumerate(zip(event_times, event_temperatures, event_labels)):
    plt.text(event_time, event_temp + 0.5, f'{event_label}\n{event_temp}°C\n{event_time.strftime("%H:%M")}',
             fontsize=10, ha='center', color='black')

# Formatting the x-axis to show time properly
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
plt.gcf().autofmt_xdate()

# Adding labels and title
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')
plt.title('Temperature vs Time with Events')

# Showing the legend
plt.legend()

# Displaying the plot
plt.show()