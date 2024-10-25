# ----------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 16/10/2024
# -- Update on 25/10/2024 - not working yet with inspection elements
# -- Author: AdrianO
# -- Version 0.1 - display on GUI how many glitch were found on each scope - counter
# -- Script Task: Remote control LabEvent oven for Burin IN 2 (set and read temperature and humidity)
# -- Oven Brand: Votschtechnik
# -- Oven Model: LabEvent T/210/70/5     
# -- Setting the IP: 192.168.122.50
# -- Serial Interface ASCII; Address: 1: Baud rate: 9600; Modbus: TCP
# -- weblink: http://192.168.122.50:443/webseason/entrypoint.html

import time

from selenium import webdriver
from selenium.webdriver.edge.service import Service

# Set the path to your Edge WebDriver
webdriver_path = "C:/WebDrivers/msedgedriver.exe"  # Replace with your actual path

# Create a Service object for the WebDriver
service = Service(executable_path=webdriver_path)

# Create an instance of Edge WebDriver
driver = webdriver.Edge(service=service)

# Open the oven web interface
driver.get("http://192.168.122.50:443/webseason/entrypoint.html")

time.sleep(20)
print("20 seconds later...")

# Example of finding an input field and setting temperature
element  = driver.find_element_by_id(By.ID,'username') 
element.send_keys("bi2")

pw_input = driver.find_element_by_id('pw') 
pw_input.send_keys("bi2")

set_button = driver.find_element_by_id('login-button')
set_button.click()

# Example of finding an input field and setting temperature
temp_input = driver.find_element_by_id('layout_1.normal-value-numpad-dialog.container_1.numberpad_1.wutinputfield_1.valueElement')  # Replace with actual input element ID

temp_input.clear()
temp_input.send_keys("85")  # Set temperature to 70°C

# Find and click the "Set" button
set_button = driver.find_element_by_id('numpad-apply')  # Replace with actual button ID
set_button.click()

set_button = driver.find_element_by_id('run-profile-button')  # Replace with actual button ID
set_button.click()

set_button = driver.find_element_by_id('confirm-okay')  # Replace with actual button ID
set_button.click()

# Close the browser
driver.quit()
