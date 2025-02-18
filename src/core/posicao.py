from core.cartao import Cartao
from itertools import combinations


__CACHE = {}

def posicao(cartao: Cartao, maior_dezena: int) -> int:
    num_dezenas = len(cartao)
    key = (maior_dezena, num_dezenas)

    if key not in __CACHE:
        __CACHE[key] = {}        

        for idx, comb in enumerate(combinations(range(1, maior_dezena + 1), num_dezenas), 1):
            __CACHE[key][hash(Cartao(comb))] = idx
        
        return __CACHE[key][hash(cartao)]
    else:
        return __CACHE[key][hash(cartao)]

if __name__ == "__main__":
    print(posicao(Cartao([1, 2, 3, 25, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]), 25))
    print(posicao(Cartao([1, 2, 3, 25, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]), 25))
