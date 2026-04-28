# VisionParse OCR

## Desenvolvido por Lindineu Duran
## Contato: lduran355@gmail.com

VisionParse é uma solução avançada de OCR (Optical Character Recognition) 
projetada para transformar imagens e documentos PDF em dados estruturados.

## Principais recursos:
• Visualização de imagens e PDFs
• Navegação com zoom e panorâmica
• Rotação e manipulação de imagens
• Extração de texto com OCR
• Preparação de dados para processamento posterior

## Run
pip install -r requirements.txt
python app/main.py


## Recurso Externo Necessário
Para que o projeto funcione, o aplicativo Tesseract-OCR deve ser colocado na raiz do projeto, "..\VisionParseOCR\";


🔥 ATUALIZE O TESSERACT
👉 Use a versão correta para Windows:
Baixe daqui:
👉 https://github.com/UB-Mannheim/tesseract/wiki


Use ESTE traineddata (compatível com Tesseract 4+ / 5+):
https://github.com/tesseract-ocr/tessdata_best/raw/main/por.traineddata

OU (mais leve e rápido):
https://github.com/tesseract-ocr/tessdata_fast/raw/main/por.traineddata

COLOQUE EM:
"..\VisionParseOCR\Tesseract-OCR\tessdata\"


