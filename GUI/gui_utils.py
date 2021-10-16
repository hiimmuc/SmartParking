import os
import random
import sys
import time
import typing

import numpy as np
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QFileDialog, QLabel,
                             QMessageBox, QTableWidgetItem, QVBoxLayout)

try:
    from GUI.gui import *
except:
    from gui import *


class App(Ui_MainWindow, QtWidgets.QWidget):
    def __init__(self, MainWindow):
        super().__init__()
        self.setupUi(MainWindow)

        self.uart_connected = False
        self.rs485_connected = False
        self.is_error = False
        self.running = False

        self.startButton.clicked.connect(self.start_program)
        self.stopButton.clicked.connect(self.stop_program)

        # timer for reading step
        self.timer = QtCore.QTimer()

        # Table
        self.table = {'account': {},
                      'database': {}}

    def start_program(self):
        self.running = True

    def stop_program(self):
        self.running = False

    def popup_msg(self, msg, src_msg='', type_msg='error'):
        """Create popup window to the ui

        Args:
            msg (str): message you want to show to the popup window
            src_msg (str, optional): source of the message. Defaults to ''.
            type_msg (str, optional): type of popup. Available: warning, error, information. Defaults to 'error'.
        """
        try:
            self.popup = QMessageBox()
            if type_msg.lower() == 'warning':
                self.popup.setIcon(QMessageBox.Warning)
            elif type_msg.lower() == 'error':
                self.popup.setIcon(QMessageBox.Critical)
                self.is_error = True
            elif type_msg.lower() == 'info':
                self.popup.setIcon(QMessageBox.Information)

            self.popup.setText(f"[{type_msg.upper()}] -> From: {src_msg}\nDetails: {msg}")
            self.popup.setStandardButtons(QMessageBox.Ok)
            self.popup.exec_()
            print(f'[{type_msg.upper()}]: {msg} from {src_msg}')
        except Exception as e:
            print('-> From: popup_msg', e)

    # +++++++++++++++++++++++++++++++++++ Camera view handling ++++++++++++++++++++++++++++++++++++++++
    def camera_screen(self):
        '''continuous update camera screen using thread
        '''
        pass

    def update_extracted_image(self, screen):
        '''update image on screen 

        Args:
            screen ([str]): which screen to update in or out
        '''
        pass

    # +++++++++++++++++++++++++++++++++++ PLC tracking table handling ++++++++++++++++++++++++++++++++++++++++
    def check_if_expand(self):
        pass

    def update_table(self):
        pass

    def init_table(self):
        pass

    # +++++++++++++++++++++++++++++++++++ CSV files handling ++++++++++++++++++++++++++++++++++++++++

    def read_csv(self, filename):
        '''Read datafrom csv

        Args:
            filename (str): name of file to read
        '''
        pass

    def write_csv(self, filename):
        pass

    def open_csv_in_notepad(self, filename):
        pass
    # +++++++++++++++++++++++++++++++++++ ID part handling ++++++++++++++++++++++++++++++++++++++++

    # track slot in park and money in account after that display on screen

    # +++++++++++++++++++++++++++++++++++ Utils function ++++++++++++++++++++++++++++++++++++++++++

    def update_lcd_led(self, lcd, led, value):
        pass

    def update_label(self, label, value):
        pass

    def update_color_led_label(self, label, color):
        pass


def run():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = App(MainWindow=MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # print(ModbusApp.mro())
    run()
