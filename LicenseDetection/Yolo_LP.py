import cv2
import numpy as np
import time
import pytesseract
from ocr import *
import random

modelConfiguration = r"yolov4-tiny-custom.cfg"
modelWeights = "yolov4-tiny-custom_best.weights"
classesFile = r"Number_plate.names"

class YOLO:
    def __init__(self, model_cfg = modelConfiguration, model_weight = modelWeights, name = classesFile):
        super().__init__()
        self.net = cv2.dnn.readNetFromDarknet(model_cfg, model_weight)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        self.name = name
        self.setup_param()

    def setup_param(self):
        self.char_list = '0123456789ABCDEFGHKLMNPRSTUVXYZ'
        self.whT = 320
        self.confThreshold = 0.8
        self.nmsThreshold = 0.1
        self.Number_of_frame = []
        self.classNames = []
        with open(self.name, 'rt') as f:
            self.classNames = f.read().rstrip('n').split('\n')

    def findObjects(self, outputs, img):
        hT, wT, cT = img.shape
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
        self.Number_of_frame.append(indices)
        # print(len(Number_of_frame), len(indices))
        for i in indices:
            i = i[0]
            box = bbox[i]
            x, y, w, h = box[0], box[1], box[2], box[3]

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img, f'{self.classNames[0].upper()} {int(confs[i] * 100)}%',
                        (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        img2 = img[y:y+h, x:x+w]
        return img2

    def yolo_LP(self, img_path):
        img = cv2.imread(img_path)
        blob = cv2.dnn.blobFromImage(img, 1 / 255, (self.whT, self.whT), [0, 0, 0], 1, crop=False)
        self.net.setInput(blob)
        layersNames = self.net.getLayerNames()
        outputNames = [(layersNames[i[0] - 1]) for i in self.net.getUnconnectedOutLayers()]
        outputs = self.net.forward(outputNames)
        img_crop = self.findObjects(outputs, img)

        return  img_crop

if __name__ == '__main__':
    # Choose random motorbike image from the dataset
    num = random.randint(0, 2489)
    image_name = "xemay" + str(num) + ".jpg"
    img_path = r"D:\Python\Pycharm\Number Plate Project\yolo_plate_dataset\\" + image_name

    # Yolo
    t0 = time.time()
    Yolo_engine = YOLO()
    print("Load model time:", time.time() - t0)
    t1 = time.time()
    LP = Yolo_engine.yolo_LP(img_path)
    print("Detect time:", time.time() - t1)
    cv2.imshow("License Plate", LP)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
