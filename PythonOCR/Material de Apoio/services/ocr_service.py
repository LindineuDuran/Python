import pytesseract
import cv2
import numpy as np

class OCRService:

    def preprocess(self, image_path):
        img = cv2.imread(image_path)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # melhora contraste
        gray = cv2.GaussianBlur(gray, (5,5), 0)

        # binarização adaptativa
        thresh = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )

        return thresh

    def extract_text(self, image_path):
        processed = self.preprocess(image_path)
        return pytesseract.image_to_string(processed)

    def extract_from_region(self, image_path, rect):
        img = cv2.imread(image_path)

        x, y, w, h = rect
        roi = img[y:y+h, x:x+w]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

        return pytesseract.image_to_string(thresh)