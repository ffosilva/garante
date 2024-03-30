arquivo_entrada = "input.csv"
arquivo_jogo = "jogo_final.txt"

apostas = set()

with open(arquivo_entrada, 'r') as input_fd:
    for line in input_fd:
        line = line.strip().split(';')
        apostas.add(tuple(map(int, line)))

with open(arquivo_jogo, 'r') as jogo_fd:
    for line in jogo_fd:
        line = line.strip().split(';')
        aposta = tuple(map(int, line))
        assert aposta in apostas
        apostas.remove(aposta)

assert(len(apostas) == 0)
