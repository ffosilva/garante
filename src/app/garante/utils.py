import time

from core.cartao import Cartao
from typing import Iterator, Iterable
from itertools import combinations

from node import Node

def gerar_cartoes(qtde_dezenas: int, tamanho_cartao: int) -> Iterator[Cartao]:
    for comb in combinations(range(1, qtde_dezenas + 1), tamanho_cartao):
        yield Cartao(comb)


def gerar_combinacoes(qtde_dez, tam_comb) -> Iterable[Node]:
    combinador_cartoes = combinations([i for i in range(1, qtde_dez + 1)], tam_comb)
    for combinacao in combinador_cartoes:
        yield Node(Cartao(combinacao))


def current_milli_time():
    return round(time.time() * 1000)
