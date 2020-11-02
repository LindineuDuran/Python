from bs4 import BeautifulSoup
import csv
import os

app_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(app_path, 'd_megasc_teste.htm')

#read the html
html = open(file_path).read()
soup = BeautifulSoup(html, 'html.parser')

# get the table from html
table = soup.select_one("table.tblperiode")

# find all rows
rows = table.findAll('tr')

# strip the header from rows
headers = rows[0]
header_text = []

# add the header text to array
for th in headers.findAll('th'):
    header_text.append(th.text)

# init row text array
row_text_array = []

# loop through rows and add row text to array
for row in rows[1:]:
    row_text = []
    
    # loop through the elements
    for row_element in row.findAll(['td']):
        coluna = row_element.text.replace('.', '').replace(',', '.').strip()
        
        # append the array with the elements inner text
        row_text.append(coluna)
        
    # append the text array to the row text array
    if len(row_text) == len(header_text) : row_text_array.append(row_text)

#insert the header_text in the begin of row_text_array
row_text_array.insert(0, header_text)

# output csv
out_file_path = os.path.join(app_path, 'out.csv')
with open(out_file_path, "w") as f:
    wr = csv.writer(f, delimiter=';')
    
    # loop through each row array
    for row_text_single in row_text_array:
        wr.writerow(row_text_single)
        
#print(row_text_array)
