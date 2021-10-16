import cv2
import numpy as np
from imutils.video import FPS
from PyQt5.QtCore import QThread, pyqtSignal
from LicenseDetection import *


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray, list)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        # load our serialized face detector model from disk
        prototxtPath = r"backups\deploy.prototxt"
        weightsPath = r"backups\res10_300x300_ssd_iter_140000.caffemodel"
        # load the face mask detector model from disk
        model_path = r"backups\mask_detector.h5"
        self.model = FaceNet(prototxt_path=prototxtPath, weights_path=weightsPath, model_path=model_path)
        self.model.creat_net()

    def run(self):
        # capture from web cam
        print("[INFO] Start recording...")
        cap = cv2.VideoCapture(0)
        # stream = VideoStream().start()
        self.fps = FPS().start()
        while self._run_flag:
            ret, frame = cap.read()
            if ret:
                output_img, self.value = self.model.detector(frame)
                self.change_pixmap_signal.emit(output_img, self.value)
                self.fps.update()
        self.fps.stop()
        print("[INFO] elasped time: {:.2f}".format(self.fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(self.fps.fps()))

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
