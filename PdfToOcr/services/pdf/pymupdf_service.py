import fitz
import os
from services.pdf.pdf_detector import PdfTypeDetector


class PDFService:
    def __init__(
        self,
        min_width=50,
        min_height=50,
        min_size_bytes=1024,
        render_scale=1 # Escala da imagem. Por exemplo, um valor de 0,5 realiza um encolhimento por um fator de 2.
    ):
        self.min_width = min_width
        self.min_height = min_height
        self.min_size_bytes = min_size_bytes
        self.render_scale = render_scale

    def extract_images(self, pdf_path):
        doc = fitz.open(pdf_path)

        # 🔍 Detecta tipo do PDF
        detector = PdfTypeDetector(doc)
        pdf_type, confidence = detector.detect()

        # print(f"🧠 Tipo do PDF: {pdf_type} (confiança: {confidence:.2f})")

        # 🔥 RESET CORRETO (ESSENCIAL)
        images = []
        xrefs_extraidos = set()

        total_paginas = len(doc)
        total_imagens_encontradas = 0

        # print(f"\n📄 Processando PDF: {pdf_path}")
        # print(f"📑 Total de páginas: {total_paginas}\n")

        for page_index in range(total_paginas):
            page = doc[page_index]

            # print(f"➡️ Página {page_index + 1}")

            # ======================================================
            # 🟢 MODO SCAN → RENDERIZA A PÁGINA INTEIRA
            # ======================================================
            if pdf_type == "SCAN":
                pix = page.get_pixmap(
                    matrix=fitz.Matrix(self.render_scale, self.render_scale)
                )

                img_bytes = pix.tobytes("png")

                images.append({
                    "type": "render",
                    "page": page_index,
                    "width": pix.width,
                    "height": pix.height,
                    "ext": "png",
                    "bytes": img_bytes
                })

                total_imagens_encontradas += 1

                # print(f"   ✅ Página renderizada {pix.width}x{pix.height}")

            # ======================================================
            # 🔵 MODO COMPOSED → EXTRAI IMAGENS INTERNAS
            # ======================================================
            else:
                image_list = page.get_images(full=True)

                print(f"   {len(image_list)} imagens encontradas")

                for img in image_list:
                    xref = img[0]

                    # 🚫 Evita duplicação global
                    if xref in xrefs_extraidos:
                        continue

                    base_image = doc.extract_image(xref)

                    width = base_image["width"]
                    height = base_image["height"]
                    img_bytes = base_image["image"]
                    ext = base_image["ext"]
                    size_bytes = len(img_bytes)

                    # 🔍 Filtros de qualidade
                    if width < self.min_width or height < self.min_height:
                        print(f"   ⚠️ Ignorada (muito pequena): {width}x{height}")
                        continue

                    if size_bytes < self.min_size_bytes:
                        print(f"   ⚠️ Ignorada (muito leve): {size_bytes} bytes")
                        continue

                    # ✅ Aceita imagem
                    xrefs_extraidos.add(xref)

                    images.append({
                        "type": "image",
                        "page": page_index,
                        "xref": xref,
                        "width": width,
                        "height": height,
                        "ext": ext,
                        "bytes": img_bytes
                    })

                    total_imagens_encontradas += 1

                    # print(f"   ✅ Imagem {total_imagens_encontradas} ({ext}) {width}x{height}")

        doc.close()

        # # ======================================================
        # # 📊 RESUMO FINAL
        # # ======================================================
        # print("\n📊 RESUMO FINAL")
        # print(f"📑 Páginas: {total_paginas}")
        # print(f"🖼️ Imagens únicas extraídas: {len(xrefs_extraidos)}")
        # print(f"📦 Total no array: {len(images)}\n")

        return images

    # ==========================================
    # 💾 EXPORTAÇÃO
    # ==========================================
    def save_images(self, images, output_dir="saida", prefix="img"):
        os.makedirs(output_dir, exist_ok=True)

        print(f"\n💾 Salvando imagens em: {output_dir}\n")

        for i, img in enumerate(images, start=1):
            nome = f"{prefix}_{i:03d}.{img.data['ext']}"
            caminho = os.path.join(output_dir, nome)

            with open(caminho, "wb") as f:
                f.write(img.data["bytes"])

            print(f"✅ Salvo: {caminho}")

        print("\n✔️ Exportação concluída\n")