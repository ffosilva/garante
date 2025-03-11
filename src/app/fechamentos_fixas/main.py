import sys

from core.cartao import Cartao
from itertools import combinations

def parse_args():
    if len(sys.argv) < 3:
        print("Usage: python main.py <num. dezenas cartao> <maior dezena> [dezenas fixas]")
        sys.exit(1)

    return list(map(int, sys.argv[1:]))


if __name__ == "__main__":
    args = parse_args()
    
    tamanho_cartao, maior_dezena = args[0], args[1]

    dezenas_fixas = args[2:]
    qtde_fixas = len(dezenas_fixas)

    todas_dezenas = [i for i in range(1, maior_dezena + 1)]

    for dezena_fixa in dezenas_fixas:
        todas_dezenas.remove(dezena_fixa)

    restante = tamanho_cartao - qtde_fixas

    for comb in combinations(todas_dezenas, restante):
        cartao = Cartao(set(comb).union(set(dezenas_fixas)))
        print(cartao.to_string(";"))
