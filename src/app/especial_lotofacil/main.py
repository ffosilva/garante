from typing import Iterable
from resultados.resultado import CachedResultadosClient
from core.posicao import posicao
from core.cartao import Cartao
from itertools import combinations
import random

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


def gerar_combinacao_aleatoria(numero_de_dezenas: int, maior_dezena: int) -> Cartao:
    dezenas = set()

    while len(dezenas) < numero_de_dezenas:
        dezenas.add(random.randint(1, maior_dezena))

    return Cartao(dezenas)


if __name__ == "__main__":
    client = CachedResultadosClient("lotofacil")
    matriz_path = "/home/ffosilva/repos/ffosilva/garante/src/app/garante/matriz_18_15_14_15_24.csv"

    resultado = client.get_resultado()

    todos_resultados = set()
    todos_resultados.add(resultado)
    for i in range(1, resultado.concurso):
        todos_resultados.add(client.get_resultado(i))

    numero_de_cartoes = 10
    foco = 11

    max_combinacoes = 0
    while True:
        apostas_set: set[Cartao] = set()
        for i in range(numero_de_cartoes):
            combinacao_aleatoria = list(gerar_combinacao_aleatoria(18, 25))
            apostas_set = apostas_set.union(explode_garante(combinacao_aleatoria, matriz_path))

        combinacoes = set()
        for aposta in apostas_set:
            combinacoes_local = combinations(aposta, foco)
            for combinacao in combinacoes_local:
                combinacoes.add(Cartao(combinacao))

        num_combinacoes = len(combinacoes)
        if num_combinacoes > max_combinacoes:
            print("====================================")
            print(f"Nova máxima: {num_combinacoes}")
            max_combinacoes = max(max_combinacoes, num_combinacoes)
            acertos = {}
            with open("temp.txt", "w") as f:
                for aposta in apostas_set:
                    f.write(aposta.to_string(";"))
                    f.write("\n")
                    print(aposta.to_string(";"))
                    for res in todos_resultados:
                        qt_acertos = aposta.qtde_acertos(res)
                        if qt_acertos >= 11:
                            acertos[qt_acertos] = acertos.get(qt_acertos, 0) + 1
            print(acertos)
            print()
            print("====================================")
