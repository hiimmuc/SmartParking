import time

import matplotlib.pyplot as plt

from LicenseDetection.Yolo_LP import *
from LicenseOCR.ocr import *
from LicenseOCR.ocr_utils import *


def remove_noiss_characters(text):
    noise = ['.', "'", '"', ";", ":", ",", "!", "?", "*", "&", "^", "%", "$", "#", "@", "~", "`", "|", "\\", "/", "(", ")", "{", "}", "[", "]"]
    for char in text:
        if char in noise:
            text = text.replace(char, "")
    return text


class LicenseRecognizer:
    def __init__(self):
        super().__init__()
        t0 = time.time()
        self.yolo_engine = YOLO()
        print("Load model time:", time.time() - t0)
        t1 = time.time()
        self.ocr_engine = OCR()
        print("Load OCR model time:", time.time() - t1)

    def extract_info(self, image, detection=True, ocr=True, show=True, preprocess=False):
        if isinstance(image, str):
            image = cv2.cvtColor(cv2.imread(image), cv2.COLOR_BGR2RGB)

        read_img = image.copy()
        text = ''
        conf = 0
        plates = None

        if detection:
            t2 = time.time()
            plates, _ = self.yolo_engine.detect(image, show=False, crop_scale=0.05)
            print("Detect time:", time.time() - t2)

            assert len(plates) == 1, "More than one license plate detected!"
            read_img = plates[0]

        _, axarr = plt.subplots(1, 2)
        axarr[0].imshow(read_img)

        if ocr:
            if preprocess:
                read_img = preprocess_image(read_img, pad=False)
                axarr[1].imshow(read_img)

            # ocr
            t3 = time.time()
            text, conf = self.ocr_engine.read(read_img, 'cv2', return_confidence=True)
            text = remove_noiss_characters(text)
            print(text, conf, time.time() - t3, 's')

        if show:
            plt.show()

        return read_img, text, conf

    def video_detect(self, video_path, show=True, preprocess=False):
        pass
