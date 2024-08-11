import random

qtde_cartoes = 3
tamanho_cartao = 18
maior_dezena = 25
#arquivo_entrada = 'numeros_entrada.csv'
arquivo_entrada = None

def numeros_entrada(arquivos_numeros: str):
    with open(arquivos_numeros, 'r') as numeros:
        nums = list(map(int, numeros.read().split(';')))
        random.shuffle(nums)
        
        return nums


def gerar_numeros(maior_dezena):
    numeros = [i for i in range(1, maior_dezena + 1)]
    random.shuffle(numeros)

    return numeros

if __name__ == "__main__":
    total_cartoes = 0

    if arquivo_entrada is not None:
        func = numeros_entrada
        argument = arquivo_entrada
    else:
        func = gerar_numeros
        argument = maior_dezena
    
    numeros = func(argument)

    cartoes = []

    while len(cartoes) < qtde_cartoes:
        cartao = set()
        while len(cartao) < tamanho_cartao:
            if len(numeros) == 0:
                numeros = func(argument)
            
            while numeros[-1] in cartao:
                random.shuffle(numeros)

            cartao.add(numeros.pop())

        cartoes.append(sorted(cartao))

    for cartao in cartoes:
        print(";".join(list(map(str, cartao))))
