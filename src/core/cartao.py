import math

from typing_extensions import Self
from typing import Iterable, Optional


class Cartao:
    __bitmap: int = 0

    def __init__(self, numeros: Optional[Iterable[int]], bitmap: Optional[int] = None) -> None:
        if bitmap is not None:
            self.__bitmap = bitmap
            return

        for numero in numeros:
            self.__set_bit(numero)

    def conferir(self, cartao: Self) -> Self:
        acertos: int = cartao.__bitmap & self.__bitmap
        return Cartao(None, acertos)

    def __set_bit(self, bit):
        self.__bitmap |= (1 << bit)
        return self.__bitmap

    def __len__(self) -> int:
        return self.__bitmap.bit_count()

    # caught from: https://stackoverflow.com/questions/8898807/pythonic-way-to-iterate-over-bits-of-integer
    @staticmethod
    def __bits(bitmap):
        while bitmap:
            b = bitmap & (~bitmap+1)
            yield math.log2(b)
            bitmap ^= b

    def to_string(self, separator: str):
        return separator.join([f"{num:02.0f}" for num in Cartao.__bits(self.__bitmap)])

    def __str__(self):
        return self.to_string(' - ')