import time

import cv2
import easyocr
import numpy as np
from PIL import Image

#     'decoder' = 'greedy'  # options are 'greedy', 'beamsearch' and 'wordbeamsearch'.
#     'beamWidth' = 5  # How many beam to keep when decoder = 'beamsearch' or 'wordbeamsearch'
#     'batch_size' = 1  # batch_size > 1 will make EasyOCR faster but use more memory
#    'workers' = 0  # Number thread used in of dataloader
#     'allowlist' = "license plate"  # - Force EasyOCR to recognize only subset of characters. Useful for specific problem (E.g. license plate, etc.)
#     'blocklist' = None  # - Block subset of character. This argument will be ignored if allowlist is given.
#     'detail' = 1  # - Set this to 0 for simple output
#     'paragraph' = False  # - Combine result into paragraph
#     'min_size' = 10  # - Filter text box smaller than minimum value in pixel
#     # - Allow EasyOCR to rotate each text box and return the one with the best confident score. Eligible values are 90, 180 and 270. For example, try [90, 180 ,270] for all possible text orientations.
#     'rotation_info' = None
#     # Parameters 2: Contrast
#     'contrast_ths' = 1  # Text box with contrast lower than this value will be passed into model 2 times. First is with original image and second with contrast adjusted to 'adjust_contrast' value. The one with more confident level will be returned as a result.
#     'adjust_contrast' = 0.5  # target contrast level for low contrast text box
#     # Parameters 3: Text Detection (from CRAFT)
#     'text_threshold' = 0.7  # Text confidence threshold
#     'low_text' = 0.4  # Text low-bound score
#     'link_threshold' = 0.4  # Link confidence threshold
#     'canvas_size' = 2560  # Maximum image size. Image bigger than this value will be resized down.
#     'mag_ratio' = 1  # Image magnification ratio
#     # Parameters 4: Bounding Box Merging
#     # This set of parameter controls when adjacent bounding boxes merge with each other. Every parameters except 'slope_ths' is in the unit of box height.

#     'slope_ths' = 0.1  # Maximum slope (delta y/delta x) to considered merging. Low value means tiled boxes will not be merged.
#     'ycenter_ths' = 0.5  # Maximum shift in y direction. Boxes with different level should not be merged.
#     'height_ths' = 0.5  # Maximum different in box height. Boxes with very different text size should not be merged.
#     'width_ths' = 0.5  # Maximum horizontal distance to merge boxes.
#     # ocr_parameter
#     'add_margin' = 0.1  # Extend bounding boxes in all direction by certain value. This is important for language with complex script (E.g. Thai).
#     'x_ths' = 1.0  # Maximum horizontal distance to merge text boxes when paragraph=True.
#     'y_ths' = 0.5  # Maximum verticall distance to merge text boxes when paragraph=True.

CONFIG = {
    'decoder': 'wordbeamsearch',
    'beamWidth': 5,
    'batch_size': 1,
    'workers': 0,
    'allowlist': None,
    'blocklist': None,
    'detail': 1,
    'paragraph': False,
    'min_size': 10,
    'rotation_info': None,
    'contrast_ths': 1,
    'adjust_contrast': 0.5,
    'text_threshold': 0.7,
    'low_text': 0.4,
    'link_threshold': 0.4,
    'canvas_size': 2560,
    'mag_ratio': 1,
    'slope_ths': 0.1,
    'ycenter_ths': 0.5,
    'height_ths': 0.5,
    'add_margin': 0.1,
    'x_ths': 1.0,
    'y_ths': 0.5,
}


class OCR():
    def __init__(self, gpu=False):
        self.engine = easyocr.Reader(['en', 'vi'], gpu=gpu)

    def read(self, image, method='cv2', return_confidence=False):
        if isinstance(image, str):
            if method == 'cv2':
                image = cv2.imread(image)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            elif method == 'PIL':
                image = Image.open(image)

        results = self.engine.readtext(image, **CONFIG)  # bbox, text, prob
        text_str = ''
        confidence = np.mean([result[2] for result in results])
        # confidence = [result[2] for result in results]

        for i, res in enumerate(results):
            text_str += (' ' + res[1])

        plate_id = text_str.strip().replace('.', '-')
        return plate_id if not return_confidence else (plate_id, confidence)


if __name__ == '__main__':
    path = r'LicenseOCR\test image\bien-so-xe-4-so-xau.jpg'

    img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
    assert isinstance(img, np.ndarray)

    t0 = time.time()
    engine = OCR()
    print('Initialize model time:', time.time() - t0)

    t = time.time()
    print(engine.read(img, 'cv2', return_confidence=True), "\nPredict time:", time.time() - t)
