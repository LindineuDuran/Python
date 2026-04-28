
import fitz, os, hashlib

class PDFService:

    def extract_images(self, pdf_path):
        doc = fitz.open(pdf_path)
        os.makedirs("output/images", exist_ok=True)
        images = []

        count = 0
        for page_index in range(len(doc)):
            for img_index, img in enumerate(doc[page_index].get_images(full=True)):
                xref = img[0]
                base = doc.extract_image(xref)
                img_bytes = base["image"]
                ext = base["ext"]

                name = f"img_{count:03}"
                path = f"output/images/{name}.{ext}"

                with open(path, "wb") as f:
                    f.write(img_bytes)

                hash_md5 = hashlib.md5(img_bytes).hexdigest()

                images.append({
                    "name": name,
                    "path": path,
                    "hash": hash_md5
                })

                count += 1

        return images
