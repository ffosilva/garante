from math import inf
from functools import reduce
from core.cartao import Cartao

def maior_primeira_dezena(cartoes: list[Cartao]) -> int:
    return reduce(lambda x, y: x if x.min() > y.min() else y, cartoes).min()

def menor_ultima_dezena(cartoes: list[Cartao]) -> int:
    return reduce(lambda x, y: x if x.max() < y.max() else y, cartoes).max()

def qtde_acertos(cartoes: list[Cartao]) -> tuple[int, int]:
    menor_qtde_acertos = +inf
    maior_qtde_acertos = -inf

    for i in range(len(cartoes)):
        for j in range(i + 1, len(cartoes)):
            maior_qtde_acertos = max(cartoes[i].qtde_acertos(cartoes[j]), maior_qtde_acertos)
            menor_qtde_acertos = min(cartoes[i].qtde_acertos(cartoes[j]), menor_qtde_acertos)

    return (menor_qtde_acertos, maior_qtde_acertos)
