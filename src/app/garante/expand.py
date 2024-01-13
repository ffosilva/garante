import sys
import os

matriz_path = sys.argv[1]
numeros_path = sys.argv[2]

matriz = []

def converte(aposta_matriz, numeros):
    ret = []
    for pos in aposta_matriz:
        ret.append(numeros[pos - 1])

    return ret

with open(matriz_path) as matriz_fd:
    for line in matriz_fd:
        line = line.strip().split(';')
        matriz.append(list(map(int, line)))

with open(numeros_path) as numeros_fd:
    for line in numeros_fd:
        line = line.strip().split(';')
        numeros = list(map(int, line))

        for aposta in matriz:
            print(";".join(list(map(str, converte(aposta, numeros)))))
