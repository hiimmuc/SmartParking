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

    def findObjects(self, outputs, img, show=False, scale=True, crop_scale=0.1):
        hT, wT, _ = img.shape

        results = []
        bboxes = []
        classIds = []
        confs = []

        for output in outputs:
            for det in output:
                scores = det[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self.confThreshold:
                    center_x, center_y, width, height = list(map(int, det[0:4] * np.array([wT, hT, wT, hT])))
                    top_left_x = int(center_x - (width / 2))
                    top_left_y = int(center_y - (height / 2))

                    bboxes.append([top_left_x, top_left_y, width, height])
                    classIds.append(classId)
                    confs.append(float(confidence))

        indices = cv2.dnn.NMSBoxes(bboxes, confs, self.confThreshold, self.nmsThreshold)
        self.n_frame.append(indices)

        if scale:
            expand_bboxes = []
            for i in indices.flatten():
                x, y, w, h = bboxes[i]
                x = abs(int(x - crop_scale * w))
                y = abs(int(y - crop_scale * h))
                w = abs(int((1 + 2 * crop_scale) * w))
                h = abs(int((1 + 2 * crop_scale) * h))

                expand_bboxes.append([x, y, w, h])
            bboxes = expand_bboxes

        if show:
            for i in indices.flatten():
                x, y, w, h = expand_bboxes[i]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(img, f'{self.classNames[0].upper()} {int(confs[i] * 100)}%',
                            (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        for box in bboxes:
            x, y, w, h = box
            results.append(img[y:y+h, x:x+w])

        scale = max([max(hT//results[i].shape[0], wT//results[i].shape[1]) for i in range(len(results))])

        results = [cv2.resize(img_crop, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC) for img_crop in results]

        return results

    def detect(self, img, show=False, scale=True, crop_scale=0.1):
        if isinstance(img, str):
            img = cv2.imread(img)

        blob = cv2.dnn.blobFromImage(img, 1 / 255., (self.whT, self.whT), [0, 0, 0], swapRB=True, crop=False)
        self.net.setInput(blob)

        layersNames = self.net.getLayerNames()
        outputNames = [(layersNames[i[0] - 1]) for i in self.net.getUnconnectedOutLayers()]
        outputs = self.net.forward(outputNames)
        img_crop = self.findObjects(outputs, img, show=show, scale=scale, crop_scale=crop_scale)

        return img_crop


if __name__ == '__main__':
    pass
