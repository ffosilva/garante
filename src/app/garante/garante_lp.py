from pulp import LpMinimize, LpProblem, LpVariable, lpSum, listSolvers, COIN_CMD
import itertools
import random

def gerar_desdobramento(T, N, X, Y):
    cbc_path = "/opt/homebrew/opt/cbc/bin/cbc"

    # Conjunto base de T dezenas escolhidas aleatoriamente
    numeros_totais = list(range(1, 26))  # Números da Lotofácil (1 a 25)
    if T > 25 or T < N:
        raise ValueError("O valor de T deve estar entre N e 25.")
    
    random.seed(42)
    conjunto_base = numeros_totais[:T]
    print(f"Números escolhidos para o desdobramento: {sorted(conjunto_base)}")

    # Gerando todas as combinações possíveis de N números dentro do conjunto escolhido
    combinacoes_possiveis = list(itertools.combinations(conjunto_base, N))
    print(f"Total de combinações possíveis: {len(combinacoes_possiveis)}")

    # Criando um modelo de Programação Linear
    modelo = LpProblem(name="desdobramento_lotofacil", sense=LpMinimize)

    # Variáveis de decisão: Se a combinação faz parte do desdobramento ou não
    X_vars = {i: LpVariable(name=f"comb_{i}", cat="Binary") for i in range(len(combinacoes_possiveis))}

    # Amostragem limitada de subconjuntos de X e Y
    subconjuntos_X = random.sample(list(itertools.combinations(conjunto_base, X)), min(100, len(list(itertools.combinations(conjunto_base, X)))))
    subconjuntos_Y = random.sample(list(itertools.combinations(conjunto_base, Y)), min(50, len(list(itertools.combinations(conjunto_base, Y)))))

    # Garantir que cada subconjunto de tamanho X apareça pelo menos uma vez
    for subset in subconjuntos_X:
        modelo += lpSum(X_vars[i] for i in range(len(combinacoes_possiveis)) if all(num in combinacoes_possiveis[i] for num in subset)) >= 1, f"Cobertura_X_{subset}"

    # Garantir que subconjuntos de tamanho Y tenham boa distribuição nas apostas
    for subset in subconjuntos_Y:
        modelo += lpSum(X_vars[i] for i in range(len(combinacoes_possiveis)) if all(num in combinacoes_possiveis[i] for num in subset)) >= 1, f"Cobertura_Y_{subset}"

    # Função objetivo: Minimizar o número de apostas garantindo cobertura mínima necessária
    modelo += lpSum(X_vars[i] for i in range(len(combinacoes_possiveis))), "Minimizar_Apostas"

    # Resolvendo o problema usando CBC
    modelo.solve(COIN_CMD(path=cbc_path))

    # Extraindo as apostas selecionadas
    apostas_selecionadas = [combinacoes_possiveis[i] for i in range(len(combinacoes_possiveis)) if X_vars[i].value() == 1]

    # Exibindo o resultado
    print("\nApostas geradas:")
    for idx, aposta in enumerate(apostas_selecionadas, start=1):
        print(f"Aposta {idx}: {sorted(aposta)}")

    return apostas_selecionadas

# Exemplo de uso
T = 18  # Total de dezenas escolhidas
N = 15  # Tamanho das apostas
X = 14  # Número de acertos garantidos
Y = 14  # Acertos desejados no resultado

apostas = gerar_desdobramento(T, N, X, Y)
