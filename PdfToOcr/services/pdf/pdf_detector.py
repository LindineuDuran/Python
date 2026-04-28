import fitz
from collections import Counter

class PdfTypeDetector:
    def __init__(self, doc):
        self.doc = doc

    def detect(self):
        total_pages = len(self.doc)

        image_counts = []
        large_image_pages = 0
        text_lengths = []
        xrefs_all = []

        for page in self.doc:
            images = page.get_images(full=True)
            image_counts.append(len(images))

            text = page.get_text("text").strip()
            text_lengths.append(len(text))

            xrefs = [img[0] for img in images]
            xrefs_all.extend(xrefs)

            for img in images:
                base = self.doc.extract_image(img[0])
                img_area = base["width"] * base["height"]
                page_area = page.rect.width * page.rect.height

                if img_area / page_area > 0.7:
                    large_image_pages += 1
                    break

        avg_images = sum(image_counts) / total_pages
        avg_text = sum(text_lengths) / total_pages
        reused_images = sum(1 for c in Counter(xrefs_all).values() if c > 1)

        score_scan = 0
        score_composed = 0

        if avg_images <= 2:
            score_scan += 2
        else:
            score_composed += 2

        if large_image_pages / total_pages > 0.7:
            score_scan += 3
        else:
            score_composed += 1

        if avg_text < 50:
            score_scan += 2
        else:
            score_composed += 2

        if reused_images > 0:
            score_composed += 3

        result = "SCAN" if score_scan > score_composed else "COMPOSED"
        confidence = max(score_scan, score_composed) / (score_scan + score_composed)

        return result, confidence