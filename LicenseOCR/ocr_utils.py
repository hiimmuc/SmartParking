import cv2
import numpy as np

# get grayscale image


def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal


def remove_noise(image):
    return cv2.medianBlur(image, 3)

# thresholding


def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# dilation


def dilate(image):
    kernel = np.ones((3, 3), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)

# erosion


def erode(image):
    kernel = np.ones((3, 3), np.uint8)
    return cv2.erode(image, kernel, iterations=1)

# opening - erosion followed by dilation


def opening(image):
    kernel = np.ones((3, 3), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

# canny edge detection


def canny(image):
    return cv2.Canny(image, 100, 200)

# skew correction


def deskew(image):

    gray = get_grayscale(image)

    gray = cv2.bitwise_not(gray)

    _, thresh = cv2.threshold(gray, 120, 255,
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -15:
        angle = -(90 + angle)
    else:
        angle = 0
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

# template matching


def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)


def padding(image):
    # Padding
    image_bw = cv2.bitwise_not(image)
    h, w = image_bw.shape
    pad_size = int(abs(h - w) / 2)
    pad_extra = abs(h - w) % 2
    image_padding = np.array([])
    if h > w:
        image_padding = cv2.copyMakeBorder(image_bw,
                                           0,
                                           0,
                                           pad_size + pad_extra,
                                           pad_size,
                                           cv2.BORDER_CONSTANT,
                                           value=[0, 0, 0])
        image_padding = cv2.copyMakeBorder(image_padding,
                                           5,
                                           5,
                                           5,
                                           5,
                                           cv2.BORDER_CONSTANT,
                                           value=[0, 0, 0])
    elif w > h:
        image_padding = cv2.copyMakeBorder(image_bw,
                                           pad_size + pad_extra,
                                           pad_size,
                                           0,
                                           0,
                                           cv2.BORDER_CONSTANT,
                                           value=[0, 0, 0])
        image_padding = cv2.copyMakeBorder(image_padding,
                                           5,
                                           5,
                                           5,
                                           5,
                                           cv2.BORDER_CONSTANT,
                                           value=[0, 0, 0])
    else:
        image_padding = image_bw

    return image_padding


def super_resolution(model_name, zoom, image):
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    path = f"{model_name}_x{zoom}.pb"
    sr.readModel(path)
    sr.setModel(model_name, zoom)
    result = sr.upsample(image)
    return result


def preprocess_image(image, pad=True):

    deskew_img = deskew(image)

    gray = get_grayscale(deskew_img)
    gray = remove_noise(gray)
    thresh = thresholding(gray)

    if pad:
        image = padding(thresh)
    else:
        image = thresh
    image = opening(image)

    rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    # rgb = super_resolution("ESPCN", 2, rgb)
    return rgb
