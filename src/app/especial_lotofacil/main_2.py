from typing import Iterable
from resultados.resultado import CachedResultadosClient
from core.posicao import posicao
from core.cartao import Cartao
from itertools import combinations
from multiprocessing import Lock, Process, Value
import random
import numpy as np

def explode_garante(dezenas: Iterable[int], arquivo_matriz: str) -> Iterable[Cartao]:
    cartoes = set()
    dezenas = list(dezenas)
    random.shuffle(dezenas)

    with open(arquivo_matriz, "r") as matriz:
        for linha in matriz:
            linha = linha.strip()
            dezenas_cartao = map(int, linha.split(';'))
            
            c = Cartao(())
            for dezena in dezenas_cartao:
                c.add(dezenas[dezena - 1])
            
            cartoes.add(c)

    return cartoes


def gerar_combinacao_aleatoria(numero_de_dezenas: int, maior_dezena: int, menor_dezena:int = 1) -> Cartao:
    dezenas = set()

    while len(dezenas) < numero_de_dezenas:
        dezenas.add(random.randint(menor_dezena, maior_dezena))

    return Cartao(dezenas)

def gerar_anticartao(numero_de_dezenas: int, maior_dezena: int, menor_dezena:int = 1, dezenas: Iterable[int] = None) -> Cartao:
    dezenas = set(range(menor_dezena, maior_dezena + 1)) - set(dezenas)

    while len(dezenas) < numero_de_dezenas:
        dezena = random.randint(menor_dezena, maior_dezena)
        if dezena not in dezenas:
            dezenas.add(dezena)

    return Cartao(dezenas)


def distancias(cartao: Cartao) -> Iterable[int]:
    return [cartao.distancia(1, 11),cartao.distancia(2, 12), cartao.distancia(3, 13), cartao.distancia(4, 14), cartao.distancia(5, 15)]


def main(lock, max_acertos, execution_file, todos_resultados):
    matriz_path = "/home/ffosilva/repos/ffosilva/garante/src/app/garante/matriz_18_15_14_15_24.csv"
    matriz_path = "/app/src/app/garante/matriz_18_15_14_15_24.csv"

    qtde_dezenas = 18
    numero_de_geracoes = 3
    anticartoes_por_geracao = 0

    foco = 11

    while True:
        apostas_set: set[Cartao] = set()
        jogos_orignais: set[Cartao] = set()
        for i in range(numero_de_geracoes):
            combinacao_aleatoria = list(gerar_combinacao_aleatoria(qtde_dezenas, 25, 1))
            jogos_orignais.add(Cartao(combinacao_aleatoria))
            apostas_set = apostas_set.union(explode_garante(combinacao_aleatoria, matriz_path))
            for j in range(anticartoes_por_geracao):
                anticartao = list(gerar_anticartao(qtde_dezenas, 25, 1, combinacao_aleatoria))
                jogos_orignais.add(Cartao(anticartao))
                apostas_set = apostas_set.union(explode_garante(anticartao, matriz_path))


        acertos = {}
        for aposta in apostas_set:
            for res in todos_resultados:
                qt_acertos = aposta.qtde_acertos(res)
                if qt_acertos >= 11:
                    acertos[qt_acertos] = acertos.get(qt_acertos, 0) + 1
        
        write_output(jogos_orignais, apostas_set, acertos, foco, max_acertos, execution_file, lock)


def write_output(jogos_orignais, apostas_set, acertos, foco, max_acertos, execution_file, lock):
    try:
        lock.acquire()

        if foco in acertos and acertos[foco] > max_acertos.value:
            max_acertos.value = acertos[foco]

            print(execution_file)
            for jogo_original in jogos_orignais:
                print(jogo_original.to_string(" - "))
            print(acertos)
            with open(execution_file, "w") as f:
                for aposta in apostas_set:
                    f.write(aposta.to_string(";"))
                    f.write("\n")
                    # print(aposta.to_string(";"))
    finally:
        lock.release()


if __name__ == "__main__":
    lock = Lock()
    max_acertos = shared_int = Value('i', 0)
    execution_file = f"temp_{random.randint(1, 1000)}.txt"
    client = CachedResultadosClient("lotofacil")

    ultimo_resultado = client.get_resultado()

    todos_resultados = set()
    todos_resultados.add(ultimo_resultado)
    for i in range(1, ultimo_resultado.concurso):
        todos_resultados.add(client.get_resultado(i))

    processes = []
    for i in range(4):
        p = Process(target=main, args=(lock, max_acertos, execution_file, todos_resultados))
        p.start()
        processes.append(p)
    
    for p in processes:
        p.join()
    

