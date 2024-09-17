from pyvisa import ResourceManager
from pandas import DataFrame
from time import sleep


#=========================================================
class HMC804x:
    """
    Rohde & Schwarz HMC8041 device is initiatied with a vxi connection, and is used to read power supply values. A 
    """

    #-----------------------------------
    def __init__(self, address, resource_manager, name_line, raw=False):
        
        # IP and connecting
        # Ip address might be different for other devices, see the HMC804x SCPI manual
        if raw:
            address_tcpip = f"TCPIP::{address}::5025::SOCKET"
        else:
            address_tcpip = f"TCPIP0::{address}::inst0::INSTR"
    
        self.instrument = resource_manager.open_resource(address_tcpip)

        # NAMING
        # Device name, dataframe column names,
        self.query_id = self.get_query_id()
        self.device_name = self.query_id[14:21]
        self.mult_channel = int(self.device_name[-1])   # The last number of the device name is the amount of channels
        self.name_line = name_line
        self.column_names = self.define_column_names()
        
        # DATA
        # Data list, request string for data
        self.data = []
        self.data_request_string = "MEAS:SCAL:VOLT?;\n;MEAS:SCAL:CURR?;\n;MEAS:SCAL:POW?;\n;MEAS:SCAL:ENER?"
        
        # SETUP 
        # Energy reset and channel selection
        self.enable_reset_energy_meas()
        self.select_channel(1)                          # preset channel to 1 at start

    #-----------------------------------
    #           QUERY
    #-----------------------------------
    def get_query_id(self):
        """Retrieve the IDN from the device"""
        query = "*IDN?"
        response = self.instrument.query(query).strip('\n')
        return response

    #-----------------------------------
    def query(self, query):
        """Simply performs query"""
        value = self.instrument.query(query)
        return value

    #-----------------------------------
    #       SETTING UP
    #-----------------------------------

    #-----------------------------------
    def enable_reset_energy_meas(self):
        """Turns on and resets the energy measurement
        Page 39 of HMC804x SCPI manual"""
        
        # Loop over all channels
        for channel_number in range(1, self.mult_channel+1):
            
            self.select_channel(channel_number)                 # Select the channel
            
            # Turn on measurement
            query = "MEAS:ENER:STAT ON;*OPC?"
            response = int(self.instrument.query(query)[0])

            # Reset if possible
            if response == 1:
                query = "MEAS:ENER:RES;*OPC?"
                response = self.instrument.query(query)
            else:
                raise Exception("Energy measurement could not be turned on")
    
    #-----------------------------------
    def select_channel(self, channel_number):
        """Selects the channel, in case there are more than 1"""
        if self.mult_channel > 1:

            query = f"INST:NSEL {channel_number}"
            self.instrument.write(query)

        else:
            pass # Command does not work for single channeled HMC8041, so pass

    
    #-----------------------------------
    #       READING DATA
    #-----------------------------------
    # Page 38 of HMC804XSCPI manual
    def read_voltage(self):
        """Reads voltage from previously selected channel"""
        query = 'MEAS:SCAL:VOLT?'
        value = self.instrument.query(query)
        return value

    #-----------------------------------
    def read_current(self):
        """Reads current from previously selected channel"""
        query = 'MEAS:SCAL:CURR?'
        value = self.instrument.query(query)
        return value

    #-----------------------------------
    def read_power(self):
        """Reads power from previously selected channel"""
        query = 'MEAS:SCAL:POW?'
        value = self.instrument.query(query)
        return value
    
    #-----------------------------------
    def read_energy(self):
        """Reads energy from previously selected channel since it was resetted"""
        # Must be turned on first!
        query = 'MEAS:SCAL:ENER?'
        value = self.instrument.query(query)
        return value

    #-----------------------------------
    def read_measurement_values(self):
        """Faster way of reading all measurement data, with one request.
        Read all the measurement values at the same time, using the self.data_request_string 
        formatted in __init__.
        Returns a list in the form of four strings containing the values of ['V', 'I', 'W','Ws'] """

        response = self.instrument.query(self.data_request_string)
        list_volt_curr_pow_ener = response.strip('\n').split('\n')
        return list_volt_curr_pow_ener

    #-----------------------------------
    #       FORMATTING DATA
    #-----------------------------------
    def append_measurement_values(self):
        """Perform measurement and format add to the data list, can be used easily
        in a loop."""

        values_all_channels = []    # All measurements

        # Loop over all channel numbers
        for channel_number in range(1, self.mult_channel+1):
            self.select_channel(channel_number)                 # Select the channel
            
            values = self.read_measurement_values()             # Read all values of channel
            values_all_channels.extend(values)                  # Add these to the list of all value

            
        self.data.append(values_all_channels)
        return values_all_channels

    #-----------------------------------
    def add_data_to_df(self):
        """Add all the measured data to a dataframe."""
        df = DataFrame(self.data, columns=self.column_names)
        return df

    #-----------------------------------
    def define_column_names(self):
        """Defines column names for the dataframe that can be made"""
        # Loop over all channel numbers
        col_names = []
        for channel_number in range(1, self.mult_channel+1):
            col_name = [f"{self.device_name} - {self.name_line} - CH{channel_number} Voltage [V]", 
                        f"{self.device_name} - {self.name_line} - CH{channel_number} Current [A]", 
                        f"{self.device_name} - {self.name_line} - CH{channel_number} Power [W]", 
                        f"{self.device_name} - {self.name_line} - CH{channel_number} Energy since inception [J]"]
            col_names.extend(col_name)
        return col_names



if __name__ == "__main__":
    
    try:
        rm = ResourceManager()
        ip_pow_hmc_3v3 = "169.254.145.1"
        hmc8041_3v3 = HMC804x(ip_pow_hmc_3v3, rm, name_line="3V3")   # 1 channel HMC

        print("Beginning loop:")
        while(1):
            values = hmc8041_3v3.append_measurement_values()
            print(values)
            sleep(0.1)

    finally:
        df = hmc8041_3v3.add_data_to_df()
        print(df)
        rm.close()
