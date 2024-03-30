import sys

acertos = {}

resultado = list(map(int, sys.argv[2:]))

with open(sys.argv[1], 'r') as jogos_fd:
    for line in jogos_fd:
        jogo = list(map(int, line.split(";")))
        acertos_jogo = 0
        for dezena in resultado:
            if dezena in jogo:
                acertos_jogo += 1
        acertos[acertos_jogo] = acertos.get(acertos_jogo, 0) + 1

        if acertos_jogo >= 4:
            print(jogo)

print(acertos)
