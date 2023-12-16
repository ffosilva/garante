import itertools

from core.cartao import Cartao
from typing import Iterator


def gerar_cartoes(qtde_dezenas: int, tamanho_cartao: int) -> Iterator[Cartao]:
    for comb in itertools.combinations(range(1, qtde_dezenas + 1), tamanho_cartao):
        yield Cartao(comb)
