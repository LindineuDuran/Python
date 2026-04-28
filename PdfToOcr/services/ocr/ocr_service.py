import pytesseract
from PIL import Image
from infrastructure.ocr.tesseract_config import TesseractConfig

class OCRService:
    def __init__(self, app_path):
        self.app_path = app_path

    def extract_text(self, wx_image, rotation=0):
        try:
            pil_img = self.wx_to_pil(wx_image)  

            # 🔥 aplica rotação (importante!)
            if rotation == 90:
                pil_img = pil_img.rotate(-90, expand=True)
            elif rotation == 270:
                pil_img = pil_img.rotate(90, expand=True)
            elif rotation == 180:
                pil_img = pil_img.rotate(180, expand=True)

            # 🔥 melhora OCR (grayscale)
            pil_img = pil_img.convert("L")

            # binarização 
            pil_img = pil_img.point(lambda x: 0 if x < 140 else 255, '1')

            config = TesseractConfig.get_config(self.app_path, "--oem 3 --psm 11 -l por+eng")

            return pytesseract.image_to_string(pil_img, config=config)

        except Exception as e:
            return f"OCR error: {e}"

    def wx_to_pil(self, wx_image):
        width = wx_image.GetWidth()
        height = wx_image.GetHeight()
        data = wx_image.GetData()

        return Image.frombytes("RGB", (width, height), data)

    def get_psm(self, w, h):
        area = w * h
        
        if area < 5000:
            return 8   # palavra
        elif area < 20000:
            return 7   # linha
        else:
            return 11  # bloco livre
    
    def extract_region(self, wx_image, rect, rotation=0):
        try:
            pil_img = self.wx_to_pil(wx_image)

            # 🔥 rotação
            if rotation == 90:
                pil_img = pil_img.rotate(-90, expand=True)
            elif rotation == 270:
                pil_img = pil_img.rotate(90, expand=True)
            elif rotation == 180:
                pil_img = pil_img.rotate(180, expand=True)

            x, y, w, h = rect

            w_img, h_img = pil_img.size  # PIL usa (width, height)
            
            # 🔥 clamp
            x = max(0, min(x, w_img - 1))
            y = max(0, min(y, h_img - 1))
            w = max(1, min(w, w_img - x))
            h = max(1, min(h, h_img - y))

            # 🔥 CORREÇÃO PRINCIPAL
            roi = pil_img.crop((x, y, x + w, y + h))

            # 🔥 validação
            if roi is None or roi.size[0] == 0 or roi.size[1] == 0:
                print("[WARN] ROI inválida:", rect)
                return ""

            # 🔥 pré-processamento
            roi = roi.convert("L")
            roi = roi.point(lambda px: 0 if px < 140 else 255, '1')

            psm = self.get_psm(w, h)

            config = TesseractConfig.get_config(self.app_path, "--oem 3 --psm 11 -l por+eng")

            return pytesseract.image_to_string(roi, config=config)

        except Exception as e:
            return f"OCR error: {e}"