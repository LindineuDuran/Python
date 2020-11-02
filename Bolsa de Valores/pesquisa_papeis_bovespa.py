# O que é uma biblioteca
import pandas as pd
import requests

# Criando um dicionário onde cada chave será uma coluna do DataFrame
data = {
            'Letras': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
       }

# Criando o DataFrame
df = pd.DataFrame(data, columns=['Letras'])
print(df)

# Cria variavel dataframe vazio para consolidar e armazenar as informações em um lugar só
consolidado_papeis = pd.DataFrame()

for letra in df["Letras"]:
    # Acessando página com informações

    #A url que você quer acesssar
    url = "https://br.advfn.com/bolsa-de-valores/bovespa/" + letra
    print(url)

    #Informações para fingir ser um navegador
    header = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"
             }

    #juntamos tudo com a requests
    r = requests.get(url, headers=header)

    #E finalmente usamos a função read_html do pandas
    acao = pd.read_html(r.text,
                        decimal=",",
                        thousands=".")
    #print(acao)
    #print(acao[0])

    # Cria um consolidado com as informações capturadas
    consolidado_papeis = consolidado_papeis.append(acao[0], sort=False)

# Rename column
consolidado_papeis = consolidado_papeis.rename(columns = {'Unnamed: 1': 'Código'}, inplace = False)

# Troca a ordem das colunas
consolidado_papeis = consolidado_papeis[['Código', 'Ação']]

print(consolidado_papeis)

# Salvando dados em um excel sem a coluna de índice
consolidado_papeis.to_excel("Papéis BOVESPA.xlsx",
                           index=False)
