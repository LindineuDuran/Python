# ----------------------
# Carrega as Bibliotecas
# ----------------------
import pandas as pd
import requests
from datetime import datetime

# --------------------
# Obtêm Lista de Ações
# --------------------
acoes_ibov = pd.read_excel("IBOV.xlsx")
# acoes_ibov = pd.read_excel("Papéis BOVESPA.xlsx")
# acoes_ibov = pd.read_excel("IBOV -Teste.xlsx")

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
    url = "https://finance.yahoo.com/quote/" + codigo_acao + ".SA/history?p=" + codigo_acao + ".SA"

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
                        decimal=".",
                        thousands=",")

    # --------------------------
    # Salvando dados em um excel
    # --------------------------
    print(acao[0])
    acao[0].to_excel("Teste Extração - Yahoo (" + codigo_acao + ").xlsx", index=False)
