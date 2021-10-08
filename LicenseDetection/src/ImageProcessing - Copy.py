import cv2
import numpy as np
import imutils


minAR = 4
maxAR = 5

img_path = r"D:\Python\Pycharm\Number Plate Project\yolo_plate_dataset\xemayBIgPlate199.jpg"
img = cv2.imread(img_path)
cv2.imshow("img", img)
img = cv2.resize(img, (620,480))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to grey scale

rectKern = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
blackHat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKern)
squareKern = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
light = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, squareKern)
light = cv2.threshold(light, 0, 255,
                      cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
gradX = cv2.Sobel(blackHat, ddepth=cv2.CV_32F,
                  dx=1, dy=0, ksize=-1)
gradX = np.absolute(gradX)
(minVal, maxVal) = (np.min(gradX), np.max(gradX))
gradX = 255 * ((gradX - minVal) / (maxVal - minVal))
gradX = gradX.astype("uint8")

gradX = cv2.GaussianBlur(gradX, (5, 5), 0)
gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKern)
thresh = cv2.threshold(gradX, 0, 255,
                       cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
thresh = cv2.erode(thresh, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=5)

thresh = cv2.bitwise_and(thresh, thresh, mask=light)
thresh = cv2.dilate(thresh, None, iterations=2)
thresh = cv2.erode(thresh, None, iterations=1)
cv2.imshow("thresh", thresh)

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
print(len(cnts))

# initialize the license plate contour and ROI
lpCnt = None
roi = None
# loop over the license plate candidate contours
for c in cnts:
# compute the bounding box of the contour and then use
# the bounding box to derive the aspect ratio
    (x, y, w, h) = cv2.boundingRect(c)
    ar = w / float(h)
    # check to see if the aspect ratio is rectangular
    if ar >= minAR and ar <= maxAR:
        # store the license plate contour and extract the
        # license plate from the grayscale image and then
        # threshold it
        lpCnt = c
        licensePlate = gray[y:y + h, x:x + w]
        roi = cv2.threshold(licensePlate, 0, 255,
                            cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        # if clearBorder:
        #     roi = clear_border(roi)
        # display any debugging information and then break
        # from the loop early since we have found the license
        # plate region
        cv2.imshow("Image", licensePlate)
        cv2.imshow("ROI", roi)
        break
    # return a 2-tuple of the license plate ROI and the contour
    # associated with it


cv2.waitKey(0)
cv2.destroyAllWindows()
