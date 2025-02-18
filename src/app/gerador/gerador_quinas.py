from core.cartao import Cartao
from itertools import combinations
from resultados.resultado import CachedResultadosClient, Resultado

from app.gerador.globo import Globo

foco = 4
foco_str = "quadra"
input_files = ["jogo-6.csv", "jogo-7.csv", "jogo-8.csv", "jogo-idesti.csv"]
resultados_client = CachedResultadosClient("megasena")

ultimo_resultado = resultados_client.get_resultado()
print("Último concurso ", ultimo_resultado.concurso)

todos_alvos = set()

# todas as quadras
for comb in combinations(range(1, 61), foco):
    todos_alvos.add(Cartao(comb))

print(f"{foco_str.capitalize()} geradas: ", len(todos_alvos))

alvos_jogados = set()
alvos_repetidos = 0

for input_file in input_files:
    for line in open(input_file):
        dezenas = [int(dezena) for dezena in line.split(";")]
        for comb in combinations(dezenas, foco):
            alvo_jogado = Cartao(comb)
            if alvo_jogado in alvos_jogados:
                alvos_repetidos += 1
            alvos_jogados.add(Cartao(comb))

print(f"{foco_str.capitalize()}s jogadas: ", len(alvos_jogados))
print(f"{foco_str.capitalize()}s repetidas: ", alvos_repetidos)

quinas_resultados: set[Resultado] = set()

min_clusters = float("inf")
max_clusters = 0

all_clusters = {}
all_lincols = {}

for concurso in range(1, ultimo_resultado.concurso + 1):
    resultado = resultados_client.get_resultado(concurso)

    for comb in combinations(resultado.iterate(), foco):
        quina_resultado = Cartao(comb)
        clusters = quina_resultado.num_clusters()
        min_clusters = min(min_clusters, clusters)
        max_clusters = max(max_clusters, clusters)

        all_clusters[clusters] = all_clusters.get(clusters, 0) + 1

        lin_col = quina_resultado.lin_col()        
        all_lincols[lin_col] = all_lincols.get(lin_col, 0) + 1

        quinas_resultados.add(quina_resultado)

print(f"{foco_str.capitalize()}s resultados: ", len(quinas_resultados))

print(min_clusters, max_clusters)
print(all_clusters)
print(all_lincols)

globo = Globo(60)

novas_apostas = 100
max_novidades = 0

input()

while True:
    novas_quadras = set()
    novidades = 0
    novos_cartoes = set()

    skip = False
    for i in range(novas_apostas):
        cartao = globo.gerar_cartao(6)
        for comb in combinations(cartao.iterate(), foco):
            quina = Cartao(comb)
            if quina in novas_quadras:
                skip = True
                break
            novas_quadras.add(quina)
            if quina not in alvos_jogados:
                novidades += 1
        novos_cartoes.add(cartao)

    if skip:
        continue

    if novidades > max_novidades:
        max_novidades = novidades
        print("Novidades: ", novidades, f"{foco_str.capitalize()}s: ", len(novas_quadras), "Cartões: ", len(novos_cartoes))
        for cartao in novos_cartoes:
            print(cartao)
