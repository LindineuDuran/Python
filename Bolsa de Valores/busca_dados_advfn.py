# ----------------------
# Carrega as Bibliotecas
# ----------------------
import pandas as pd
import requests
from datetime import datetime

# ----------------------------
# Rotina para renomear colunas
# ----------------------------
def renomeia_colunas(df, nome_coluna):
    # -----------------------------------------------------
    # Transforma a primeira linha do dataframe em cabecalho
    # -----------------------------------------------------
    df.columns = df.iloc[0] # Define o cabeçalho como a primeira linha
    df = df.drop(0) # Deleta a linha zero, que passou a ser o cabeçalho

    # -------------------
    # Renomeia as colunas
    # -------------------
    df = df.rename(columns = {
                                '1 Semana' :  nome_coluna + ' 1 Semana',
                                '1 Mês' :  nome_coluna + ' 1 Mês',
                                '3 Meses' :  nome_coluna + ' 3 Meses',
                                '6 Meses' :  nome_coluna + ' 6 Meses',
                                '1 Ano' :  nome_coluna + ' 1 Ano',
                                '3 Anos' :  nome_coluna + ' 3 Anos',
                                '5 Anos' :  nome_coluna + ' 5 Anos'
                             },
                             inplace = False)

    # -------------------------------------------
    # Resetando o index para juntar no concatenar
    # -------------------------------------------
    df = df.reset_index(drop=True) # drop=True remove o index anterior salvo pela função em uma nova coluna
    # print(df)

    return df

# ----------------------------
# A url que você quer acesssar
# ----------------------------
url = "https://br.advfn.com/bolsa-de-valores/bovespa/ARZZ3/cotacao"

# ---------------------------------------
#Informações para fingir ser um navegador
# ---------------------------------------
header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}
#juntamos tudo com a requests
r = requests.get(url, headers=header)

# ---------------------------
#juntamos tudo com a requests
# ---------------------------
acao = pd.read_html(r.text,
                    decimal=",",
                    thousands=".")

# -------------------------------------------
# Descobre a tabela de informações do período
# -------------------------------------------
num_itens_acao = len(acao)
#print(num_itens_acao)

periodo = pd.DataFrame()
for item in range(4, num_itens_acao):
    if 'Período' in acao[item].columns:
        acao[item] = acao[item].transpose()
        periodo = acao[item]
        break

# -----------------------------------
# Fatia a informação de Identificação
# -----------------------------------
identificacao = acao[1].iloc[:1, 0:4]
# print(identificacao)

# Fatia a informação de Variação do Dia
variacao_dia = acao[2].iloc[:1, 1:5]
variacao_dia['Data de Extração'] = datetime.now()
# print(variacao_dia)

# ----------------------------------
# Fatia a informação de Preço do Dia
# ----------------------------------
preco_dia = acao[3].iloc[:1, 1:5]
# print(preco_dia)

# ---------------------------------------
# Fatia a informação de Valor de Abertura
# ---------------------------------------
abertura = periodo.iloc[[0, 1]]
# print(abertura)

# ----------------------------------
# Fatia a informação de Valor Máximo
# ----------------------------------
maximo = periodo.iloc[[0, 2]]
# print(maximo)

# ----------------------------------
# Fatia a informação de Valor Mínimo
# ----------------------------------
minino = periodo.iloc[[0, 3]]
# print(minino)

# ---------------------------------
# Fatia a informação de Preço Médio
# ---------------------------------
preco_med = periodo.iloc[[0, 4]]
# print(preco_med)

# ----------------------------------
# Fatia a informação de Volume Médio
# ----------------------------------
vol_med = periodo.iloc[[0, 5]]
# print(vol_med)

# ------------------------------
# Fatia a informação de Variação
# ------------------------------
variacao = periodo.iloc[[0, 6]]
# print(variacao)

# --------------------------------
# Fatia a informação de Percentual
# --------------------------------
percent = periodo.iloc[[0, 7]]
# print(percent)

# -------------------------------------------
# Resetando o index para juntar no concatenar
# -------------------------------------------
identificacao = identificacao.reset_index(drop=True) # drop=True remove o index anterior salvo pela função em uma nova coluna
variacao_dia = variacao_dia.reset_index(drop=True) # drop=True remove o index anterior salvo pela função em uma nova coluna
preco_dia = preco_dia.reset_index(drop=True) # drop=True remove o index anterior salvo pela função em uma nova coluna
abertura = abertura.reset_index(drop=True) # drop=True remove o index anterior salvo pela função em uma nova coluna
maximo = maximo.reset_index(drop=True) # drop=True remove o index anterior salvo pela função em uma nova coluna
minino = minino.reset_index(drop=True) # drop=True remove o index anterior salvo pela função em uma nova coluna
preco_med = preco_med.reset_index(drop=True) # drop=True remove o index anterior salvo pela função em uma nova coluna
vol_med = vol_med.reset_index(drop=True) # drop=True remove o index anterior salvo pela função em uma nova coluna
variacao = variacao.reset_index(drop=True) # drop=True remove o index anterior salvo pela função em uma nova coluna
percent = percent.reset_index(drop=True) # drop=True remove o index anterior salvo pela função em uma nova coluna

# print(identificacao,variacao_dia,abertura)

# ----------------
# Renomeia colunas
# ----------------
abertura = renomeia_colunas(abertura, 'Abe')
maximo = renomeia_colunas(maximo, 'Máx.')
minino = renomeia_colunas(minino, 'Mín.')
preco_med = renomeia_colunas(preco_med, 'Preço Méd.')
vol_med = renomeia_colunas(vol_med, 'Vol Méd.')
variacao = renomeia_colunas(variacao, 'Var')
percent = renomeia_colunas(percent, '%')

# ------------
# Concatenando
# ------------
acao = pd.concat([identificacao,
                  variacao_dia,
                  preco_dia,
                  abertura,
                  maximo,
                  minino,
                  preco_med,
                  vol_med,
                  variacao,
                  percent
                 ], # Quais tabelas quero concatenar em uma só
                 axis=1, # Quero concatenar em colunas
                 join='inner') # Tipo de concatenar inner = o que é comum aos dois

acao = acao.reset_index(drop=True) # drop=True remove o index anterior salvo pela função em uma nova coluna

print(acao)

# --------------------------
# Salvando dados em um excel
# --------------------------
acao.to_excel("Teste Extração - Ações do IBOV.xlsx", index=False)
