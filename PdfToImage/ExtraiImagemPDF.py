def convert(filepath):
    with open(filepath, "rb") as file:
        pdf = file.read()

    startmark = b"\xff\xd8"
    startfix = 0
    endmark = b"\xff\xd9"
    endfix = 2
    i = 0

    njpg = 0
    while True:
        istream = pdf.find(b"stream", i)
        if istream < 0:
            break
        istart = pdf.find(startmark, istream, istream + 20)
        if istart < 0:
            i = istream + 20
            continue
        iend = pdf.find(b"endstream", istart)
        if iend < 0:
            raise Exception("Didn't find end of stream!")
        iend = pdf.find(endmark, iend - 20)
        if iend < 0:
            raise Exception("Didn't find end of JPG!")

        istart += startfix
        iend += endfix
        jpg = pdf[istart:iend]
        newfile = "{}jpg".format(filepath[:-3])
        with open(newfile, "wb") as jpgfile:
            jpgfile.write(jpg)

        njpg += 1
        i = iend

        return newfile

# Teste = convert('C:\\Users\\lindineu.duran\\Documents\\Python\\PdfToImage\\Dirf 2020.pdf')
Teste = convert(r'C:\Users\lindineu.duran\Documents\Python\PdfExtractor\PDFs de Notas Fiscais\14102020 7122 CHAMPION-PO Bloq.PDF')
print(Teste)
