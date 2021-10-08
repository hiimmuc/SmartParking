import time

import cv2
import easyocr


class OCR_engine():
    def __init__(self):
        self.engine = easyocr.Reader(['en', 'vi'])

    def read(self, image):
        if isinstance(image, str):
            image = cv2.imread(image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = self.engine.readtext(image)  # bbox, text, prob
        text_str = ''

        for i, res in enumerate(results):
            text_str += (' ' + res[1])

        return text_str


if __name__ == '__main__':
    path = r'LicenseOCR\test image\xem-tra-bien-so-xe-e1563508757390.jpg'
    engine = OCR_engine()
    print(engine.read(path))
