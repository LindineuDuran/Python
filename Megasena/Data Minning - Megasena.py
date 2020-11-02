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
# http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_mgsasc.zip

# converting a html table to a csv in python
html = open("D:\Documents\Python\Megasena\Resultados Megasena\d_megasc.htm").read()
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
df.to_csv(r'D:\Documents\Python\Megasena\Resultados Megasena\ResultadosMegaSena.txt',
          encoding='latin-1', sep = ';', index = False)

# create a subset containing the columns for the dozens drawn.
balls = df[['D1','D2','D3','D4','D5','D6']]

# flatten these columns into a single vector and convert the result into a DataFrame
balls_agg = pd.DataFrame( balls.values.flatten(), columns=['total'] )

# use the value_counts method from a series of values
balls_count = balls_agg['total'].value_counts(sort=True).to_frame().reset_index().sort_values('total', ascending=False)

# balls_count to csv
balls_count.to_csv(r'D:\Documents\Python\Megasena\Resultados Megasena\balls_count.txt',
          encoding='latin-1', sep = ';', index = False)

# plot the bar graph
f, ax = plt.subplots(figsize=(6, 25))

sns.barplot(y="index", x="total", data=balls_count, label="Total", orient='h', color='g', order=balls_count['index'])

ax.set(xlim=(0, 270), ylabel="", xlabel="Quantidade de vezes que a dezena foi sorteada desde 1996")
sns.despine(left=True, bottom=True)

# calculate the number of times that two dozen were chosen in the same drawing
from itertools import combinations
from collections import defaultdict
pair_list = defaultdict(lambda: 0, [])

# iterate over the subset of results (which has columns D1 .. D6),
# taking the values from two to two and increasing in the dictionary
# the count of times the pair appears
for values in balls.iterrows():
    for k in combinations(values[1], 2):
        pair_list[k] += 1

# After the iteration, the dictionary is transformed into a DataFrame with two columns
# (dozens and total times that appear together)
pairs = pd.DataFrame( list(pair_list.items()), columns=['dezenas', 'total'])

# pairs to csv
pairs.to_csv(r'D:\Documents\Python\Megasena\Resultados Megasena\pairs.txt', encoding='latin-1', sep = ';', index = False)

# separate the dozens column in D1 and D2 to facilitate work with the data
new_col_list = ['d1','d2']
for n,col in enumerate(new_col_list):
    pairs[col] = pairs['dezenas'].apply(lambda dezena: dezena[n])

# observe the combinations between two dozens drawn
# and the frequency with which these dozens are drawn together
#cusing a heatmap
f, ax = plt.subplots(figsize=(33, 18))
pairs2 = pairs.pivot('d2','d1', 'total')

sns.color_palette("Paired")
sns.heatmap(pairs2, square=True, ax=ax, linewidths=.2, cmap=sns.light_palette("green", as_cmap=True))
ax.set(xlim=(0, 61), ylabel="Dezena", xlabel="Pares sorteados em um mesmo sorteio")
f.tight_layout()

# The 20 most frequent combinations, now in list format
pairs[['d1','d2','total']].sort_values('total', ascending=False)[:20]

# It is possible to do the same thing with trios of balls drawn,
# changing the grouping of combinations. This time, they will be
#taken 3 in 3.
trio_list = defaultdict(lambda: 0, [])

for values in balls.iterrows():
    for k in combinations(values[1], 3):
        trio_list[k] += 1

# generates the combination with three balls
trios = pd.DataFrame( list(trio_list.items()), columns=['dezenas', 'total'] )

new_col_list = ['d1','d2','d3']
for n,col in enumerate(new_col_list):
    trios[col] = trios['dezenas'].apply(lambda dezena: dezena[n])

# The 50 trios of dozens that have been most drawn together to date:
trios[['d1','d2', 'd3', 'total']].sort_values('total', ascending=False)[:50]

# trios to csv
trios.to_csv(r'D:\Documents\Python\Megasena\Resultados Megasena\trios.txt', encoding='latin-1', sep = ';', index = False)

# plot the fundraising graph, in a weaker color
# and then plot the prize graph, in a stronger color
f, ax = plt.subplots(figsize=(8, 40))

anos = df[df["Arrecadacao_Total"]> 0].groupby( df.Data.dt.to_period("M") )

sns.set_color_codes("pastel")
sns.barplot(y='Data', x='Arrecadacao_Total', label=u"Arrecadação", data=anos['Arrecadacao_Total'].sum().reset_index(), color='g', orient='h' )

sns.set_color_codes("muted")
sns.barplot(y='Data', x='Premios', label=u"Premiação", data=anos['Premios'].sum().reset_index(), color='g', orient='h' )

ax.legend(ncol=2, loc="upper right", frameon=True)
ax.set(ylabel=u"Ano/Mês", xlabel=u"Valor mensal em Centenas de Milhões")

# It is possible to do the same thing with sena of balls drawn,
# changing the grouping of combinations. This time, they will be
#taken 6 in 6.
sena_list = defaultdict(lambda: 0, [])

for values in balls.iterrows():
    for k in combinations(values[1], 6):
        sena_list[k] += 1

# generates the combination with three balls
senas = pd.DataFrame( list(sena_list.items()), columns=['dezenas', 'total'] )

test_list = ['d1','d2','d3','d4','d5','d6']
for n,col in enumerate(test_list):
    senas[col] = senas['dezenas'].apply(lambda dezena: dezena[n])

# The 50 senas of dozens that have been most drawn together to date:
senas[['d1','d2','d3','d4','d5','d6', 'total']].sort_values('total', ascending=False)[:50]

# senas to csv
senas.to_csv(r'D:\Documents\Python\Megasena\Resultados Megasena\senas.txt', encoding='latin-1', sep = ';', index = False)
