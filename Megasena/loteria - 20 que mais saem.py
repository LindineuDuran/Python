# Function which returns subset or r length from n 
import pandas as pd
from itertools import combinations 
from collections import defaultdict

sena_list = defaultdict(lambda: 0, [])
    
values = [4,5,10,16,17,23,24,27,28,30,32,33,34,37,42,43,44,51,53,54]
for k in combinations(values, 7):
    sena_list[k] += 1
    
# generates the combination with three balls
jogos = pd.DataFrame( list(sena_list.items()), columns=['combinações', 'total'] )

# senas to csv
jogos.to_csv(r'D:\Documents\Python\Megasena\ResultadosMegasena\jogos.txt', encoding='latin-1', sep = ';', index = False)
