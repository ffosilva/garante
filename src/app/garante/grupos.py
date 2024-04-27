from itertools import combinations
from typing import Iterable
from app.garante.node import Node
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

def gerar_combinacoes(qtde_grupos, qtde_dezenas_grupo, tam_comb) -> Iterable[Node]:
    grupos = gerar_grupos(qtde_grupos, qtde_dezenas_grupo)
    max_indice_por_grupo = [(len(i) - 1) for i in grupos]
    indice_atual = [0 for _ in range(len(grupos))]

    while indice_atual != max_indice_por_grupo:
        yield Cartao([grupo[indice] for grupo, indice in zip(grupos, indice_atual)])
        incrementa_indices(indice_atual, max_indice_por_grupo)

    yield Cartao([grupo[indice] for grupo, indice in zip(grupos, indice_atual)])        


if __name__ == "__main__":
    for cartao in gerar_combinacoes(6, 4, 6):
        print(cartao)
