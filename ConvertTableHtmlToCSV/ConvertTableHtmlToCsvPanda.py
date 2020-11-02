from bs4 import BeautifulSoup
import csv
import pandas as pd
import os

app_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(app_path, 'd_megasc_teste.htm')

html = open(file_path).read()
soup = BeautifulSoup(html, features="lxml")
table = soup.select_one("table.tblperiode")

output_rows = []
for table_row in table.findAll('tr'):
    columns = table_row.findAll(['th','td'])
    output_row = []
    
    for column in columns:
        output_row.append(column.text.replace('.', '').replace(',', '.'))
        
    if len(output_row) == 21 : output_rows.append(output_row)

    df = pd.DataFrame(output_rows)

# Delete multiple columns from the dataframe
df = df.drop([0, 10, 11, 19, 20], axis=1)

# Delete the rows with label 0
df = df.drop([0], axis=0)


# Rename multiple columns in one go with a larger dictionary
df = df.rename(
        columns={
                 1: "Data",
                 2: "D1",
                 3: "D2",
                 4: "D3",
                 5: "D4",
                 6: "D5",
                 7: "D6",
                 8: "Arrecadacao_Total",
                 9: "Sena",
                 12: "Rateio_Sena",
                 13: "Quina",
                 14: "Rateio_Quina",
                 15: "Quadra",
                 16: "Rateio_Quadra",
                 17: "Acumulado",
                 18: "Valor_Acumulado"
                }
)

out_file_path = os.path.join(app_path, 'out.csv')
df.to_csv(out_file_path, encoding='latin-1', sep = ';', index = False)