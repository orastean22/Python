# HMC804x interface for Python
Python interface for Rohde & Schwarz [HMC8041, HMC8042, HMC8043](https://www.rohde-schwarz.com/nl/product/hmc804x) all in one class, using [PyVisa](https://pyvisa.readthedocs.io/en/latest/).


<p align="center">
<img src="https://github.com/HaralDev/HMC804x-Python/blob/master/HMC904x_setup.png" width="400">
  <br>Figure 1: Rohde & Schwarz HMC devices - three HMC8041 and one HMC8042 (top right)
</p>

# Workings
Class works with all three HMC804x devices, might work with other similar product which use [SCPI commands](https://cdn.rohde-schwarz.com/pws/dl_downloads/dl_common_library/dl_manuals/gb_1/h/hmc804x/HMC804x_SCPI_ProgrammersManual_en_02.pdf). The power supply has to be connected to the same network as the computer used.

# Tips
- See the bottom of the script how to implement the instrument in a measurement loop.
- Check if you can interface with HMC device by accessing the IP address in the browser. Find the HMC IP address on the device with "Setup > Interface > PARAMETER". You might need to set the first two numbers to the same address as your PCs address. Example: Computer IP address is 169.154.1.1 and HMC is 180.195.523.12 > set the HMC address to 169.154.x.x (x's do not matter).
- Install the [Rohde&Schwarz VISA tester interface](https://www.rohde-schwarz.com/de/driver-pages/fernsteuerung/3-visa-and-tools_231388.html), it makes playing around with commands a lot easier.
- See the manuals [HMC804x manual](https://scdn.rohde-schwarz.com/ur/pws/dl_downloads/dl_common_library/dl_manuals/gb_1/h/hmc804x/HMC804x_UserManual_de_en_04.pdf) and [HMC804x SCPI Manual](https://cdn.rohde-schwarz.com/pws/dl_downloads/dl_common_library/dl_manuals/gb_1/h/hmc804x/HMC804x_SCPI_ProgrammersManual_en_02.pdf) 
- The type of connection might be different, for me it was a TCPIP0::{ip_address}::inst0::INSTR connection (line 22). See types of connections at [PyVisa documentation](https://pyvisa.readthedocs.io/en/1.8/names.html#visa-resource-syntax-and-examples). 
