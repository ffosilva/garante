#encoding: utf-8

import numpy as np
import logging

from random import Random
from typing import Optional, List, Iterator
from app.garante.utils import gerar_combinacoes, current_milli_time
from core.cartao import Cartao


def garante(todas_combinacoes_generator: Iterator[Cartao], combinacoes_garante_generator: Iterator[Cartao], garante: int, seed: Optional[int] = None, force_random: Optional[bool] = False) -> List[Cartao]:
    logger = logging.getLogger(__name__)

    progresso_grafo = 0
    progresso_processamento = 0

    combinacoes_cartoes = list(todas_combinacoes_generator)
    logger.info("Foram gerados {:d} cartões.".format(len(combinacoes_cartoes)))

    combinacoes_garante = list(combinacoes_garante_generator)
    total_combinacoes_garante = len(combinacoes_garante)
    logger.info("Foram geradas {:d} combinações.".format(total_combinacoes_garante))

    if seed is not None or force_random:
        rnd = Random(seed)
        rnd.shuffle(combinacoes_cartoes)
        rnd.shuffle(combinacoes_garante)

    logger.info("Iniciando geração do grafo.")

    start_time = current_milli_time()
    for i in range(len(combinacoes_cartoes)):
        progresso_grafo = ((i + 1)/len(combinacoes_cartoes)) * 100
        for j in range(len(combinacoes_garante)):
            if combinacoes_cartoes[i].value.qtde_acertos(combinacoes_garante[j].value) >= garante:
                combinacoes_cartoes[i].connect(combinacoes_garante[j])
    end_time = current_milli_time()

    logger.info(f"Geração do grafo finalizada. Duração: {(end_time - start_time) / 1000}s")

    cartoes_escolhidos = []

    total_inicial = None

    logger.info("Iniciando processamento.")
    start_time = current_milli_time()

    while True:
        acertos_cartoes_n = [0 for i in range(len(combinacoes_cartoes))]

        total_acertos_cartoes_n = 0

        for i in range(len(combinacoes_cartoes)):
            acertos_cartoes_n[i] = combinacoes_cartoes[i].adj_count()
            total_acertos_cartoes_n += combinacoes_cartoes[i].adj_count()
        
        if total_inicial is None:
            total_inicial = total_acertos_cartoes_n

        if len(acertos_cartoes_n) == 0 or max(acertos_cartoes_n) == 0:
            break

        max_index = int(np.argmax(acertos_cartoes_n))
        cartao_escolhido = combinacoes_cartoes.pop(max_index)
        cartoes_escolhidos.append(cartao_escolhido)
        for e in set(cartao_escolhido.adjacents):
            e.disconnect_all()

    end_time = current_milli_time()
    logger.info(f"Processamento finalizado. Duração: {(end_time - start_time) / 1000}s")

    logger.info(f"Conferência iniciada.")

    for cartao_da_vez in combinacoes_garante:
        encontrado = False
        for cartao in cartoes_escolhidos:
            if cartao_da_vez.value.qtde_acertos(cartao.value) >= garante:
                encontrado = True
                break
        assert encontrado

    logger.info(f"Conferência finalizada.")

    ret: List[Cartao] = list()
    for e in cartoes_escolhidos:
        ret.append(e.value)

    logger.info(f"Foram escolhidos {len(ret)} cartões.")

    return ret
