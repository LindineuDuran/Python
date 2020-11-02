# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 17:30:40 2020

@author: User
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 20:59:11 2020
@author: Lindineu Duran
"""
# importar as bibliotecas
import pandas as pd
import locale
import matplotlib.pyplot as plt
import numpy as np 
import seaborn as sns
from bs4 import BeautifulSoup
import dateutil
import csv
import qgrid

# inicializar configurações de ambiente
sns.set(style="whitegrid")

sns.set(style="whitegrid")
pal = sns.dark_palette("palegreen", as_cmap=True)

locale.setlocale(locale.LC_NUMERIC, 'Portuguese_Brazil.1252')

# arquivo disponibilizado pela Caixa Ecônomica Federal
# http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_mgsasc.zip

# converting a html table to a csv in python
html = open("D:\Documents\Python\Megasena\ResultadosMegasena\\d_megasc.htm").read()
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
df = df.drop([0, 10, 11, 19, 20], axis=1)

# Delete the rows with label 0
df = df.drop([0], axis=0)


# Rename multiple columns in one go with a larger dictionary
df = df.rename(
        columns={
                 1: 'Data',
                 2: 'D1',
                 3: 'D2',
                 4: 'D3',
                 5: 'D4',
                 6: 'D5',
                 7: 'D6',
                 8: 'Arrecadacao_Total',
                 9: 'Sena',
                 12: 'Rateio_Sena',
                 13: 'Quina',
                 14: 'Rateio_Quina',
                 15: 'Quadra',
                 16: 'Rateio_Quadra',
                 17: 'Acumulado',
                 18: 'Valor_Acumulado'
                }
      )

# Fix the column types
df['Data'] = df['Data'].apply(dateutil.parser.parse, dayfirst=True)
df = df.astype({'Arrecadacao_Total':'float64',
                'Sena':'int64',
                'Rateio_Sena':'float64',
                'Quina':'int64',
                'Rateio_Quina':'float64',
                'Quadra':'int64',
                'Rateio_Quadra':'float64',
                'Acumulado':'str',
                'Valor_Acumulado':'float64'})

# totaliza valor dos prêmios pagos
df['Premios'] = df['Sena'] * df['Rateio_Sena'] + df['Quina'] * df['Rateio_Quina'] + df['Quadra'] * df['Rateio_Quadra']

# output csv
df.to_csv(r'D:\Documents\Python\Megasena\ResultadosMegasena\ResultadosMegaSena.txt',
          encoding='latin-1', sep = ';', index = False)

# create a subset containing the columns for the dozens drawn.
balls_date = df[['Data','D1','D2','D3','D4','D5','D6']]

# balls_count to csv
balls_date.to_csv(r'D:\Documents\Python\Megasena\ResultadosMegasena\balls_date.txt',
          encoding='latin-1', sep = ';', index = False)