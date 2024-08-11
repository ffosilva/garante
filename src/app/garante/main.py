from app.garante.core_functions import garante
from app.garante.utils import gerar_combinacoes, current_milli_time
from app.garante.grupos import gerar_combinacoes as gerar_combinacoes_grupos
from app.garante.node import Node

import logging


logging.basicConfig(level=logging.DEBUG)

total_dezenas = 18
tamanho_aposta = 15
acertando = 15

# todas_combinacoes_generator = gerar_combinacoes_grupos(total_dezenas, tamanho_aposta)
# combinacoes_garante_generator = gerar_combinacoes(total_dezenas, acertando)


quantidade_grupos = 6
dezenas_por_grupo = 4
garante_dezenas = 4
acertando = 4

todas_combinacoes_generator = map(Node, gerar_combinacoes_grupos(quantidade_grupos, dezenas_por_grupo))
combinacoes_garante_generator = map(Node, gerar_combinacoes_grupos(quantidade_grupos, dezenas_por_grupo, acertando))


for cartao in garante(todas_combinacoes_generator, combinacoes_garante_generator, garante_dezenas):
    print(cartao)
