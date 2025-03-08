from abc import ABC, abstractmethod
from typing import Iterator, Iterable

from core.cartao import Cartao
from logging import getLogger

class Filter(ABC):
    @abstractmethod
    def accepts(self, cartao: Cartao) -> bool:
        pass


class FilterChain(Filter):
    def __init__(self, filters: Iterable[Filter]) -> None:
        self.filters = filters

    def accepts(self, cartao: Cartao) -> bool:
        return all(f.accepts(cartao) for f in self.filters)


class ClustersFilter(Filter):
    def __init__(self, min_clusters: int, max_clusters: int) -> None:
        self.min_clusters = min_clusters
        self.max_clusters = max_clusters

    def accepts(self, cartao: Cartao) -> bool:
        res = self.min_clusters <= cartao.num_clusters() <= self.max_clusters

        if not res:
            getLogger(__name__).debug(f"Rejeitado por clusters: {cartao}")
        
        return res


class BlockListFilter(Filter):
    cartoes: set[Cartao]

    def __init__(self, to_block: Iterable[Cartao] = None) -> None:
        if to_block is not None:
            self.cartoes = set(to_block)
        else:
            self.cartoes = set()

    def add(self, cartao: Cartao) -> None:
        self.cartoes.add(cartao)
    
    def remove(self, cartao: Cartao) -> None:
        self.cartoes.remove(cartao)

    def accepts(self, cartao: Cartao) -> bool:
        res = cartao not in self.cartoes
        
        if not res:
            getLogger(__name__).debug(f"Rejeitado por blocklist: {cartao}")
        
        return res
