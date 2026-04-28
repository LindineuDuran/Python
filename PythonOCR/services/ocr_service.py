import pytesseract
import cv2
import numpy as np

class OCRService:
    def read_image(self, path):
        with open(path, 'rb') as f:
            file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        return img
    
    def preprocess(self, path):
        img = self.read_image(path)

        if img is None:
            raise Exception(f"Erro ao carregar imagem: {path}")
    
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)

        thresh = cv2.adaptiveThreshold(
            blur, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        return thresh

    # def extract_text(self, path):
    #     img = self.preprocess(path)
    #     return pytesseract.image_to_string(img)

    def extract_text(self, path, rotation=0):
        img = self.read_image(path)

        if rotation == 90:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        elif rotation == 180:
            img = cv2.rotate(img, cv2.ROTATE_180)
        elif rotation == 270:
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        return pytesseract.image_to_string(gray)

    # def extract_region(self, path, rect):
    #     img = self.read_image(path)

    #     if img is None:
    #         raise Exception(f"Erro ao carregar imagem: {path}")

    #     x, y, w, h = rect

    #     # 🔥 CLAMP (evita sair da imagem)
    #     h_img, w_img = img.shape[:2]

    #     x = max(0, min(x, w_img - 1))
    #     y = max(0, min(y, h_img - 1))
    #     w = max(1, min(w, w_img - x))
    #     h = max(1, min(h, h_img - y))

    #     roi = img[y:y+h, x:x+w]

    #     # 🔥 PROTEÇÃO FINAL
    #     if roi is None or roi.size == 0:
    #         print("[WARN] ROI inválida:", rect)
    #         return ""

    #     gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    #     thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    #     return pytesseract.image_to_string(thresh)

    def extract_region(self, path, rect, rotation=0):
        img = self.read_image(path)

        if img is None:
            raise Exception(f"Erro ao carregar imagem: {path}")

        # aplica rotação primeiro
        if rotation == 90:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        elif rotation == 180:
            img = cv2.rotate(img, cv2.ROTATE_180)
        elif rotation == 270:
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

        x, y, w, h = rect

        # 🔥 CLAMP (evita sair da imagem)
        h_img, w_img = img.shape[:2]

        x = max(0, min(x, w_img - 1))
        y = max(0, min(y, h_img - 1))
        w = max(1, min(w, w_img - x))
        h = max(1, min(h, h_img - y))

        roi = img[y:y+h, x:x+w]

        # 🔥 PROTEÇÃO FINAL
        if roi is None or roi.size == 0:
            print("[WARN] ROI inválida:", rect)
            return ""

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

        return pytesseract.image_to_string(thresh)