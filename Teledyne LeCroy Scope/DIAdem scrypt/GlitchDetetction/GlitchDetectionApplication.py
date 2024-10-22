import numpy as np
import sys
sys.path.insert(0, r'\\pictshare01\04_Ops\16_data_science\script\Test_Engineer\GlitchDetection\lib') 
import detectGlitch 
import UIdesign
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (QApplication)
app = QApplication(sys.argv)
window = UIdesign.MainWindow()
sys.exit(app.exec())