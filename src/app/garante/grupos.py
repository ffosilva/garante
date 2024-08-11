from itertools import combinations
from typing import Iterable
from core.cartao import Cartao

def gerar_grupos(qtde_grupos: int, qtde_dezenas_grupo: int) -> list[list[int]]:
    grupos = []
    num = 1

    for i in range(qtde_grupos):
        grupo_da_vez = []
        for j in range(qtde_dezenas_grupo):
            grupo_da_vez.append(num)
            num += 1
    
        grupos.append(grupo_da_vez)
    
    return grupos


def incrementa_indices(indices: list[int], max_indices: list[int]):
    maior_indice = len(indices) - 1

    indices[maior_indice] += 1

    while True:
        if indices[maior_indice] > max_indices[maior_indice]:
            indices[maior_indice] = 0
            maior_indice -= 1
            indices[maior_indice] += 1
        else:
            break

def gera_cartao(grupos: list[list[int]], indice_atual: list[int], tam_comb: int, cartoes_processados: set[Cartao]):
    todas_dezenas = [grupo[indice] for grupo, indice in zip(grupos, indice_atual)]
    cartoes = combinations(todas_dezenas, tam_comb)
    for dezenas_cartao in cartoes:
        cartao = Cartao(dezenas_cartao)
        if cartao in cartoes_processados:
            continue
        cartoes_processados.add(cartao)
        yield cartao


def gerar_combinacoes(qtde_grupos: int, qtde_dezenas_grupo: int, tam_comb: int = None) -> Iterable[Cartao]:
    if tam_comb == None:
        tam_comb = qtde_grupos

    grupos = gerar_grupos(qtde_grupos, qtde_dezenas_grupo)
    max_indice_por_grupo = [(len(i) - 1) for i in grupos]
    indice_atual = [0 for _ in range(len(grupos))]

    cartoes_processados: set[Cartao] = set()

    while indice_atual != max_indice_por_grupo:
        for cartao in gera_cartao(grupos, indice_atual, tam_comb, cartoes_processados):
            yield cartao
        incrementa_indices(indice_atual, max_indice_por_grupo)

    for cartao in gera_cartao(grupos, indice_atual, tam_comb, cartoes_processados):
        yield cartao        


if __name__ == "__main__":
    for cartao in gerar_combinacoes(6, 4, 3):
        print(cartao)
