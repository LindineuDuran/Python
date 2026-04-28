
import pytesseract
from PIL import Image

class OCRService:
    def extract_text(self, image_path):
        return pytesseract.image_to_string(Image.open(image_path))
