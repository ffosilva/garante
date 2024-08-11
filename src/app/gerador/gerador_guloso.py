from resultados.resultado import CachedResultadosClient
from core.cartao import Cartao
from random import shuffle
from itertools import combinations
from core.stats import *


if __name__ == "__main__":
    client = CachedResultadosClient("lotofacil")

    ultimo_resultado = client.get_resultado()
    numero_concurso = ultimo_resultado.concurso

    print(f"ultimo concuros: {numero_concurso}")

    num_cartoes = 100
    qtde_dezenas = 15
    maior_dezena = 25

    min_acertos = 8

    todos_resultados = set()
    for i in range(1, numero_concurso + 1):
        todos_resultados.add(client.get_resultado(i))

    maior_primeira = maior_primeira_dezena(todos_resultados)
    menor_ultima = menor_ultima_dezena(todos_resultados)
    clusters = qtde_clusters(todos_resultados)

    print(f"clusters: {clusters}")
