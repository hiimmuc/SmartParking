import pytesseract as ocr
from PIL import Image

path = r"LicenseOCR\test image\bien-so-xe-may.jpg"
custom_config = r"--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIKLMNOPQRSTUVWXYZ"
image = Image.open(path)
ocr.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
results = ocr.image_to_boxes(image, config=custom_config)
print(results)
