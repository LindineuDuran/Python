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

# --------------------
# Obtêm Lista de Ações
# --------------------
acoes_ibov = pd.read_excel("IBOV.xlsx")
# acoes_ibov = pd.read_excel("Papéis BOVESPA.xlsx")
# acoes_ibov = pd.read_excel("IBOV -Teste.xlsx")

#print(acoes_ibov)

# ---------------------------------------------------------------------------------------
# Cria variavel dataframe vazio para consolidar e armazenar as informações em um lugar só
# ---------------------------------------------------------------------------------------
consolidado_acoes = pd.DataFrame()
# print(consolidado_acoes)

# --------------------------------------------------------
# Fazendo o programa repetir os passos para diversas acoes
# --------------------------------------------------------
for codigo_acao in acoes_ibov["Código"]:
    # --------------------------------
    # Acessando página com informações
    # --------------------------------
    print("Coletando informações do papel:", codigo_acao)

    # ----------------------------
    # A url que você quer acesssar
    # ----------------------------
    url = "https://br.advfn.com/bolsa-de-valores/bovespa/" + codigo_acao + "/cotacao"

    # ---------------------------------------
    #Informações para fingir ser um navegador
    # ---------------------------------------
    header = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"
             }

    # ---------------------------
    #juntamos tudo com a requests
    # ---------------------------
    r = requests.get(url, headers=header)

    # ------------------------------------------------
    # E finalmente usamos a função read_html do pandas
    # ------------------------------------------------
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
    # print(acao)

    # -------------------------------------------------
    # Cria um consolidado com as informações capturadas
    # -------------------------------------------------
    if acao.loc[0,'Variação do Dia (p)'] != 0:
        consolidado_acoes = consolidado_acoes.append(acao, sort=False)

# -------------------------------
# Redefinindo a ordem das colunas
# -------------------------------
if consolidado_acoes.shape[0] > 0:
    consolidado_acoes = consolidado_acoes[['Nome da Ação', 'Código da Ação', 'Último Preço', 'Hora', 'Data de Extração', 'Preço Mínimo', 'Preço Máximo', 'Preço de Abertura', 'Fech. Anterior']]

# --------------------------
# Salvando dados em um excel
# --------------------------
consolidado_acoes.to_excel("Ações do IBOV - ADVFN.xlsx", index=False)

# # -------------------------------------------------
# # cria um subconjunto contendo as colunas desejadas
# # -------------------------------------------------
# consolidado_analise = consolidado_acoes[['Nome da Ação', 'Código da Ação', 'Bolsa de Valores', 'Tipo de Ativo', 'Hora', 'Data de Extração', 'Variação do Dia (p)',
#                                          'Variação do Dia %', 'Último Preço', 'Preço Mínimo', 'Preço Máximo', 'Preço de Abertura', 'Fech. Anterior',
#                                          'Abe 1 Semana',  'Máx. 1 Semana', 'Mín. 1 Semana', 'Preço Méd. 1 Semana', 'Vol Méd. 1 Semana', 'Var 1 Semana', '% 1 Semana',
#                                          'Abe 1 Mês', 'Máx. 1 Mês', 'Mín. 1 Mês', 'Preço Méd. 1 Mês', 'Vol Méd. 1 Mês', 'Var 1 Mês', '% 1 Mês',
#                                          'Abe 3 Meses', 'Máx. 3 Meses', 'Mín. 3 Meses', 'Preço Méd. 3 Meses', 'Vol Méd. 3 Meses', 'Var 3 Meses', '% 3 Meses']]
#
# # --------------------------
# # Salvando dados em um excel
# # --------------------------
# consolidado_analise.to_excel("Ações do IBOV - ADVFN (Para Análise).xlsx", index=False)
