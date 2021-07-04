import csv
import shutil, os

def get_csv_column(filename, column):
    with open(filename,encoding='utf-8') as stream:
        reader = csv.reader(stream)
        for row in reader:
            yield row[column]

# print( list(get_csv_column(r'C:\Users\lindineu.duran\Downloads\PDFs - MELI\lista_de_lixo_novo.txt', 0)) )

lista_de_arquivos = list(get_csv_column(r'C:\Users\lindineu.duran\Downloads\PDFs - MELI\lista_de_lidos.txt', 0))
print(lista_de_arquivos)

pasta_origem = r'C:\Users\lindineu.duran\Downloads\PDFs - MELI'
pasta_destino = r'C:\Users\lindineu.duran\Downloads\PDFs - MELI\Carregado'

for arq in lista_de_arquivos:
    origem = os.path.join(pasta_origem, arq)
    destino = os.path.join(pasta_destino, arq)

    try:
        shutil.move(origem, destino)
    except:
        print('Erro no arquivo ', arq)
