import time

import cv2
import easyocr
import numpy as np
from PIL import Image


class OCR_engine():
    def __init__(self):
        self.engine = easyocr.Reader(['en', 'vi'])

    def read(self, image, method='cv2', return_confidence=False):
        if isinstance(image, str):
            if method == 'cv2':
                image = cv2.imread(image)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            elif method == 'PIL':
                image = Image.open(image)

        results = self.engine.readtext(image)  # bbox, text, prob
        text_str = ''
        confidence = np.mean([result[2] for result in results])
        # confidence = [result[2] for result in results]

        for i, res in enumerate(results):
            text_str += (' ' + res[1])

        return text_str if not return_confidence else (text_str, confidence)


if __name__ == '__main__':
    path = r'LicenseOCR\test image\bien-so-xe-may.jpg'

    t0 = time.time()
    engine = OCR_engine()
    print('Initialize model time:', time.time() - t0)

    t = time.time()
    print(engine.read(path, 'cv2', return_confidence=True), "\nPredict time:", time.time() - t)
