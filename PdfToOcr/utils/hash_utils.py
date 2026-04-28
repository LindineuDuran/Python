import hashlib

def generate_hash(data):
    return hashlib.md5(data).hexdigest()