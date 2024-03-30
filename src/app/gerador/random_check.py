import random


def gerar_numeros_unitario(maior_dezena):
    numeros = [i for i in range(1, maior_dezena + 1)]
    random.shuffle(numeros)

    return [tuple(sorted(numeros[0:6]))]


def gerar_numeros_varios(maior_dezena):
    numeros = [i for i in range(1, maior_dezena + 1)]
    random.shuffle(numeros)

    while len(numeros) >= 6:
        cartao = []
        for i in range(6):
            cartao.append(numeros.pop())
        yield tuple(sorted(cartao))

resultado = (21, 24, 33, 41, 48, 56)

escolhidos_unitarios = set()

escolhidos_varios = set()
qtde_acertos_varios = {}


def rodar_jogo(fun):
    rateio = {}
    encontrado = False
    qtde = 0
    while not encontrado:
        for cartao in fun(60):
            qtde += 1
            acertos_jogo = 0
            for dezena in cartao:
                if dezena in resultado:
                    acertos_jogo += 1
            rateio[acertos_jogo] = rateio.get(acertos_jogo, 0) + 1

            if acertos_jogo >= 6:
                encontrado = True
                break
    print(qtde)
    print(rateio)

# rodar_jogo(gerar_numeros_unitario)
rodar_jogo(gerar_numeros_varios)
