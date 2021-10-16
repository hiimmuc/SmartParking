import cv2
import numpy as np
from imutils.video import FPS
from LicenseDetection import *
from PyQt5.QtCore import QThread, pyqtSignal


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray, list)

    def __init__(self, source=0, detection_model=None):
        super().__init__()
        self.run_flag = True
        self.source = source

        # initmodel here
        self.model = detection_model

    def run(self):
        # capture from web cam
        bbox = []
        print("[INFO] Start recording...")
        cap = cv2.VideoCapture(self.source)
        self.fps = FPS().start()

        while self.run_flag:
            ret, frame = cap.read()
            if ret:
                if self.model is not None:
                    # detect license plate
                    bbox, frame = self.model.detect_license_plate(frame)

                self.change_pixmap_signal.emit(frame, bbox)

                self.fps.update()
        self.fps.stop()

        try:
            print("[INFO] elasped time: {:.2f}".format(self.fps.elapsed()))
            print("[INFO] approx. FPS: {:.2f}".format(self.fps.fps()))
        except ZeroDivisionError:
            pass

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self.run_flag = False
        self.wait()
