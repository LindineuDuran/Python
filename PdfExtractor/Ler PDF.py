# -*- coding: utf-8 -*-
"""
Created on Tue May 26 12:51:13 2020

@author: lindineu.duran
"""

import PyPDF2
import re
import TextRegex as tr

#phoneNumRegex = re.compile(r'\d\d\d-\d\d\d-\d\d\d\d')
#mo = phoneNumRegex.search('My number is 415-555-4242.')
#print('Phone number found: ' + mo.group())

# pdf_file = open('C:\\Users\\lindineu.duran\\Documents\\Python\\PdfExtractor\\PDFs de Notas Fiscais\\Notas.pdf', 'rb')
# pdf_file = open( r'D:\Documentos\Python\PdfExtractor\PDFs de Notas Fiscais\000.010.326-9699194376-4500187916.pdf', 'rb')
pdf_file = open( r'D:\Documentos\Python\PdfExtractor\PDFs de Notas Fiscais\1262-9600101513-4500185105.pdf', 'rb')

try:
    pdfReader = PyPDF2.PdfReader(pdf_file, strict=False)

    number_of_pages = len(pdfReader.pages)
    print("Número de Paginas:" + str(number_of_pages))

    for x in range(number_of_pages):
        page = pdfReader.pages[x]
        page_content = page.extract_text()

        parsed = ''.join(page_content)
        # parsed = re.sub('\r\n', '', parsed)

        #print('Conteúdo:' + parsed.replace('\n', '') + '***')

        print('Conteúdo:' + parsed + '***')

        numNF = tr.obtem_num_serie(parsed)
        print("NumNF: ", numNF)
        
        chave = tr.obtem_chave(parsed)
        print("Chave: ", chave)

        cnpj = tr.obtem_cnpj(parsed)
        print("CNPJ: " + cnpj)
except ValueError:
    print(ValueError)
    print("Erro ao ler PDF!")
