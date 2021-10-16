import random
import sys
import time
import typing

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets

from GUI.gui_utils import *
from LicenseDetection.Yolo_LP import *
from LicenseOCR.ocr import *


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
    img_path = os.path.join(r"backup\Number Plate Dataset\yolo_plate_dataset", image_name)

    # Yolo
    t0 = time.time()
    Yolo_engine = YOLO()
    print("Load model time:", time.time() - t0)
    # OCR
    t1 = time.time()
    ocr = OCR_engine()
    print("Load OCR model time:", time.time() - t1)
    # detect
    t2 = time.time()
    LP = Yolo_engine.yolo_LP(img_path)
    print("Detect time:", time.time() - t2)
    plt.imshow(LP)
    # ocr
    t3 = time.time()
    print(ocr.read(LP, 'cv2', return_confidence=True), "\nPredict time:", time.time() - t3)
    plt.show()


if __name__ == "__main__":
    model()
