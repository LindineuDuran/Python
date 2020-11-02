# ----------------------
# Carrega as Bibliotecas
# ----------------------
import pandas as pd
import requests
from datetime import datetime

# ----------------------------
# A url que você quer acesssar
# ----------------------------
url = "https://finance.yahoo.com/quote/PETR4.SA/history?p=PETR4.SA"

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
acao[0].to_excel("Teste Extração - Yahoo (PETR4).xlsx", index=False)

# # output csv
# acao[0].to_csv(r'Teste Extração - Yahoo (PETR4).txt', encoding='latin-1', sep = ';', index = False)
