import cv2
import numpy as np

try:
    from LicenseDetection.wpod_utils import detect_lp, im2single, load_model
except:
    from wpod_utils import detect_lp, im2single, load_model

wpod_net_path = r"backup\Number Plate Dataset\wpod-net_update1.json"


class WPOD:
    def __init__(self, model_path=wpod_net_path) -> None:
        super().__init__()
        self.model = load_model(model_path)
        self.setup_params()

    def setup_params(self):
        self.Dmax = 608
        self.Dmin = 288

    def detect(self, image, threshold=0.5, show=False):
        if isinstance(image, str):
            image = cv2.imread(image)

        ratio = float(max(image.shape[:2])) / min(image.shape[:2])
        side = int(ratio * self.Dmin)
        bound_dim = min(side, self.Dmax)

        _, lp_image, lp_type = detect_lp(self.model, im2single(image), bound_dim, lp_threshold=threshold)

        if len(lp_image) > 0:
            lp_image[0] = cv2.convertScaleAbs(lp_image[0], alpha=(255.0))

            gray = cv2.cvtColor(lp_image[0], cv2.COLOR_BGR2GRAY)

            binary = cv2.threshold(gray, 170, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)[1]
            binary = cv2.dilate(binary, (3, 3), iterations=5)
            binary = cv2.erode(binary, (3, 3), iterations=2)

            if show:
                cv2.imshow("Gray image", gray)
                cv2.imshow("Anh bien so sau threshold", binary)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            return lp_image, lp_type
        else:
            return None, None


if __name__ == '__main__':
    import time

    t0 = time.time()
    wpod_engine = WPOD()
    print("Load model time:", time.time() - t0)

    img_path = r"LicenseDetection\test_img\Shear 1.jpg"
    t1 = time.time()
    wpod_engine.detect(img_path, show=True)
    print("Detect time:", time.time() - t1)
