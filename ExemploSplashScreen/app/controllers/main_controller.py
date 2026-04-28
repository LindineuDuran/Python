
from infrastructure.pdf.pymupdf_extractor import PDFExtractor
from infrastructure.ocr.tesseract_engine import TesseractEngine
from core.usecases.process_pipeline import ProcessPipeline
from core.entities.image_entity import ImageEntity
from utils.hash_utils import generate_hash

class MainController:

    def __init__(self):
        self.extractor = PDFExtractor()
        self.ocr = TesseractEngine()
        self.pipeline = ProcessPipeline(self.ocr)

    def load_pdf(self, path):
        images = self.extractor.extract_images(path)
        entities = []

        for i, img in enumerate(images):
            hash_id = generate_hash(img)
            entities.append(ImageEntity(f"img_{i}", img, hash_id))

        return entities

    def process_image(self, image):
        return self.pipeline.process(image)
