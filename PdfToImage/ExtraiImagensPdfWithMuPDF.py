import fitz  # PyMuPDF
import os


def extrair_imagens_pdf(
    caminho_pdf,
    pasta_saida="imagens_extraidas",
    prefixo="figura",
    formato_preferido=None  # "png" ou "jpg" ou None (original)
):
    os.makedirs(pasta_saida, exist_ok=True)

    doc = fitz.open(caminho_pdf)
    contador = 0

    for num_pagina in range(len(doc)):
        pagina = doc[num_pagina]
        imagens = pagina.get_images(full=True)

        for img_index, img in enumerate(imagens):
            xref = img[0]
            base_img = doc.extract_image(xref)

            image_bytes = base_img["image"]
            ext_original = base_img["ext"]

            # Decide formato final
            if formato_preferido:
                ext = formato_preferido.lower()
            else:
                #ext = ext_original
                ext = sugerir_formato(ext_original)

            contador += 1

            nome_arquivo = f"{prefixo}_{contador:02d}.{ext}"
            caminho_saida = os.path.join(pasta_saida, nome_arquivo)

            # Salva direto se formato for o original
            if ext == ext_original:
                with open(caminho_saida, "wb") as f:
                    f.write(image_bytes)
            else:
                # Conversão de formato (opcional)
                from PIL import Image
                import io

                img_pil = Image.open(io.BytesIO(image_bytes))
                img_pil.save(caminho_saida)

    doc.close()

    print(f"\nTotal de imagens extraídas: {contador}")
    print(f"Salvas em: {os.path.abspath(pasta_saida)}")
    print(f"[Página {num_pagina}] Imagem {contador} extraída ({ext})")

def sugerir_formato(ext_original):
    if ext_original in ["jpeg", "jpg"]:
        return "jpg"   # fotos
    elif ext_original in ["png"]:
        return "png"   # gráficos
    else:
        return "png"   # fallback

# ===============================
# EXEMPLO DE USO
# ===============================
if __name__ == "__main__":
    extrair_imagens_pdf(
        #caminho_pdf="Notas.1.pdf",
        caminho_pdf=r'D:\Ascensão Celesteial\Ascensão Celestial 12\Ascensão Celestial 12 - Img.pdf',
        pasta_saida="saida_imagens",
        prefixo="img",
        formato_preferido=None  # pode ser "png" ou "jpg"
    )