
import os

class ExportService:
    def export_txt(self, data, path):
        os.makedirs("output", exist_ok=True)
        with open(path,"w",encoding="utf-8") as f:
            for d in data:
                f.write(f"{d['name']} ({d['type']})\n{d['text']}\n\n")
