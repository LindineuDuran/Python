# The convention is to import Pandas with shortcut 'pd'
import pandas as pd
import  os

# Criando um dicionário onde cada chave será uma coluna do DataFrame
data = {
            'País': ['Bélgica', 'Índia', 'Brasil'],
            'Capital': ['Bruxelas', 'Nova Delhi', 'Brasília'],
            'População': [123465, 456789, 987654]
       }

# Criando o DataFrame
df = pd.DataFrame(data, columns=['País','Capital','População'])
print(df)
