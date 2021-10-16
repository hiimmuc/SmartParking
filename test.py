import random
import sys
import time
import typing

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets

from GUI.gui_utils import *
from LicenseRecognition import *


def gui():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = App(MainWindow=MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


def model():
    # Choose random motorbike image from the dataset
    num = random.randint(0, 2489)
    image_name = "xemay" + str(num) + ".jpg"
    # img_path = os.path.join(r"backup\Number Plate Dataset\yolo_plate_dataset", image_name)
    img_path = r"backup\Number Plate Dataset\yolo_plate_dataset\xemay1434.jpg"

    recognizer = LicenseRecognizer()
    recognizer.extract_info(img_path, only_ocr=False, preprocess=True)


if __name__ == "__main__":
    model()
