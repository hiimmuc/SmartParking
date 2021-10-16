import random
import time

import cv2
import numpy as np
from LicenseOCR.ocr import *

modelConfiguration = r"backup\model\yolov4-tiny-custom.cfg"
modelWeights = r"backup\model\yolov4-tiny-custom_best.weights"
classesFile = r"backup\model\Number_plate.names"


class YOLO:
    def __init__(self, model_cfg=modelConfiguration, model_weight=modelWeights, name=classesFile):
        super().__init__()
        self.net = cv2.dnn.readNetFromDarknet(model_cfg, model_weight)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        self.name = name
        self.setup_param()

    def setup_param(self):
        self.char_list = '0123456789ABCDEFGHKLMNPRSTUVXYZ'
        self.whT = 320
        self.confThreshold = 0.4
        self.nmsThreshold = 0.6
        self.n_frame = []
        self.classNames = []
        with open(self.name, 'rt') as f:
            self.classNames = f.read().rstrip('n').split('\n')

    def findObjects(self, outputs, img, show=False):
        hT, wT, _ = img.shape
        bbox = []
        classIds = []
        confs = []

        for output in outputs:
            for det in output:
                scores = det[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self.confThreshold:
                    w, h = int(det[2] * wT), int(det[3] * hT)
                    x, y = int((det[0] * wT) - w / 2), int((det[1] * hT) - h / 2)
                    bbox.append([x, y, w, h])
                    classIds.append(classId)
                    confs.append(float(confidence))

        indices = cv2.dnn.NMSBoxes(bbox, confs, self.confThreshold, self.nmsThreshold)
        self.n_frame.append(indices)

        if show:
            for i in indices:
                i = i[0]
                box = bbox[i]
                x, y, w, h = box[0], box[1], box[2], box[3]

                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(img, f'{self.classNames[0].upper()} {int(confs[i] * 100)}%',
                            (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        img_crop = img[y:y+h, x:x+w]
        results = cv2.resize(img_crop, (hT, wT), interpolation=cv2.INTER_CUBIC)

        return results

    def yolo_LP(self, img):
        if isinstance(img, str):
            img = cv2.imread(img)

        blob = cv2.dnn.blobFromImage(img, 1 / 255., (self.whT, self.whT), [0, 0, 0], swapRB=True, crop=False)
        self.net.setInput(blob)

        layersNames = self.net.getLayerNames()
        outputNames = [(layersNames[i[0] - 1]) for i in self.net.getUnconnectedOutLayers()]
        outputs = self.net.forward(outputNames)
        img_crop = self.findObjects(outputs, img)

        return img_crop


if __name__ == '__main__':
    pass
