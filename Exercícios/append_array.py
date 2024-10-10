v =[]
continuar = "s"

while continuar == "s":
    try:
        n = int(input("Digite um valor: "))

        if n in v:
            print("Valor duplicado! Não vou adicionar...")
        else:
            v.append(n)
            print("Valor adicionado com sucesso...")
        continuar = str(input("Quer continuar? [S/N] ")).strip().lower()
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")
    
v.sort()
print(f"Você digitou os valores {v}")