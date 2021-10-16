import sys
import time
import typing

import numpy as np
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets

from GUI.gui_utils import *

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = App(MainWindow=MainWindow)
MainWindow.show()
sys.exit(app.exec_())
