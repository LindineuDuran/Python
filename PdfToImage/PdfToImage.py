from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image  # Importando o módulo Pillow para abrir a imagem no script
import pytesseract  # Módulo para a utilização da tecnologia OCR

dpi = 200 # dots per inch
pdf_file = 'C:\\Users\\lindineu.duran\\Documents\\Python\\PdfToImage\\Dirf 2020.pdf'
pages = convert_from_path(pdf_file ,dpi )
for i in range(len(pages)):
   page = pages[i]
   page.save('output_{}.jpg'.format(i), 'JPEG')
