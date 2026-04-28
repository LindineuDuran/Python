
from concurrent.futures import ThreadPoolExecutor
from app.infrastructure.worker import Worker

class AppController:

    def __init__(self, frame, services):
        self.frame = frame
        self.services = services

    def process_pdf(self, pdf_path):

        def task():
            images = self.services["pdf"].extract_images(pdf_path)
            total = len(images)
            results = []

            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = []
                for img_data in images:
                    futures.append(executor.submit(self.process_single, img_data))

                for i, future in enumerate(futures):
                    result = future.result()
                    if result:
                        results.append(result)
                        self.frame.show_preview(result["path"])

                    yield int((i + 1) / total * 100)

            self.services["export"].export_txt(results, "output/result.txt")

        Worker(task, self.frame.update_progress, self.frame.on_complete).start()

    def process_single(self, img_data):
        cache = self.services["cache"]

        if cache.exists(img_data["hash"]):
            return None

        text = self.services["ocr"].extract_text(img_data["path"])
        classification = self.services["classifier"].classify(img_data["path"])

        cache.save(img_data["hash"], text)

        return {
            "name": img_data["name"],
            "text": text,
            "type": classification,
            "path": img_data["path"]
        }
