def progressao_aritmetica(valor_inicial, razao, valor_final):
    # Validando os valores recebidos
    if not isinstance(valor_inicial, (int, float)) or not isinstance(razao, (int, float)) or not isinstance(valor_final, (int, float)):
        raise ValueError("Os valores devem ser números inteiros ou decimais.")

    if razao == 0:
        raise ValueError("A razão não pode ser zero.")

    if valor_inicial > valor_final and razao > 0:
        raise ValueError("Se a razão for positiva, o valor inicial não pode ser maior que o valor final.")

    if valor_inicial < valor_final and razao < 0:
        raise ValueError("Se a razão for negativa, o valor inicial não pode ser menor que o valor final.")

    # Calculando a progressão aritmética
    atual = valor_inicial
    while atual <= valor_final:
        print(atual, end=' ')
        atual += razao

try:
    valor_inicial = float(input("Digite o valor inicial da progressão: "))
    razao = float(input("Digite a razão da progressão: "))
    valor_final = float(input("Digite o valor final da progressão: "))
    
    progressao_aritmetica(valor_inicial, razao, valor_final)

except ValueError as ve:
    print(f"Erro: {ve}")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")