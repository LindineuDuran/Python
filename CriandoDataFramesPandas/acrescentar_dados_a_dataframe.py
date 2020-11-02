# The convention is to import Pandas with shortcut 'pd'
import pandas as pd
import  os

columns = ['Date', 'Name', 'Action','ID']
df = pd.DataFrame(columns=columns)

print(df)

df.loc[len(df)]=['8/19/2014','Jun','Fly','98765']

print(df)

print('==================================================')

# Criando o DataFrame
df = pd.DataFrame(columns=['País','Capital','População'])
print(df)

print('==================================================')

df.loc[len(df)]=['Bélgica','Bruxelas',123465]
print(df)

print('==================================================')

df.loc[len(df)]=['Índia','Nova Delhi',456789]
print(df)

print('==================================================')

df.loc[len(df)]=['Brasil','Brasília',987654]
print(df)

print('==================================================')
