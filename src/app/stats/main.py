import math
import sys

from core.stats import maior_primeira_dezena, menor_ultima_dezena, qtde_acertos
from resultados.resultado import CachedResultadosClient
from core.cartao import Cartao

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(f"usage: python {sys.argv[0]} <nome da loteria>")
        exit(1)

    nome_loteria = sys.argv[1]
    client = CachedResultadosClient(nome_loteria)

    ultimo_resultado = client.get_resultado()
    numero_concurso = ultimo_resultado.concurso

    resultados: list[Cartao] = []

    print(f"Loteria: {nome_loteria} - Último concurso: {numero_concurso}")

    print("Carregando resultados... ", end="")
    for i in range(1, numero_concurso + 1):
        resultado = Cartao(list(map(int, client.get_resultado(i).iterate())))
        resultados.append(resultado)
    print("Pronto!")

    print(f"Menor ultima dezena: {menor_ultima_dezena(resultados)}")
    print(f"Maior primeira dezena: {maior_primeira_dezena(resultados)}")
    print(f"Quantidade de acertos entre cartões: {qtde_acertos(resultados)}")
