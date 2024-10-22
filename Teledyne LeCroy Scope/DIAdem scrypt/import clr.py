import clr
clr.AddReference("NationalInstruments.DIAdem.Controls.Data")
clr.AddReference("NationalInstruments.DataPlugin.DataSet")
clr.AddReference("NationalInstruments.DIAdem.Controls.Toolkit")

from NationalInstruments.DIAdem.Controls.Data import DataSetOpenMode
from NationalInstruments.DataPlugin.DataSet import TDMReader

# Define the path to the TDM file
tdm_file_path = "path/to/your/file.tdm"

# Open the TDM file
data_set = TDMReader.Open(tdm_file_path, DataSetOpenMode.Read)

# Get the channels from the data set
channels = data_set.GetChannels()

# Print some information about the channels
for channel in channels:
    print("Channel Name:", channel.Name)
    print("Channel Type:", channel.Type)
    print("Channel Length:", channel.Length)
    print("Channel Data:", channel.GetRawData(0, 10))  # Print first 10 data points
    print("\n")

# Close the data set
data_set.Close()
