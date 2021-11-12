import random
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from Communication import *
from Communication.RS485 import RS485
from GUI.gui_utils import *
from LicenseDetection import *
from LicenseOCR import *
from LicenseRecognition import LicenseRecognizer

# *DESC* implement all things :v


class Pipeline:
    def __init__(self) -> None:
        self.rs485 = RS485(port=5)
        self.recognizer = LicenseRecognizer()
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = App(self.MainWindow, self.rs485, self.recognizer)

    def run(self):
        self.MainWindow.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run()
