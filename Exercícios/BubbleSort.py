def bubble_sort(arr):
    n = len(arr)

    # Percorre todos os elementos do array
    for i in range(n):
        # Últimos i elementos já estão na posição correta
        for j in range(0, n-i-1):
            # Troca se o elemento encontrado é maior do que o próximo elemento
            if(arr[j] > arr[j+1]):
                arr[j], arr[j+1] = arr[j+1], arr[j]

    return arr

def corrige_indice(arr):
    n = len(arr)

    # Percorre todos os elementos do array
    for i in range(n):
        arr[i][0] = i + 1

    return arr

def elimina_item(arr):
    n = len(arr)

    # Percorre todos os elementos do array
    for i in range(n):
        if(i == 1 or i == 3):  
            arr[i][1] = 'N/A'

    return arr

# Declaração de um array 
meu_array = [[35,'John'],
             [98, 'Peter'],
             [23,'Mariah'],
             [43,'Bill'],
             [50,'Chris']]

print(meu_array)

meu_array_ordenado = bubble_sort(meu_array)
print(meu_array_ordenado)

meu_array_corrigido = corrige_indice(meu_array_ordenado)
print(meu_array_corrigido)

meu_array_NA = elimina_item(meu_array_corrigido)
print(meu_array_NA)