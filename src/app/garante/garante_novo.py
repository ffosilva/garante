from itertools import combinations
from core.cartao import Cartao

quantidade_dezenas = 15
garante = 5
acertando = 6
tamanho_cartao = 6

todas_combinacoes = combinations(range(1, quantidade_dezenas + 1), tamanho_cartao)

cartoes_garante = list(combinations(range(1, quantidade_dezenas + 1), garante))
