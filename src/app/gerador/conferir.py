import sys
from resultados.resultado import CachedResultadosClient

numeros = []
arquivos = []

usar_resultado = False
loteria = None
concurso = None

for arg in sys.argv[1:]:
    if "last-" in arg:
        arg = arg.split("-")
        usar_resultado = True
        loteria = arg[1]
        continue

    if "res-" in arg:
        arg = arg.split("-")
        concurso = int(arg[2])
        loteria = arg[1]
        usar_resultado = True
        continue

    if arg.isdigit():
        numeros.append(int(arg))
    else:
        arquivos.append(arg)

print(numeros)
print(arquivos)

if usar_resultado:
    client = CachedResultadosClient(loteria)
    res = client.get_resultado(concurso)
    numeros = list(res.iterate())
    print(numeros)

for arquivo in arquivos:
    acertos = {}
    print(arquivo)
    with open(arquivo, 'r') as jogos_fd:
        for line in jogos_fd:
            jogo = list(map(int, line.split(";")))
            acertos_jogo = 0
            for dezena in numeros:
                if dezena in jogo:
                    acertos_jogo += 1
            acertos[acertos_jogo] = acertos.get(acertos_jogo, 0) + 1

    for e in dict(reversed(sorted(acertos.items()))).items():
        print(f"acertos: {e[0]} - qtde: {e[1]}")
