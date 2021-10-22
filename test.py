import random
import sys
import time
import typing

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from LicenseDetection import Yolo_LP
from LicenseRecognition import *


def model():
    # Choose random motorbike image from the dataset
    img_path = r"LicenseOCR\test image\bien-so-xe-4-so-xau.jpg"

    recognizer = LicenseRecognizer()

    recognizer.extract_info(img_path,
                            detection=True,
                            ocr=True,
                            preprocess=True,
                            show=True)

    recognizer.extract_info(img_path,
                            detection=False,
                            ocr=True,
                            preprocess=True,
                            show=True)

    recognizer.extract_info(img_path,
                            detection=False,
                            ocr=True,
                            preprocess=False,
                            show=True)

    recognizer.extract_info(img_path,
                            detection=True,
                            ocr=False,
                            preprocess=True,
                            show=True)


if __name__ == "__main__":
    model()
    pass
