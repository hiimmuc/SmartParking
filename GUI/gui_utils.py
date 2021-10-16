import os
import random
import sys
import time
import typing
from pathlib import Path

import numpy as np
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QFileDialog, QLabel,
                             QMessageBox, QTableWidgetItem, QVBoxLayout)

try:
    from GUI.gui import *
    from GUI.gui_thread import *
except:
    from gui import *
    from gui_thread import *


class App(Ui_MainWindow, VideoThread, QtWidgets.QWidget):
    def __init__(self, MainWindow) -> None:
        super().__init__()
        self.setupUi(MainWindow)

        self.uart_connected = False
        self.rs485_connected = False
        self.is_error = False
        self.running = False

        self.thread = VideoThread()
        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.camera_screen)

        self.startButton.clicked.connect(self.start_program)
        self.stopButton.clicked.connect(self.stop_program)

        # timer for reading step
        self.timer = QtCore.QTimer()

        # Table
        self.table = {'account': {},
                      'database': {},
                      'plc': {}}

    def start_program(self):
        self.thread.start()
        self.running = True

    def stop_program(self):
        self.thread.stop()
        self.running = False
        sys.exit(1)

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

    def convert_cv2qt(self, cv_img):
        '''Convert cv image to qt image to display on gui

        Args:
            cv_img (ndarray): BGR image

        Returns:
            image: RGB image with qt format
        '''
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(640, 360, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    @pyqtSlot(np.ndarray, list)
    def camera_screen(self, cv_img):
        '''continuous update camera screen using thread

        Args:
            cv_img (ndarray): BGR image
        '''
        qt_img = self.convert_cv2qt(cv_img)
        self.screen.setPixmap(qt_img)

    def update_extracted_image(self, screen, cv_img):
        '''update image on screen 

        Args:
            screen ([str]): which screen to update in or out
        '''
        qt_img = self.convert_cv2qt(cv_img)
        if screen == 'view_in':
            self.ViewPlateIn.setPixmap(qt_img)
        elif screen == 'view_out':
            self.ViewPlateOut.setPixmap(qt_img)
        pass

    # +++++++++++++++++++++++++++++++++++ PLC tracking table handling ++++++++++++++++++++++++++++++++++++++++
    def check_if_expand(self, table_name):
        try:
            table = self.tableWidget

            n_rows = table.rowCount()
            data_length = len(self.table[table_name])
            gap = data_length - n_rows
            if gap > 0:
                for i in range(n_rows, data_length):
                    table.insertRow(i)
        except Exception as e:
            self.popup_msg(e, src_msg='check_if_expanding', type_msg='error')

    def update_table(self):
        pass

    def init_table(self):
        pass

    # +++++++++++++++++++++++++++++++++++ CSV files handling ++++++++++++++++++++++++++++++++++++++++

    def read_csv(self, table_name):
        '''Read datafrom csv

        Args:
            filename (str): name of file to read
        '''
        try:
            csv_path = Path(f"backup/{table_name}.csv")
            data = pd.read_csv(csv_path)
            if table_name == 'account':
                self.table[table_name]['id'] = list(data['id'])
                self.table[table_name]['plate'] = list(data['plate'])
                self.table[table_name]['plate_path'] = list(data['plate_path'])
            elif table_name == 'database':
                self.table[table_name]['id'] = list(data['id'])
                self.table[table_name]['money_left'] = list(data['money_left'])
            print(f'[INFO] Read {table_name} table from csv')
        except Exception as e:
            self.popup_msg(f'Error: {e}', 'read_csv', 'error')

    def write_csv(self, table_name):
        '''Write dictionary dataframe to csv

        Args:
            table_name (dict):  data to write
        '''
        try:
            df = pd.DataFrame.from_dict(self.table[table_name])
            csv_path = Path(f"backup/{table_name}.csv")
            df.to_csv(csv_path, index=False)
        except Exception as e:
            self.popup_msg(f'Error: {e}', 'write_csv', 'error')
    # +++++++++++++++++++++++++++++++++++ ID part handling ++++++++++++++++++++++++++++++++++++++++

    # track slot in park and money in account after that display on screen

    # +++++++++++++++++++++++++++++++++++ Utils function ++++++++++++++++++++++++++++++++++++++++++

    def update_lcd_led(self, lcd, value):
        '''Change number in lcd display to value

        Args:
            lcd (str): name of lcd
            value (int): Value to display
        '''
        if lcd == 'TotalSlot':
            lcd_box = self.TotalSlot
        elif lcd == 'MoneyLeft':
            lcd_box = self.MoneyLeft
        elif lcd == 'SlotCount':
            lcd_box = self.SlotCount
        elif lcd == 'IDcard':
            lcd_box = self.IDcard
        lcd_box.display(str(int(value)))

    def update_label(self, label, value):
        '''Change text of label box (only plate number)

        Args:
            label (str): label box name
            value (str): string to display in label box
        '''
        if label == 'extractedInfo':
            self.extractedInfo.setText(value)
        pass

    def update_color_led_label(self, label, color):
        '''Change color of label box to look as led on, off or error

        Args:
            label (srt): name of label box
            color (srt): color to display
        '''
        if label == 'ledTrigger':
            self.ledTrigger.setStyleSheet(f"background-color: {color}")
        elif label == 'Verify':
            self.VerifyBox.setStyleSheet(f"background-color: {color}")
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
