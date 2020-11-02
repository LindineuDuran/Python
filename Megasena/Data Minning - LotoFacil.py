# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 20:59:11 2020
@author: Lindineu Duran
"""
# importar as bibliotecas
import pandas as pd
import locale
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
import dateutil

# inicializar configurações de ambiente
sns.set(style="whitegrid")

sns.set(style="whitegrid")
pal = sns.dark_palette("palegreen", as_cmap=True)

locale.setlocale(locale.LC_NUMERIC, 'Portuguese_Brazil.1252')

# arquivo disponibilizado pela Caixa Ecônomica Federal
# http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_lotfac.zip

# converting a html table to a csv in python
html = open("D:\Documents\Python\Megasena\ResultadosMegasena\\d_lotfac.htm").read()
soup = BeautifulSoup(html, features="lxml")
table = soup.select_one("table.tblperiode")

# find all rows, loop through them and add row text to array
output_rows = []
for table_row in table.findAll('tr'):
    columns = table_row.findAll(['th','td'])
    output_row = []
    
    # converts numbers to American standard
    for column in columns:
        output_row.append(column.text.replace('.', '').replace(',', '.'))
        
    # only rows with correct number of columns are allowed
    if len(output_rows) > 0 and len(output_row) == len(output_rows[0]) :
        output_rows.append(output_row)
    elif len(output_rows) == 0 :
        output_rows.append(output_row)

    # make a data frame from the html table read
    df = pd.DataFrame(output_rows)

# Delete multiple columns from the dataframe
df = df.drop([0, 19, 20], axis=1)

# Rename multiple columns in one go with a larger dictionary
df = df.rename(
        columns={
                 1 :  'Data',
                 2 :  'D01',
                 3 :  'D02',
                 4 :  'D03',
                 5 :  'D04',
                 6 :  'D05',
                 7 :  'D06',
                 8 :  'D07',
                 9 :  'D08',
                 10 : 'D09',
                 11 : 'D10',
                 12 : 'D11',
                 13 : 'D12',
                 14 : 'D13',
                 15 : 'D14',
                 16 : 'D15',
                 17 : df.iloc[0][17],
                 18 : df.iloc[0][18],
                 21 : df.iloc[0][21],
                 22 : df.iloc[0][22],
                 23 : df.iloc[0][23],
                 24 : df.iloc[0][24],
                 25 : df.iloc[0][25],
                 26 : df.iloc[0][26],
                 27 : df.iloc[0][27],
                 28 : df.iloc[0][28],
                 29 : df.iloc[0][29],
                 30 : df.iloc[0][30],
                 31 : df.iloc[0][31],
                 32 : df.iloc[0][32]
                }
      )

# Delete the rows with label 0
df = df.drop([0], axis=0)

# Fix the column types
df['Data'] = df['Data'].apply(dateutil.parser.parse, dayfirst=True)
df = df.astype({'Arrecadacao_Total':'float64',
                'Ganhadores_15_Números':'int64',
                'Ganhadores_14_Números':'int64',
                'Ganhadores_13_Números':'int64',
                'Ganhadores_12_Números':'int64',
                'Ganhadores_11_Números':'int64',
                'Valor_Rateio_15_Números':'float64',
                'Valor_Rateio_14_Números':'float64',
                'Valor_Rateio_13_Números':'float64',
                'Valor_Rateio_12_Números':'float64',
                'Valor_Rateio_11_Números':'float64',
                'Acumulado_15_Números':'float64',
                'Estimativa_Premio':'float64',
                'Valor_Acumulado_Especial':'float64'})

## totaliza valor dos prêmios pagos
#df['Premios'] = df['Sena'] * df['Rateio_Sena'] + df['Quina'] * df['Rateio_Quina'] + df['Quadra'] * df['Rateio_Quadra']

# output csv
df.to_csv(r'D:\Documents\Python\Megasena\ResultadosMegasena\ResultadosLotoFacil.csv',
          encoding='latin-1', sep = ';', index = False)

# create a subset containing the columns for the dozens drawn.
balls = df[['D01','D02','D03','D04','D05','D06','D07','D08','D09','D10','D11','D12','D13','D14','D15']]

# flatten these columns into a single vector and convert the result into a DataFrame
balls_agg = pd.DataFrame( balls.values.flatten(), columns=['total'] )

# use the value_counts method from a series of values
balls_count = balls_agg['total'].value_counts(sort=True).to_frame().reset_index().sort_values('total', ascending=False)

# balls_count to csv
balls_count.to_csv(r'D:\Documents\Python\Megasena\ResultadosMegasena\LotoFacil_balls_count.csv',
          encoding='latin-1', sep = ';', index = False)

# plot the bar graph
f, ax = plt.subplots(figsize=(6, 25))

sns.barplot(y="index", x="total", data=balls_count, label="Total", orient='h', color='g', order=balls_count['index'])

ax.set(xlim=(0, 270), ylabel="", xlabel="Quantidade de vezes que a dezena foi sorteada desde 1996")
sns.despine(left=True, bottom=True)

# calculate the number of times that two dozen were chosen in the same drawing
from itertools import combinations
from collections import defaultdict

# It is possible to do the same thing with sena of balls drawn,
# changing the grouping of combinations. This time, they will be
#taken 6 in 6.
sena_list = defaultdict(lambda: 0, [])
    
for values in balls.iterrows():
    for k in combinations(values[1], 15):
        sena_list[k] += 1

# generates the combination with three balls
senas = pd.DataFrame( list(sena_list.items()), columns=['dezenas', 'total'] )

test_list = ['D01','D02','D03','D04','D05','D06','D07','D08','D09','D10','D11','D12','D13','D14','D15']
for n,col in enumerate(test_list):
    senas[col] = senas['dezenas'].apply(lambda dezena: dezena[n])

# The 50 senas of dozens that have been most drawn together to date:  
senas[['D01','D02','D03','D04','D05','D06','D07','D08','D09','D10','D11','D12','D13','D14','D15', 'total']].sort_values('total', ascending=False)[:50]

# senas to csv
senas.to_csv(r'D:\Documents\Python\Megasena\ResultadosMegasena\JogosLotoFacil.csv', encoding='latin-1', sep = ';', index = False)
