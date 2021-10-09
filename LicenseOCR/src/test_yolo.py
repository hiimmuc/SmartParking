import argparse
import os.path
import sys

import cv2 as cv

from yolo import Yolo

classes_filename = r'LicenseOCR\src\config\classes.names',
model_architecture_filename = r"LicenseOCR\src\config\yolov3_license_plates.cfg",
model_weights_filename = r"LicenseOCR\src\config\yolov3_license_plates_last.weights",
output_directory = r'debug'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Testing YOLO...')
    parser.add_argument('--image', help='Path to image file.', default=0)
    args = parser.parse_args()

    yolo = Yolo(img_width=1056, img_height=576,
                confidence_threshold=0.6, non_max_supress_theshold=0.4,
                classes_filename=classes_filename,
                model_architecture_filename=model_architecture_filename,
                model_weights_filename=model_weights_filename,
                output_directory=output_directory)

    # Open the image file
    if not os.path.isfile(args.image):
        print("Input image file ", args.image, " doesn't exist")
        sys.exit(1)
    cap = cv.VideoCapture(args.image)

    # get frame
    hasFrame, frame = cap.read()

    if hasFrame:
        yolo.detect(frame)
    else:
        print("Frame not found!")
