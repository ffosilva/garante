from core.cartao import Cartao
from itertools import combinations
from resultados.resultado import CachedResultadosClient, Resultado

from app.gerador.globo import Globo

input_files = ["jogo-6.csv", "jogo-7.csv", "jogo-8.csv"]
resultados_client = CachedResultadosClient("megasena")

ultimo_resultado = resultados_client.get_resultado()
print("Último concurso ", ultimo_resultado.concurso)

quadras = set()

# todas as quadras
for comb in combinations(range(1, 61), 4):
    quadras.add(Cartao(comb))

print("Quadras geradas: ", len(quadras))

quadras_jogadas = set()

for input_file in input_files:
    for line in open(input_file):
        dezenas = [int(dezena) for dezena in line.split(";")]
        for comb in combinations(dezenas, 4):
            quadras_jogadas.add(Cartao(comb))

print("Quadras jogadas: ", len(quadras_jogadas))

quadras_resultados: set[Resultado] = set()

min_clusters = float("inf")
max_clusters = 0

all_clusters = {}

for concurso in range(1, ultimo_resultado.concurso + 1):
    resultado = resultados_client.get_resultado(concurso)
    clusters = resultado.num_clusters()
    min_clusters = min(min_clusters, clusters)
    max_clusters = max(max_clusters, clusters)

    all_clusters[clusters] = all_clusters.get(clusters, 0) + 1

    for comb in combinations(resultado.iterate(), 4):
        quadras_resultados.add(Cartao(comb))

print("Quadras resultados: ", len(quadras_resultados))

print(min_clusters, max_clusters)
print(all_clusters)

globo = Globo(60)

novas_apostas = 100
max_novidades = 0

while True:
    novas_quadras = set()
    novidades = 0
    novos_cartoes = set()

    skip = False
    for i in range(novas_apostas):
        cartao = globo.gerar_cartao(6)
        for comb in combinations(cartao.iterate(), 4):
            quadra = Cartao(comb)
            if quadra in novas_quadras:
                skip = True
                break
            novas_quadras.add(quadra)
            if quadra not in quadras_jogadas:
                novidades += 1
        novos_cartoes.add(cartao)

    if skip:
        continue

    if novidades > max_novidades:
        max_novidades = novidades
        print("Novidades: ", novidades, "Quadras: ", len(novas_quadras), "Cartões: ", len(novos_cartoes))
        for cartao in novos_cartoes:
            print(cartao)
