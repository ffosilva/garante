from typing import Iterable
from resultados.resultado import CachedResultadosClient
from core.posicao import posicao
from core.cartao import Cartao
from itertools import combinations
from multiprocessing import Lock, Process, Value
from core.filters import FilterChain, ClustersFilter, BlockListFilter
from math import inf
import random
import numpy as np

def explode_garante(dezenas: Iterable[int], arquivo_matriz: str) -> Iterable[Cartao]:
    cartoes = set()
    dezenas = list(dezenas)
    random.shuffle(dezenas)

    with open(arquivo_matriz, "r") as matriz:
        for linha in matriz:
            linha = linha.strip()
            dezenas_cartao = map(int, linha.split(';'))
            
            c = Cartao(())
            for dezena in dezenas_cartao:
                c.add(dezenas[dezena - 1])
            
            cartoes.add(c)

    return cartoes


def gerar_combinacao_aleatoria(numero_de_dezenas: int, maior_dezena: int, menor_dezena:int = 1) -> Cartao:
    dezenas = set()

    while len(dezenas) < numero_de_dezenas:
        dezenas.add(random.randint(menor_dezena, maior_dezena))

    return Cartao(dezenas)

def gerar_anticartao(numero_de_dezenas: int, maior_dezena: int, menor_dezena:int = 1, dezenas: Iterable[int] = None) -> Cartao:
    dezenas = set(range(menor_dezena, maior_dezena + 1)) - set(dezenas)

    while len(dezenas) < numero_de_dezenas:
        dezena = random.randint(menor_dezena, maior_dezena)
        if dezena not in dezenas:
            dezenas.add(dezena)

    return Cartao(dezenas)


def main(lock, max_acertos, execution_file, foco, filter_chain: FilterChain):
    matriz_path = "../garante/matriz_18_15_14_15_24.csv"
    #matriz_path = "/app/src/app/garante/matriz_18_15_14_15_24.csv"

    qtde_dezenas = 18
    numero_de_geracoes = 4
    anticartoes_por_geracao = 0

    while True:
        apostas_set: set[Cartao] = set()
        jogos_originais: set[Cartao] = set()
        for _ in range(numero_de_geracoes):
            combinacao_aleatoria = list(gerar_combinacao_aleatoria(qtde_dezenas, 25, 1))
            jogos_originais.add(Cartao(combinacao_aleatoria))
            apostas_set = apostas_set.union(explode_garante(combinacao_aleatoria, matriz_path))
            for _ in range(anticartoes_por_geracao):
                anticartao = list(gerar_anticartao(qtde_dezenas, 25, 1, combinacao_aleatoria))
                jogos_originais.add(Cartao(anticartao))
                apostas_set = apostas_set.union(explode_garante(anticartao, matriz_path))

        apostas_set = list(filter(filter_chain.accepts, apostas_set))

        foco_encontrado = set()
        for aposta in apostas_set:
            for comb_foco in combinations(aposta.iterate(), foco):
                foco_encontrado.add(Cartao(comb_foco))

        write_output(jogos_originais, apostas_set, max_acertos, execution_file, lock, foco_encontrado)


def write_output(jogos_orignais, apostas_set, max_acertos, execution_file, lock, foco_encontrado):
    try:
        lock.acquire()

        if len(foco_encontrado) > max_acertos.value:
            max_acertos.value = len(foco_encontrado)

            print(execution_file)
            for jogo_original in jogos_orignais:
                print(jogo_original.to_string(" - "))

            with open(execution_file, "w") as f:
                for aposta in apostas_set:
                    f.write(aposta.to_string(";"))
                    f.write("\n")
                    # print(aposta.to_string(";"))
            print(len(foco_encontrado))
    finally:
        lock.release()


if __name__ == "__main__":
    lock = Lock()
    max_acertos = shared_int = Value('i', 0)
    execution_file = f"temp_{random.randint(1, 1000)}.txt"

    resultados_client = CachedResultadosClient("lotofacil")
    ultimo_resultado = resultados_client.get_resultado()

    block_filter = BlockListFilter()
    min_clusters, max_clusters = +inf, -inf
    clusters = []

    # calcular os clusters (min e max)
    for i in range(1, ultimo_resultado.concurso + 1):
        resultado = resultados_client.get_resultado(i)
        block_filter.add(resultado)
        min_clusters = min(min_clusters, resultado.num_clusters())
        max_clusters = max(max_clusters, resultado.num_clusters())
        clusters.append(resultado.num_clusters())

    cluster_filter = ClustersFilter(min_clusters, max_clusters)
    filter_chain = FilterChain([block_filter, cluster_filter])

    foco = 13

    processes = []
    for i in range(4):
        p = Process(target=main, args=(lock, max_acertos, execution_file, foco, filter_chain))
        p.start()
        processes.append(p)
    
    for p in processes:
        p.join()
    

