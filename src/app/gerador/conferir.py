import sys
from resultados.resultado import CachedResultadosClient

numeros = []
arquivos = []

usar_resultado = False
loteria = None
concurso = None
rateio = None

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
    print(res)
    numeros = list(res.iterate())
    rateio = res.rateio

for arquivo in arquivos:
    acertos = {}
    premio_total: float = 0.0
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
        print(f"acertos: {e[0]} - qtde: {e[1]}", end="")
        if rateio:
            for faixa in rateio:
                if str(e[0]) in faixa['descricaoFaixa'].split(" "):
                    premio = faixa['valorPremio'] * e[1]
                    premio_total += premio
                    print(f" - rateio: R$ {premio:.02f}", end="")
        print()

    if rateio:
        print(f"\nPremio total: R$ {premio_total:.02f}\n\n")
