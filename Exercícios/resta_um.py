qtd_players = int(input('Informe número de participantes: '))
players = []
val_players = []
val_distrib_players = []
soma = 0

for i in range(0, qtd_players):
    players.append(input('Informe o nome do participante: '))
    val_players.append(int(input(f'Informe o valor para {players[i]}: ')))

for i in range(0, qtd_players):
    val_distrib_players.append(0)

print(players)
print(val_players)
print(len(val_distrib_players))

soma = sum(val_players)
print(soma)

i = 0
contador = 0

for i in range(0, soma):
    contador = i
    if contador == len(val_players):
        contador = 0

    val_distrib_players[contador] = i+1

    print(f'i:{i}; contador: {contador}; soma: {soma}; val_distrib_players[{contador}]: {i+1}')


print(contador)
print(val_distrib_players[contador])
