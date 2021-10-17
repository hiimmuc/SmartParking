import time

import matplotlib.pyplot as plt

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

    def extract_info(self, image, only_ocr=False, show=True, preprocess=False):
        if isinstance(image, str):
            print(image)
            image = cv2.imread(image)
        if not only_ocr:
            t2 = time.time()
            plates = self.yolo_engine.detect(image, show=False, crop_scale=0.025)
            print("Detect time:", time.time() - t2)

            _, axarr = plt.subplots(1, 2)

            for plate in plates:
                axarr[0].imshow(plate)

                if preprocess:
                    plate = preprocess_image(plate, pad=False)
                    axarr[1].imshow(plate, cmap='gray')

                # ocr
                t3 = time.time()
                text, conf = self.ocr_engine.read(image, 'cv2', return_confidence=True)
                print(text, conf, time.time() - t3)
            if show:
                plt.show()

        else:
            t3 = time.time()
            text, conf = self.ocr_engine.read(image, 'cv2', return_confidence=True)
            print(text, conf, time.time() - t3)
        # TODO: return plates, text based on confidence of text

    def video_detect(self, video_path, show=True, preprocess=False):
        pass
