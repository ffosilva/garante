from typing import Hashable
from typing_extensions import Self

class Node:
    def __init__(self, value) -> None:
        self.value: Hashable = value
        self.adjacents: set[Self] = set()
    
    def __hash__(self) -> int:
        return self.value.__hash__()

    def __connect(self, node) -> None:
        self.adjacents.add(node)

    def connect(self, node) -> None:
        assert type(node) == Node
        self.__connect(node)
        node.__connect(self)

    def __disconnect(self, node) -> None:
        self.adjacents.remove(node)

    def disconnect(self, node) -> None:
        assert type(node) == Node
        self.__disconnect(node)
        node.__disconnect(self)

    def disconnect_all(self) -> None:
        for node in set(self.adjacents):
            node.disconnect(self)

    def adj_count(self) -> int:
        return len(self.adjacents)
