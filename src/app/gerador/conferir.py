import sys


numeros = []
arquivos = []

for arg in sys.argv[1:]:
    if arg.isdigit():
        numeros.append(int(arg))
    else:
        arquivos.append(arg)

print(numeros)
print(arquivos)

for arquivo in arquivos:
    acertos = {}
    print(arquivo)
    with open(arquivo, 'r') as jogos_fd:
        for line in jogos_fd:
            jogo = list(map(int, line.split(";")))
            acertos_jogo = 0
            for dezena in numeros:
                if dezena in jogo:
                    acertos_jogo += 1
            acertos[acertos_jogo] = acertos.get(acertos_jogo, 0) + 1

    for e in dict(reversed(sorted(acertos.items()))).items():
        print(f"acertos: {e[0]} - qtde: {e[1]}")
