import sys
import os
import pandas as pd
import numpy as np

from PyQt6.QtWidgets import (QApplication, QComboBox, QVBoxLayout, QWidget,
                             QPushButton, QMainWindow, QLabel,QFileDialog,QLineEdit,
                             QMessageBox)

from PyQt6.QtCore import pyqtSlot
import matplotlib.pyplot as plt
import matplotlib
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
        self.file_select_label = QLabel("Step 1: Select Path with .tdms:")
        self.file_select_button = QPushButton("Browse")
        
        # Label for data information (initially empty)
        self.file_path_label = QLineEdit("") 
        self.layout.addWidget(self.file_select_label)
        self.layout.addWidget(self.file_path_label)
        self.layout.addWidget(self.file_select_button)
        self.file_select_button.clicked.connect(self.on_file_select_clicked)
        
        # Output path selection
        self.output_path_label = QLabel("Step 2: Select Path to store your output:                                       ")
        self.output_path_edit = QLineEdit(r"\\pictshare01\04_Ops\16_data_science\script\Test_Engineer\GlitchDetection\Output")
        self.output_path = r"\\pictshare01\04_Ops\16_data_science\script\Test_Engineer\GlitchDetection\Output"
        self.output_path_button = QPushButton("Browse")
        self.output_path_button.clicked.connect(self.on_output_path_clicked)
        self.layout.addWidget(self.output_path_label)
        self.layout.addWidget(self.output_path_edit)
        self.layout.addWidget(self.output_path_button) 
        
        # File selection button
        self.analyze_button = QPushButton("Start Analyze")
        self.analyze_button.clicked.connect(self.on_plot_clicked)
        self.layout.addWidget(self.analyze_button)
    
        self.setWindowTitle("Glitch Detection")
        self.show()


    def on_plot_clicked(self):
        
        print('start')
        files = []
        extension='.TDMS'
        for filename in os.listdir(self.file_path):
            file_extension = os.path.splitext(filename)[1].lower()
            if file_extension == extension.lower():
                files.append(filename)
        group_name = "DUT Data" 
        for Analyzefile in files:
            
            print('running file:'+Analyzefile)
            channel_names = detectGlitch.load_data(self.file_path+'//'+Analyzefile)
            selectedSignal = [name for name in channel_names if 'Signal' in name]
            for SignalAnalyze in selectedSignal:
                
                # Get selected variables
                signal_data_name = SignalAnalyze
                upper_limit_name = '_'.join(SignalAnalyze.split('_')[0:3])+'_Lim_up'
                lower_limit_name = '_'.join(SignalAnalyze.split('_')[0:3])+'_Lim_low'
                print(signal_data_name)

                # Get the specified group and channel data
                tdms_file = TdmsFile.read(self.file_path+'//'+Analyzefile)
                group_name = "DUT Data"
                group = tdms_file[group_name]
                signal_data = group[signal_data_name][:]
                upperLimit_data = group[upper_limit_name][:]
                lowerLimit_data = group[lower_limit_name][:] 
                threshold = 5

                pulse_times, pulse_widths = detectGlitch.read_tdms_file(self.file_path+'//'+Analyzefile, group_name,signal_data_name, threshold)
                # Example usage
                data = pulse_widths[signal_data_name]
                Percent_thereshold =50  # Adjust this value to define the minimum contribution
                Percent_theresholdLow =10
                # Get high contribution numbers
                high_contribution_numbers,low_contribution_numbers = detectGlitch.get_high_contribution_numbers(data, Percent_thereshold,
                                                                                                   Percent_theresholdLow)

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
                    start = pulse_times[channel_name][glitches_detected[0]][0]
                    end = pulse_times[channel_name][glitches_detected[0]][1]
                    step=50
                    if(len(glitches_detected)>0):
                       
                        print(glitches_detected)
                        plot_data = detectGlitch.get_plotGlitch(signal_data,upperLimit_data,lowerLimit_data,
                                       start = pulse_times[channel_name][glitches_detected[0]][0],
                                       end = pulse_times[channel_name][glitches_detected[0]][1],
                                       step=50)

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
                        writer = pd.ExcelWriter(self.output_path+ "\\"+Analyzefile[:-5]+"_"+signal_data_name+".xlsx", engine='xlsxwriter')
                        overall.to_excel(writer,sheet_name = 'summary',index=False)
                        signalDetectDF.to_excel(writer, sheet_name ="GlitchesRaw",index=False)
                        worksheet = writer.sheets['summary']    
                        plot_cell = chr(ord('@')+overall.shape[1]+2)+str(1)
                        worksheet.insert_image(plot_cell ,r"\\pictshare01\04_Ops\16_data_science\script\Test_Engineer\GlitchDetection\Output\temp.png" )
                        writer.close()
        self.show_success_message()
       
    def on_file_select_clicked(self):

        # Open file dialog to select a file
        tdms_dir = QFileDialog.getExistingDirectory(self, "Select Path with .tdms")
        if tdms_dir:
            self.file_path =tdms_dir
            self.file_path_label.setText(tdms_dir)
        print(tdms_dir)

    def on_output_path_clicked(self):

        output_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        self.output_path = output_dir
        # Update the output path edit line with the selected directory
        if output_dir:
            self.output_path_edit.setText(output_dir)
            
    def show_success_message(self):
        success_message = "Analysis completed successfully!"
        QMessageBox.information(self, "Success", success_message)
        #message_box.exec()  # Display the message box


