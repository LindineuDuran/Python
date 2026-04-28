from pathlib import Path
import os
import sys


class PathManager:

    @staticmethod
    def is_frozen():
        return getattr(sys, "frozen", False)

    @staticmethod
    def base():
        # EXE PyInstaller
        if PathManager.is_frozen():
            return sys._MEIPASS

        # DEV = raiz do projeto
        return os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
        )

    # ------------------------
    # ICONES / IMAGENS
    # ------------------------
    @staticmethod
    def icons():
        if PathManager.is_frozen():
            return os.path.join(PathManager.base(), "icones")

        return os.path.join(PathManager.base(), "app", "icones")

    @staticmethod
    def icon(filename):
        return os.path.join(PathManager.icons(), filename)

    @staticmethod
    def splash():
        return PathManager.icon("visionparse_ocr.png")

    # ------------------------
    # TESSERACT
    # ------------------------
    @staticmethod
    def tesseract():
        return os.path.join(PathManager.base(), "Tesseract-OCR")

    @staticmethod
    def tesseract_exe():
        return os.path.join(PathManager.tesseract(), "tesseract.exe")

    @staticmethod
    def tessdata():
        return os.path.join(PathManager.tesseract(), "tessdata")

    # ------------------------
    # OUTPUT
    # ------------------------
    @staticmethod
    def output():
        docs = Path.home() / "Documents" / "VisionParseOCR" / "output"
        docs.mkdir(parents=True, exist_ok=True)
        return str(docs)