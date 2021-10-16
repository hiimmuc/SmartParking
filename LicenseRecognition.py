import sys
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from LicenseDetection.Yolo_LP import *
from LicenseOCR.ocr import *
from LicenseOCR.ocr_utils import *


class LicenseRecognizer:
    def __init__(self):
        super().__init__()
        t0 = time.time()
        self.yolo_engine = YOLO()
        print("Load model time:", time.time() - t0)
        t1 = time.time()
        self.ocr_engine = OCR()
        print("Load OCR model time:", time.time() - t1)

    def extract_info(self, image, show=True, preprocess=False):
        if isinstance(image, str):
            image = cv2.imread(image)
        t2 = time.time()
        plates = self.yolo_engine.detect(image, show=True, crop_scale=0.12)
        print("Detect time:", time.time() - t2)

        f, axarr = plt.subplots(1, 2)

        for plate in plates:
            axarr[0].imshow(plate)

            if preprocess:
                plate = preprocess_image(plate)
                axarr[1].imshow(plate)
            # ocr
            t3 = time.time()
            print(self.ocr_engine.read(plate, 'cv2', return_confidence=True), "\nPredict time:", time.time() - t3)
        if show:
            plt.show()

    def video_detect(self, video_path, show=True, preprocess=False):
        pass
