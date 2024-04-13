from app.garante.core_functions import garante
import logging


logging.basicConfig(level=logging.DEBUG)

for cartao in garante(18, 15, 14, 15):
    print(cartao)
