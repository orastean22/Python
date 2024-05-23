import os
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyQt6.QtWidgets import (QComboBox, QVBoxLayout, QWidget,
                             QPushButton, QMainWindow, QLabel, QFileDialog, QLineEdit)

matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from nptdms import TdmsFile
sys.path.insert(0, r'\\pictshare01\04_Ops\16_data_science\script\Test_Engineer\GlitchDetection\lib') 
import detectGlitch 

class MainWindow(QMainWindow):
    def __init__(self):
        
        super().__init__()
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)  # Create a QVBoxLayout

         # File selection button
        self.file_select_button = QPushButton("Select File")
        self.file_select_button.clicked.connect(self.on_file_select_clicked)
        self.layout.addWidget(self.file_select_button)
        # Label for data information (initially empty)
        self.data_info_label = QLabel("")
        self.layout.addWidget(self.file_select_button)

        # Create combo boxes for variable selection
        self.combo_signal_data = QComboBox(self)
        self.combo_upper_limit = QComboBox(self)
        self.combo_lower_limit = QComboBox(self)
        
        # Add combo boxes and label to layout
        self.layout.addWidget(QLabel("Select Signal Data:"))
        self.layout.addWidget( self.combo_signal_data)
        self.layout.addWidget(QLabel("Select Upper Limit:"))
        self.layout.addWidget(self.combo_upper_limit)
        self.layout.addWidget(QLabel("Select Lower Limit:"))
        self.layout.addWidget(self.combo_lower_limit)
        
        # Output path selection
        self.output_path_label = QLabel("Output Path:")
        self.output_path_edit = QLineEdit(r"\\pictshare01\04_Ops\16_data_science\script\Test_Engineer\GlitchDetection\Output")
        self.output_path = r"\\pictshare01\04_Ops\16_data_science\script\Test_Engineer\GlitchDetection\Output"
        self.output_path_button = QPushButton("Browse")
        self.output_path_button.clicked.connect(self.on_output_path_clicked)
        self.layout.addWidget(self.output_path_label)
        self.layout.addWidget(self.output_path_edit)
        self.layout.addWidget(self.output_path_button) 

        # Create plot widget
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.layout.addWidget(self.canvas) 

        # Create button to trigger algorithm and plot
        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.on_plot_clicked)

        # Add plot widget and button to layout
        self.layout.addWidget(self.canvas) 
        self.layout.addWidget(self.plot_button)

        self.setWindowTitle("Glitch Detection")
        self.show()


    def on_plot_clicked(self):
        # Get selected variables
        signal_data_name = self.combo_signal_data.currentText()
        upper_limit_name = self.combo_upper_limit.currentText()
        lower_limit_name = self.combo_lower_limit.currentText()
        print(signal_data_name)
        
        # Get the specified group and channel data
        tdms_file = TdmsFile.read(self.file_path)
        group_name = "DUT Data"
        group = tdms_file[group_name]
        signal_data = group[signal_data_name][:]
        upperLimit_data = group[upper_limit_name][:]
        lowerLimit_data = group[lower_limit_name][:] 
        threshold = 5

        pulse_times, pulse_widths = detectGlitch.read_tdms_file(self.file_path, group_name,signal_data_name, threshold)
        # Example usage
        data = pulse_widths[signal_data_name]
        Percent_thereshold =50  # Adjust this value to define the minimum contribution
        Percent_theresholdLow =10
        # Get high contribution numbers
        high_contribution_numbers,low_contribution_numbers = detectGlitch.get_high_contribution_numbers(data, Percent_thereshold,
                                                                                           Percent_theresholdLow)
        print(high_contribution_numbers )
        print(low_contribution_numbers)
#        pulse_times, pulse_widths = read_tdms_file(file_path, group_name, channel_names, threshold)
        channel_name = signal_data_name
        print("All pulses for", channel_name + ":")
        for i, (start, end) in enumerate(pulse_times[channel_name]):
            width = pulse_widths[channel_name][i]
            rise_time = start
            fall_time = end

            print("Pulse", i+1, "- Rise time:", rise_time, "- Fall time:", fall_time, "- Width:", width)

        print("\nGlitches detected (width < 5) for", channel_name + ":")
        if (len(low_contribution_numbers)>0):
            glitches_detected = [i+1 for i, width in enumerate(pulse_widths[channel_name]) if ((width < high_contribution_numbers[0]) & (width <=low_contribution_numbers[0]))]
        else:
            glitches_detected = []
        if glitches_detected:
            print("Pulses with width less than 5:", glitches_detected)
            if(glitches_detected[0]==1):
                glitches_detected = glitches_detected[1:]
            print( glitches_detected )
            
            
            if(len(glitches_detected)>0):
                #if(abs(glitches_detected[0] - glitches_detected[1])<50):
                start = pulse_times[channel_name][glitches_detected[0]][0]
                end = pulse_times[channel_name][glitches_detected[0]][1]
                step=50
                print(glitches_detected)
                plot_data = detectGlitch.get_plotGlitch(signal_data,upperLimit_data,lowerLimit_data,
                                start = pulse_times[channel_name][glitches_detected[0]][0],
                                end = pulse_times[channel_name][glitches_detected[0]][1],
                                step=50)
                print(plot_data[1])
                print(plot_data[3])
                print(plot_data[2])
                    # Clear previous plot (optional)
                # Update the plot with the returned data
                self.ax.cla()  # Clear the axes before plotting again
                self.ax.plot(plot_data[0], plot_data[1], label='Signal')
                self.ax.plot(plot_data[0], plot_data[2], label='Upper Limit')
                self.ax.plot(plot_data[0], plot_data[3], label='Lower Limit')

                # ... (add labels, title, etc. as needed)
                self.ax.legend()
                self.canvas.draw()  # Update the canvas to display the plot
                overall = pd.DataFrame({'SignalDetect':[channel_name],
                    'Glitches Detected':['Yes'],
                    'RowDetected':[str(glitches_detected)]})
                signalDetect = {signal_data_name:np.array([signal_data[start-step:end+step]]).flatten(),
                                upper_limit_name:np.array([upperLimit_data[start-step:end+step]]).flatten(),
                                lower_limit_name:np.array([lowerLimit_data[start-step:end+step]]).flatten()}
                #signalDetect[upper_limit_name] = np.array([upperLimit_data[start-step:end+step]]).flatten()
                #signalDetect[upper_limit_name] = np.array([upperLimit_data[start-step:end+step]]).flatten()
#                     signalDetect = {'test':np.array([signal_data[start-step:end+step]]).flatten()}
                signalDetectDF = pd.DataFrame(signalDetect)
                writer = pd.ExcelWriter(self.output_path+ "\\"+os.path.basename(self.file_path)[:-5]+"_"+signal_data_name+".xlsx", engine='xlsxwriter')
                overall.to_excel(writer,sheet_name = 'summary',index=False)
                signalDetectDF.to_excel(writer, sheet_name ="GlitchesRaw",index=False)
                worksheet = writer.sheets['summary']    
                plot_cell = chr(ord('@')+overall.shape[1]+2)+str(1)
                worksheet.insert_image(plot_cell ,self.output_path+ "\\" +"temp.png" )
                writer.close()
            else:
                sq = np.arange(1, len(signal_data) + 1)
                  # Clear previous plot (optional)
                # Update the plot with the returned data
                self.ax.cla()  # Clear the axes before plotting again
                self.ax.plot(sq, signal_data, label='Signal')
                self.ax.plot(sq, upperLimit_data, label='Upper Limit')
                self.ax.plot(sq, lowerLimit_data, label='Lower Limit')
                self.ax.set_title("No glitches Detected")
                self.ax.legend()
                self.canvas.draw()  # Update the canvas to display the plot
                print(signal_data)
                print("No glitches detected.")

        else:
            sq = np.arange(1, len(signal_data) + 1)
              # Clear previous plot (optional)
            # Update the plot with the returned data
            self.ax.cla()  # Clear the axes before plotting again
            self.ax.plot(sq, signal_data, label='Signal')
            self.ax.plot(sq, upperLimit_data, label='Upper Limit')
            self.ax.plot(sq, lowerLimit_data, label='Lower Limit')
            self.ax.set_title("No glitches Detected")
            self.ax.legend()
            self.canvas.draw()  # Update the canvas to display the plot
            print(signal_data)
            print("No glitches detected.")
        print("\n")

    def on_file_select_clicked(self):

        # Open file dialog to select a file
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Data File", "", "TDMS Files (*.tdms)")
        self.file_path = file_path
        
        
        # Check if a file was selected
        if not file_path:
            return

        # Load data from the selected file
        try:
            self.data = detectGlitch.load_data(file_path)
            self.update_variable_lists()  # Update combo boxes with loaded variables
            self.data_info_label.setText(f"File loaded: {file_path}")  # Display info
        except Exception as e:
            self.data_info_label.setText(f"Error loading file: {e}")  # Display error
#This method is called when the "Browse" button for the output path is clicked.It opens a file dialog and allows the user to select a directory to store the output.

    def on_output_path_clicked(self):

        output_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        self.output_path = output_dir
        # Update the output path edit line with the selected directory
        if output_dir:
            self.output_path_edit.setText(output_dir)

    
    def update_variable_lists(self):
        self.combo_signal_data.clear()
        self.combo_upper_limit.clear()
        self.combo_lower_limit.clear()
        self.combo_signal_data.addItems(self.data)
        self.combo_upper_limit.addItems(self.data)
        self.combo_lower_limit.addItems(self.data)

