from core.cartao import Cartao
from resultados.resultado import CachedResultadosClient
from typing import Any


def calcular_surpresa(ultimas_chamadas, todas_chamadas, quantidade_dezenas) -> Cartao:
    dezenas_escolhidas = set()
    ultimas_chamadas_sorted = sorted(ultimas_chamadas, key=ultimas_chamadas.get, reverse=False)
    todas_chamadas_sorted = list(sorted(todas_chamadas, key=todas_chamadas.get, reverse=False))

    for key in ultimas_chamadas_sorted:
        if ultimas_chamadas[key] == 0:
            break
        dezenas_escolhidas.add(key)

        if len(dezenas_escolhidas) == quantidade_dezenas:
            break

    if len(dezenas_escolhidas) == quantidade_dezenas:
        ret = Cartao(dezenas_escolhidas)
        return ret

    while len(dezenas_escolhidas) < quantidade_dezenas:        
        dezenas_escolhidas.add(todas_chamadas_sorted.pop())

    ret = Cartao(dezenas_escolhidas)
    
    return ret


def calcular_antisurpresa(ultimas_chamadas, todas_chamadas, quantidade_dezenas, maior_dezena, surpresa = None) -> Cartao:
    if surpresa is None:
        surpresa = calcular_surpresa(ultimas_chamadas, todas_chamadas, quantidade_dezenas)
    todas_chamadas_sorted = list(sorted(todas_chamadas, key=todas_chamadas.get, reverse=True))

    anti_surpresa = set()
    for i in range(1, maior_dezena + 1):
        if i not in surpresa:
            anti_surpresa.add(i)

    while len(anti_surpresa) < quantidade_dezenas:        
        anti_surpresa.add(todas_chamadas_sorted.pop())

    return Cartao(anti_surpresa)


def carregar_matriz(filename: str) -> list[list[int]]:
    matriz = []

    with open(filename, 'r') as matriz_fp:
        for line in matriz_fp:
            line_map = map(int, line.strip().split(";"))
            matriz.append(list(line_map))
    
    return matriz


def preencher_matriz(matriz: list[list[int]], dezenas: Cartao) -> list[Cartao]:
    nova_matriz = []
    dezenas = list(dezenas)

    for cartao_matriz in matriz:
        numeros = []
        for idx in cartao_matriz:
            numeros.append(dezenas[idx - 1])
        nova_matriz.append(Cartao(numeros))
    
    return nova_matriz


def carregar_faixa(rateio: dict[str, Any], total_dezenas) -> dict[int, float]:
    faixa_acertos = {}
    for faixa in rateio:
        qtde_acertos = total_dezenas - (faixa["faixa"] - 1)
        faixa_acertos[qtde_acertos] = faixa["valorPremio"]

    return faixa_acertos

matriz_arquivo = carregar_matriz("matriz_18_15_14_15_24.csv")
nome_loteria = "lotofacil"
client = CachedResultadosClient(nome_loteria)

ultimo_resultado = client.get_resultado().concurso

ultimas_chamadas = {}
todas_chamadas = {}

maior_dezena = 25
menor_premiacao = 11
tamanho_surpresa = 18

todos_chamados = False

surpresa = None
anti_surpresa = None

saldo = 0.0

for i in range(1, ultimo_resultado + 1):
    resultado = client.get_resultado(i)
    for dezena in range(1, maior_dezena + 1):
        if dezena not in resultado:
            ultimas_chamadas[dezena] = ultimas_chamadas.get(dezena, 0) + 1

    print(f"Concurso {resultado.concurso}", end=" ")
    for numero in resultado:
        idade = ultimas_chamadas.get(numero, 0)
        ultimas_chamadas[numero] = 0
        todas_chamadas[numero] = todas_chamadas.get(numero, 0) + 1
        print(f" {numero:02d} [{idade:02d}]", end="")
    
    qtde_acertos = resultado.qtde_acertos(surpresa) if surpresa is not None else None
    if surpresa is not None:
        faixas_de_acertos = carregar_faixa(resultado.rateio, resultado.qtde_dezenas)
        custo_cartao = faixas_de_acertos[11] / 2
        custo_jogo = len(matriz_arquivo) * custo_cartao
        saldo -= custo_jogo
        matriz = preencher_matriz(matriz_arquivo, surpresa)
        for cartao in matriz:
            acertos = resultado.qtde_acertos(cartao)
            if acertos >= menor_premiacao:
                saldo += faixas_de_acertos[acertos]
        
        # matriz = preencher_matriz(matriz_arquivo, anti_surpresa)
        # for cartao in matriz:
        #     acertos = resultado.qtde_acertos(cartao)
        #     if acertos >= menor_premiacao:
        #         saldo += faixas_de_acertos[acertos]

    print()

    if not todos_chamados and len(todas_chamadas.keys()) >= maior_dezena:
        todos_chamados = True
    
    if todos_chamados:
        surpresa = calcular_surpresa(ultimas_chamadas, todas_chamadas, tamanho_surpresa)
        anti_surpresa = calcular_antisurpresa(ultimas_chamadas, todas_chamadas, tamanho_surpresa, maior_dezena, surpresa)
        
print(saldo)
print(surpresa)
anti_surpresa = calcular_antisurpresa(ultimas_chamadas, todas_chamadas, tamanho_surpresa, maior_dezena, surpresa)
print(anti_surpresa)

for i in range(3):
    print(anti_surpresa)
    anti_surpresa = calcular_antisurpresa(ultimas_chamadas, todas_chamadas, tamanho_surpresa, maior_dezena, anti_surpresa)
