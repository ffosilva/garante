import math

from typing_extensions import Self
from typing import Iterable, Optional


class Cartao:
    def __init__(self, numeros: Optional[Iterable[int]] = None, bitmap: Optional[int] = None) -> None:
        self.__bitmap: int = 0

        if bitmap is not None:
            self.__bitmap = bitmap
            return

        for numero in numeros:
            self.__set_bit(numero)

    def lin_col(self, largura = 10) -> tuple[int, int]:
        set_linhas = set()
        set_colunas = set()
    
        for dezena in self.iterate():
            set_linhas.add(int((dezena - 1) / largura))
            set_colunas.add(int(((dezena - 1) % largura) + 1))
        
        return (len(set_linhas), len(set_colunas))

    def conferir(self, cartao: Self) -> Self:
        acertos: int = cartao.__bitmap & self.__bitmap
        return Cartao(None, acertos)

    def qtde_acertos(self, cartao: Self) -> Self:
        acertos: int = cartao.__bitmap & self.__bitmap
        return acertos.bit_count()

    def __set_bit(self, bit):
        self.__bitmap |= (1 << bit)
        return self.__bitmap

    def __len__(self) -> int:
        return self.__bitmap.bit_count()

    # inspired on: https://stackoverflow.com/questions/8898807/pythonic-way-to-iterate-over-bits-of-integer
    @staticmethod
    def __bits(bitmap):
        while bitmap:
            b = bitmap & (~bitmap+1)
            yield math.log2(b)
            bitmap ^= b

    def to_string(self, separator: str) -> str:
        return separator.join([f"{num:02.0f}" for num in Cartao.__bits(self.__bitmap)])

    def iterate(self) -> Iterable[int]:
        return Cartao.__bits(self.__bitmap)
    
    def num_clusters(self) -> int:
        bitmap = self.__bitmap

        clusters = 0
        on_cluster = False
        while bitmap != 0:
            if bitmap & 1 == 1:
                if not on_cluster:
                    on_cluster = True
                    clusters += 1
            else:
                on_cluster = False

            bitmap >>= 1

        return clusters

    def min(self) -> int | None:
        if self.__bitmap == 0:
            return None
        
        return (self.__bitmap & -self.__bitmap).bit_length() - 1

    def max(self) -> int | None:
        if self.__bitmap == 0:
            return None

        return self.__bitmap.bit_length() - 1

    def __str__(self):
        return self.to_string(' - ')

    def __repr__(self):
        return f"Cartao([{', '.join([f"{num:.0f}" for num in Cartao.__bits(self.__bitmap)])}])"

    def __hash__(self) -> int:
        return self.__bitmap

    def __eq__(self, __value: object) -> bool:
        return type(__value) == Cartao and __value.__bitmap == self.__bitmap
