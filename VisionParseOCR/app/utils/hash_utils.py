from app.infrastructure.logging.logger import get_logger
logger = get_logger(__name__)

import hashlib

def generate_hash(data):
    return hashlib.md5(data).hexdigest()