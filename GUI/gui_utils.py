import os
import random
import sys
import time
import typing

import pandas as pd
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem


class Modbus(QtWidgets.QWidget):
    def __init__(self, MainWindow):
        super().__init__()
        self.setupUi(MainWindow)

    def popup_msg(self, msg):
        pass

    def camera_screen(self):
        pass

    def update_extracted_image(self):
        # extracted image and to box label
        pass

    # +++++++++++++++++++++++++++++++++++
    def check_if_expand(self):
        pass

    def update_table(self):
        pass

    def init_table(self):
        pass

    # +++++++++++++++++++++++++++++++++++

    def read_csv(self, filename):
        pass

    def write_csv(self, filename):
        pass

    def open_csv_in_notepad(self, filename):
        pass
