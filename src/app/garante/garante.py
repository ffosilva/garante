#encoding: utf-8

import argparse
import numpy as np
import os
import sys

from itertools import combinations
from random import Random
from node import Node
from core.cartao import Cartao
from unbuffered import Unbuffered
from typing import Iterable

def gerar_combinacoes(qtde_dez, tam_comb) -> Iterable[Node]:
    combinador_cartoes = combinations([i for i in range(1, qtde_dez + 1)], tam_comb)
    for combinacao in combinador_cartoes:
        yield Node(Cartao(combinacao))

    return


parser = argparse.ArgumentParser(description='GARANTE - Gerador de Combinações de Loteria')
parser.add_argument('total_dezenas', type=int, help='quantidade de dezenas que se deseja jogar')
parser.add_argument('tamanho_aposta', type=int, help='quantidade de dezeas das apostas que serão geradas')
parser.add_argument('garante', type=int, help='quantidade de dezenas que se quer garantir')
parser.add_argument('acertando', type=int, help='quantidade mínima de dezenas para garantir')
parser.add_argument('caminho_saida', type=str, help='caminho para salvar o arquivo de saída')
parser.add_argument('--random', type=int, help='valor da semente aleatória', required=False)

args = parser.parse_args()
ustdout = Unbuffered(sys.stdout)

total_dezenas = args.total_dezenas
tamanho_aposta = args.tamanho_aposta
garante = args.garante
acertando = args.acertando
caminho_saida = args.caminho_saida
seed = args.random

arquivo_saida = None

try:
    assert os.path.isdir(caminho_saida)
except AssertionError as e:
    print("Erro: '{}' não é um caminho válido.".format(caminho_saida))
    exit(1)
else:
    nome_arquivo = "matriz_{:d}_{:d}_{:d}_{:d}".format(total_dezenas, tamanho_aposta, garante, acertando)

# gerando combinações para escolher
print("Gerando cartões para serem escolhidos ...", end=" ", file=ustdout)
combinacoes_cartoes = list(gerar_combinacoes(total_dezenas, tamanho_aposta))
print("Pronto!")
print("Foram gerados {:d} cartões.".format(len(combinacoes_cartoes)))

print("Gerando combinações que serão cobertas ...", end=" ", file=ustdout)
combinacoes_garante = list(gerar_combinacoes(total_dezenas, acertando))
total_combinacoes_garante = len(combinacoes_garante)
print("Pronto!")
print("Foram geradas {:d} combinações.".format(total_combinacoes_garante),
      end="\n\n")

if seed is not None:
    rnd = Random(seed)
    rnd.shuffle(combinacoes_cartoes)
    rnd.shuffle(combinacoes_garante)

for i in range(len(combinacoes_cartoes)):
    print("Gerando grafo ... Progresso: {:.2f} % \r".format(((i + 1)/len(combinacoes_cartoes)) * 100), end="", file=ustdout)
    for j in range(len(combinacoes_garante)):
        if combinacoes_cartoes[i].value.qtde_acertos(combinacoes_garante[j].value) >= garante:
            combinacoes_cartoes[i].connect(combinacoes_garante[j])
print("Gerando grafo ... Pronto!            ")

cartoes_escolhidos = []

total_inicial = None

while True:
    acertos_cartoes_n = [0 for i in range(len(combinacoes_cartoes))]

    total_acertos_cartoes_n = 0

    for i in range(len(combinacoes_cartoes)):
        acertos_cartoes_n[i] = combinacoes_cartoes[i].adj_count()
        total_acertos_cartoes_n += combinacoes_cartoes[i].adj_count()
    
    if total_inicial is None:
        total_inicial = total_acertos_cartoes_n

    print("Progresso: {:.2f} % \r".format((1 - (total_acertos_cartoes_n/total_inicial)) * 100), end="", file=ustdout)

    if len(acertos_cartoes_n) == 0 or max(acertos_cartoes_n) == 0:
        break

    max_index = int(np.argmax(acertos_cartoes_n))
    cartao_escolhido = combinacoes_cartoes.pop(max_index)
    cartoes_escolhidos.append(cartao_escolhido)
    for e in set(cartao_escolhido.adjacents):
        e.disconnect_all()


print("Conferindo jogo gerado...")

comb_checagem = list(gerar_combinacoes(total_dezenas, acertando))

for cartao_da_vez in comb_checagem:
    encontrado = False
    for cartao in cartoes_escolhidos:
        if cartao_da_vez.value.qtde_acertos(cartao.value) >= garante:
            encontrado = True
            break
    assert encontrado

nome_arquivo += "_{:d}.csv".format(len(cartoes_escolhidos))

print("Criando o arquivo '{}'...".format(nome_arquivo))
arquivo_saida = open(os.path.join(caminho_saida, nome_arquivo), 'w')

for e in cartoes_escolhidos:
    print(';'.join(map(str, map(int, e.value.iterate()))), file=arquivo_saida)

print("Foram escolhidos {} cartões.".format(len(cartoes_escolhidos)))
arquivo_saida.close()
