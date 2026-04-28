from app.infrastructure.logging.logger import get_logger
logger = get_logger(__name__)
import os
import pytesseract

from app.utils.path_manager import PathManager

class TesseractConfig:
    _configured = False
    base_path = None

    @classmethod
    def setup(cls):
        if cls._configured:
            return

        # 🔥 CORREÇÃO CRÍTICA
        pytesseract.pytesseract.tesseract_cmd = PathManager.tesseract_exe()

        # 🔥 SOLUÇÃO CRÍTICA
        os.environ["TESSDATA_PREFIX"] = (PathManager.tessdata() + os.sep)

        logger.debug("TESSDATA_PREFIX: %s", os.environ["TESSDATA_PREFIX"])
        logger.debug("EXISTS: %s", os.path.exists(os.environ["TESSDATA_PREFIX"]))
        logger.debug("FILES: %s", os.listdir(os.environ["TESSDATA_PREFIX"]))

        cls._configured = True

    @classmethod
    def get_config(cls, extra=""):
        cls.setup()
        return extra.strip()