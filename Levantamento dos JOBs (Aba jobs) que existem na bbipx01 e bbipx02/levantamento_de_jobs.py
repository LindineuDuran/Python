import pandas as pd
import re

def ler_colunas_jobs(arquivo_excel, aba="Jobs", colunas=["NOME_CADEIA", "JOB_NAME"]):
    """
    Lê as colunas especificadas de uma aba em um arquivo Excel e retorna um DataFrame.

    :param arquivo_excel: Caminho do arquivo Excel (.xlsx)
    :param aba: Nome da aba onde estão as colunas (padrão: "Jobs")
    :param colunas: Lista de colunas a serem lidas (padrão: ["NOME_CADEIA", "JOB_NAME"])
    :return: DataFrame contendo apenas as colunas desejadas
    """
    try:
        df = pd.read_excel(arquivo_excel, sheet_name=aba, usecols=colunas)
        return df
    except Exception as e:
        print(f"Erro ao ler o arquivo {arquivo_excel}: {e}")
        return None

def filtrar_outros_jobs(df):
    """Filtra o DataFrame para excluir registros cujo NOME_CADEIA começa com 'MIGRADO_' ou 'REMOVER_'."""
    if df is None:
        return None
    return df[~df["NOME_CADEIA"].str.startswith(("MIGRADO_", "REMOVER_"), na=False)]

def extrair_nome_dataframe(nome_arquivo):
    """
    Extrai os caracteres após o ÚLTIMO '_' antes de '.xlsx' para formar um nome significativo.

    Exemplo:
    "Levantamento_JETL_VTAL_bddpx01.xlsx" -> "bddpx01"
    "Levantamento_JETL_VTAL_gc-jetlpx01.xlsx" -> "jetlpx01"
    """
    nome_base = nome_arquivo.rsplit("_", 1)[-1]  # Pega tudo após o último "_"
    return nome_base.replace(".xlsx", "")  # Remove a extensão

def comparar_jobs(df1: pd.DataFrame, df2: pd.DataFrame, nome_df1: str, nome_df2: str):
    """
    Compara as colunas JOB_NAME de dois dataframes e retorna um dataframe
    contendo apenas os jobs presentes no primeiro e ausentes no segundo.
    
    Parâmetros:
    - df1: DataFrame principal
    - df2: DataFrame a ser comparado
    - nome_df1: Nome identificador do primeiro DataFrame
    - nome_df2: Nome identificador do segundo DataFrame
    
    Retorna:
    - Um novo DataFrame filtrado
    """
    
    # Garantir que JOB_NAME está presente nos dois DataFrames
    if 'JOB_NAME' not in df1.columns or 'JOB_NAME' not in df2.columns:
        raise ValueError("Ambos os DataFrames devem conter a coluna 'JOB_NAME'")
    
    # Filtrar os jobs que estão em df1 e não estão em df2
    df_filtrado = df1[~df1['JOB_NAME'].isin(df2['JOB_NAME'])]
    
    # Nome do dataframe resultante
    nome_resultado = f"df_jobs_presentes_{nome_df1}_ausentes_{nome_df2}"
    
    return nome_resultado, df_filtrado

# Lista de arquivos a serem processados
arquivos = [
    "Levantamento_JETL_VTAL_bddpx01.xlsx",
    "Levantamento_JETL_VTAL_bddpx02.xlsx",
    "Levantamento_JETL_VTAL_gc_jetlpx01.xlsx"
]

# Dicionário para armazenar os DataFrames resultantes
dataframes_filtrados = {}

# Processar cada arquivo
for arquivo in arquivos:
    df_jobs = ler_colunas_jobs(arquivo)
    df_outros = filtrar_outros_jobs(df_jobs)
    
    if df_outros is not None:
        nome_df = f"df_{extrair_nome_dataframe(arquivo)}"
        dataframes_filtrados[nome_df] = df_outros
        print(f"\nResultados para {arquivo} armazenados como {nome_df}:")
        print(df_outros.head())  # Exibir as primeiras linhas

# Exemplo: Acessando um dos DataFrames filtrados
print(dataframes_filtrados["df_bddpx01"])
print(dataframes_filtrados["df_bddpx02"])
print(dataframes_filtrados["df_jetlpx01"])

print("")

nome, resultado = comparar_jobs(dataframes_filtrados["df_bddpx01"], dataframes_filtrados["df_jetlpx01"], "bddpx01", "df_jetlpx01")
print(f"{nome}:")
print(resultado)

dataframes_filtrados[nome] = resultado

print("")

nome, resultado = comparar_jobs(dataframes_filtrados["df_bddpx02"], dataframes_filtrados["df_jetlpx01"], "bddpx02", "df_jetlpx01")
print(f"{nome}:")
print(resultado)

dataframes_filtrados[nome] = resultado

# Salvar todos os DataFrames em arquivos Excel
for nome_df, df in dataframes_filtrados.items():
    df.to_excel(f"{nome_df}.xlsx", index=False)
    print(f"DataFrame {nome_df} salvo como {nome_df}.xlsx")