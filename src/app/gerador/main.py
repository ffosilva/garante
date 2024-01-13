import random

qtde_cartoes = 10
tamanho_cartao = 6
maior_dezena = 60


def gerar_numeros(maior_dezena):
    numeros = [i for i in range(1, maior_dezena + 1)]
    random.shuffle(numeros)

    return numeros[0:6]

total_cartoes = 0
numeros = gerar_numeros(maior_dezena)


