#encoding: utf-8

import argparse
import numpy as np
import os
import sys

from itertools import combinations
from random import Random
from app.garante.node import Node
from core.cartao import Cartao
from unbuffered import Unbuffered
from typing import Iterable, Optional
from app_args import AppArgs

melhor_encontrado = float('inf')

def gerar_combinacoes(qtde_dez, tam_comb) -> Iterable[Node]:
    combinador_cartoes = combinations([i for i in range(1, qtde_dez + 1)], tam_comb)
    for combinacao in combinador_cartoes:
        yield Node(Cartao(combinacao))

    return


def parse_args() -> AppArgs:
    parser = argparse.ArgumentParser(description='GARANTE - Gerador de Combinações de Loteria')
    parser.add_argument('total_dezenas', type=int, help='quantidade de dezenas que se deseja jogar')
    parser.add_argument('tamanho_aposta', type=int, help='quantidade de dezeas das apostas que serão geradas')
    parser.add_argument('garante', type=int, help='quantidade de dezenas que se quer garantir')
    parser.add_argument('acertando', type=int, help='quantidade mínima de dezenas para garantir')
    parser.add_argument('caminho_saida', type=str, help='caminho para salvar o arquivo de saída')
    parser.add_argument('--random', type=int, help='valor da semente aleatória', required=False)

    args = parser.parse_args()

    return AppArgs(args.total_dezenas, args.tamanho_aposta, args.garante, args.acertando, args.caminho_saida, args.random)


def main(total_dezenas: int, tamanho_aposta: int, garante: int, acertando: int, caminho_saida: str, seed: Optional[int], ustdout: Unbuffered, force_random: bool = False):
    global melhor_encontrado

    try:
        assert os.path.isdir(caminho_saida)
    except AssertionError as e:
        print(f"Erro: '{caminho_saida}' não é um caminho válido.", file=ustdout)
        exit(1)
    else:
        nome_arquivo = "matriz_{:d}_{:d}_{:d}_{:d}".format(total_dezenas, tamanho_aposta, garante, acertando)

    # gerando combinações para escolher
    print("Gerando cartões para serem escolhidos ...", end=" ", file=ustdout)
    combinacoes_cartoes = list(gerar_combinacoes(total_dezenas, tamanho_aposta))
    print("Pronto!", file=ustdout)
    print("Foram gerados {:d} cartões.".format(len(combinacoes_cartoes)), file=ustdout)

    print("Gerando combinações que serão cobertas ...", end=" ", file=ustdout)
    combinacoes_garante = list(gerar_combinacoes(total_dezenas, acertando))
    total_combinacoes_garante = len(combinacoes_garante)
    print("Pronto!", file=ustdout)
    print("Foram geradas {:d} combinações.".format(total_combinacoes_garante),
        end="\n\n", file=ustdout)

    if seed is not None or force_random:
        rnd = Random(seed)
        rnd.shuffle(combinacoes_cartoes)
        rnd.shuffle(combinacoes_garante)

    for i in range(len(combinacoes_cartoes)):
        print("Gerando grafo ... Progresso: {:.2f} % \r".format(((i + 1)/len(combinacoes_cartoes)) * 100), end="", file=ustdout)
        for j in range(len(combinacoes_garante)):
            if combinacoes_cartoes[i].value.qtde_acertos(combinacoes_garante[j].value) >= garante:
                combinacoes_cartoes[i].connect(combinacoes_garante[j])
    print("Gerando grafo ... Pronto!            ", file=ustdout)

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

    if len(cartoes_escolhidos) < melhor_encontrado:
        melhor_encontrado = len(cartoes_escolhidos)
    else:
        print(f"Resultado melhor já encontrado.", file=ustdout)
        return    

    nome_arquivo += "_{:d}.csv".format(len(cartoes_escolhidos))
    saida_path = os.path.join(caminho_saida, nome_arquivo)

    if os.path.exists(saida_path):
        print(f"Arquivo de saída '{saida_path}' já existe.", file=ustdout)
        return

    arquivo_saida = open(saida_path, 'w')

    print("Conferindo jogo gerado...", file=ustdout)

    comb_checagem = list(gerar_combinacoes(total_dezenas, acertando))

    for cartao_da_vez in comb_checagem:
        encontrado = False
        for cartao in cartoes_escolhidos:
            if cartao_da_vez.value.qtde_acertos(cartao.value) >= garante:
                encontrado = True
                break
        assert encontrado

    print("Criando o arquivo '{}'...".format(nome_arquivo), file=ustdout)

    for e in cartoes_escolhidos:
        print(';'.join(map(str, map(int, e.value.iterate()))), file=arquivo_saida)

    print("Foram escolhidos {} cartões.".format(len(cartoes_escolhidos)), file=ustdout)
    arquivo_saida.close()

if __name__ == "__main__":
    appargs = parse_args()


    caminho_saida = appargs.caminho_saida
    total_dezenas = appargs.total_dezenas
    tamanho_aposta = appargs.tamanho_aposta
    garante = appargs.garante
    acertando = appargs.acertando
    seed = appargs.seed
    ustdout = Unbuffered(sys.stdout)

    main(total_dezenas, tamanho_aposta, garante, acertando, caminho_saida, seed, ustdout)
