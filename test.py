from LicenseRecognition import *


def model():
    # Choose random motorbike image from the dataset
    recognizer = LicenseRecognizer()

    recognizer.video_detect()

    # recognizer.extract_info(img_path,
    #                         detection=True,
    #                         ocr=True,
    #                         preprocess=True,
    #                         show=True)

    # recognizer.extract_info(img_path,
    #                         detection=False,
    #                         ocr=True,
    #                         preprocess=True,
    #                         show=True)

    # recognizer.extract_info(img_path,
    #                         detection=False,
    #                         ocr=True,
    #                         preprocess=False,
    #                         show=True)

    # recognizer.extract_info(img_path,
    #                         detection=True,
    #                         ocr=False,
    #                         preprocess=True,
    #                         show=True)


if __name__ == "__main__":
    model()
    pass
