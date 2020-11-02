# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 22:51:00 2020

@author: User
"""
import pandas as pd

df = pd.read_csv('D:\\Documents\\Python\\Megasena\\ResultadosMegasena\\Teste.csv', encoding='ISO-8859-1', header=None, sep='\n')

df = df[0].str.split(';', expand=True)

df

df = df.drop(columns=0)
df = df.drop(columns=10)
df = df.drop(columns=11)
df = df.drop(columns=19)
df = df.drop(columns=20)

df.columns

df.columns = ['Data', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'Arrecadacao_Total', 'Sena', 'Rateio_Sena', 'Quina', 'Rateio_Quina', 'Quadra', 'Rateio_Quadra', 'Acumulado', 'Valor_Acumulado']

df.columns

df = df.drop([0, 1])

for row in areader:
    if row[1] == null :
        df.to_csv('D:\\Documents\\Python\\Megasena\\ResultadosMegasena\\TesteNovo.csv', sep=';', encoding='ISO-8859-1')