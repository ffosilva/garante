import os
import sys

matriz_fp = open(sys.argv[1], 'r')
jogo_fp = open(sys.argv[2], 'r')

matriz = []
jogos = []

for line in matriz_fp:
    line = list(map(int, line.strip().split(";")))
    matriz.append(line)


for line in jogo_fp:
    line = list(map(int, line.strip().split(" - ")))
    jogos.append(line)

for jogo in jogos:
    for aposta in matriz:
        cartao = []
        for dezena in aposta:
            cartao.append(jogo[dezena - 1])
        
        print(";".join(list(map(str, cartao))))
