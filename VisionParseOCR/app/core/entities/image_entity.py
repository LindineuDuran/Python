from app.infrastructure.logging.logger import get_logger
logger = get_logger(__name__)

class ImageEntity:
    def __init__(self, name, data, hash_id):
        self.name = name
        self.data = data
        self.hash_id = hash_id
        self.text = ""
        self.type = data.get("type", "")  # já aproveita o tipo do extractor

    def has_text(self):
        return bool(self.text.strip())

    def is_render(self):
        return self.data.get("type") == "render"
    
    @property
    def bytes(self):
        return self.data.get("bytes")