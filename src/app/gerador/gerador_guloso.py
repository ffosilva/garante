from resultados.resultado import CachedResultadosClient
from core.cartao import Cartao
from random import shuffle
from itertools import combinations
from core.stats import *
from app.gerador.globo import Globo

if __name__ == "__main__":
    client = CachedResultadosClient("lotofacil")

    ultimo_resultado = client.get_resultado()
    numero_concurso = ultimo_resultado.concurso

    print(f"ultimo concuros: {numero_concurso}")

    num_cartoes = 20
    qtde_dezenas = 6
    maior_dezena = 60
    alvo = 6

    todos_resultados = set()
    for i in range(1, numero_concurso + 1):
        cartao = client.get_resultado(i)
        if cartao in todos_resultados:
            print(f"Cartao repetido: {cartao}")
        todos_resultados.add(cartao)

    maior_primeira = maior_primeira_dezena(todos_resultados)
    menor_ultima = menor_ultima_dezena(todos_resultados)
    clusters = qtde_clusters(todos_resultados)

    print(f"clusters: {clusters}")

    max_combinacoes_alvo = 0
    while True:
        globo = Globo(maior_dezena)
        cartoes = set()
        while len(cartoes) < num_cartoes:
            cartoes.add(globo.gerar_cartao(qtde_dezenas))
        
        combinacoes_alvo = set()
        for cartao in cartoes:
            for combinacao in combinations(cartao.iterate(), alvo):
                combinacoes_alvo.add(combinacao)

        if len(combinacoes_alvo) > max_combinacoes_alvo:
            max_combinacoes_alvo = len(combinacoes_alvo)
            print(f"Grupos de {alvo}: {max_combinacoes_alvo}")
            for cartao in cartoes:
                print(cartao)
