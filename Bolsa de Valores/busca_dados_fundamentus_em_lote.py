# O que é uma biblioteca
import pandas as pd
import requests

# Lendo um arquivo Excel
acoes_ibov = pd.read_excel("IBOV.xlsx")
print(acoes_ibov)

# Fazendo o programa repetir os passos para diversas acoes
###################################PASSO ADICIONAL PARA CONCATENAR AS INFORMACOES#######################################

# Cria variavel dataframe vazio para consolidar e armazenar as informações em um lugar só
consolidado_acoes = pd.DataFrame()

print(consolidado_acoes)

for codigo_acao in acoes_ibov["Código"]:
    # Acessando página com informações

    print("Coletando informações do papel:", codigo_acao)

    #A url que você quer acesssar
    url = "https://www.fundamentus.com.br/detalhes.php?papel=" + codigo_acao

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

    # Transpondo as tabelas
    acao[0] = acao[0].transpose()
    acao[1] = acao[1].transpose()
    acao[2] = acao[2].transpose()

    # Separando os grupos de informações sobre a acao para organizar em colunas
    # Primeira tabela
    informações_1 = acao[0].iloc[:2, :]
    informações_2 = acao[0].iloc[2:, :]

    # Segunda tabela
    informações_3 = acao[1].iloc[:2, :]
    informações_4 = acao[1].iloc[2:, :]

    # Terceira tabela
    informações_5 = acao[2].iloc[:2, 1:4]

    # Resetando o index para juntar no concatenar
    informações_2 = informações_2.reset_index(drop=True) # drop=True remove o index anterior salvo pela função em uma nova coluna
    informações_4 = informações_4.reset_index(drop=True) # drop=True remove o index anterior salvo pela função em uma nova coluna

    # Concatenando as informações em uma linha única
    acao = pd.concat([informações_1,
                      informações_2,
                      informações_3,
                      informações_4,
                      informações_5,
                     ], # Quais tabelas quero concatenar em uma só
                     axis=1, # Quero concatenar em colunas
                     join='inner') # Tipo de concatenar inner = o que é comum aos dois

    # Transforma a primeira linha em cabecalho
    acao.columns = acao.iloc[0] # Define o cabeçalho como a primeira linha
    acao = acao.drop(0) # Deleta a linha zero, que passou a ser o cabeçalho

    # Cria um consolidado com as informações capturadas
    consolidado_acoes = consolidado_acoes.append(acao, sort=False)

    ## Mostra o robo colocando as informacoes uma a uma na tabela
    ## Remover depois
    #print(consolidado_acoes)

# Rename column
consolidado_acoes = consolidado_acoes.rename(columns = {
                                                          'Dia': 'Osc. Dia',
                                                          'Mês': 'Osc. Mês',
                                                          '30 dias': 'Osc. 30 dias'
                                                       },
                                                       inplace = False)

print(consolidado_acoes)

# Correcoes finais no consolidado

# corrigindo index do consolidado
consolidado_acoes = consolidado_acoes.reset_index(drop=True)

print(consolidado_acoes)

# Remove as interrogações do cabeçalho
# acao.columns é uma lista, deve navegar na lista removendo os "?"
novo_cabecalho = [coluna.replace('?', '') for coluna in consolidado_acoes.columns]
consolidado_acoes.columns = novo_cabecalho # Diz que acao.columns agora recebe o novo_cabecalho

# Corrigindo as duas colunas de datas
consolidado_acoes["Data últ cot"] = pd.to_datetime(consolidado_acoes["Data últ cot"],
                                                   errors='ignore',
                                                   format="%d/%m/%Y"
                                                  )

consolidado_acoes["Últ balanço processado"] = pd.to_datetime(consolidado_acoes["Últ balanço processado"],
                                                             errors='ignore',
                                                             format="%d/%m/%Y"
                                                            )

# Corrigindo colunas com valores numéricos
consolidado_acoes["Vol $ méd (2m)"] = pd.to_numeric(consolidado_acoes["Vol $ méd (2m)"],
                                                    errors='coerce'
                                                   )

consolidado_acoes["Valor de mercado"] = pd.to_numeric(consolidado_acoes["Valor de mercado"],
                                                      errors='coerce'
                                                     )

consolidado_acoes["Valor da firma"] = pd.to_numeric(consolidado_acoes["Valor da firma"],
                                                    errors='coerce'
                                                   )

consolidado_acoes["Nro. Ações"] = pd.to_numeric(consolidado_acoes["Nro. Ações"],
                                                errors='coerce'
                                               )

print(consolidado_acoes)

# Salvando dados em um excel
consolidado_acoes.to_excel("Ações do IBOV - Fundamentus.xlsx", index=False)
