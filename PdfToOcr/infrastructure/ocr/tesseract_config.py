import os
import pytesseract
#from utils.path_utils import get_base_path


class TesseractConfig:
    _configured = False

    @classmethod
    def setup(cls, app_path):
        if cls._configured:
            return

        
        tesseract_cmd = os.path.normpath(os.path.join(app_path,  "Tesseract-OCR", "tesseract.exe"))
        tessdata_dir = os.path.normpath(os.path.join(app_path, "Tesseract-OCR", "tessdata"))

        # 🔥 CORREÇÃO CRÍTICA
        tessdata_dir = tessdata_dir + os.sep   # ← adiciona barra final

        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

        # 🔥 SOLUÇÃO CRÍTICA
        os.environ["TESSDATA_PREFIX"] = tessdata_dir

        # print("TESSDATA_PREFIX:", os.environ["TESSDATA_PREFIX"])
        # print("EXISTS:", os.path.exists(os.environ["TESSDATA_PREFIX"]))
        # print("FILES:", os.listdir(os.environ["TESSDATA_PREFIX"]))

        cls.config = ""
        cls._configured = True

    @classmethod
    def get_config(cls, app_path, extra=""):
        cls.setup(app_path)
        return f"{cls.config} {extra}".strip()