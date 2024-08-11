import pulp
from app.garante.utils import gerar_cartoes

def exact_set_cover(partition_a, partition_b, edges):
    # Create a linear programming problem
    problem = pulp.LpProblem("SetCover", pulp.LpMinimize)

    # Create a binary variable for each element in partition A
    x = pulp.LpVariable.dicts('x', partition_a, 0, 1, pulp.LpBinary)

    # Objective function: minimize the sum of selected nodes in partition A
    problem += pulp.lpSum(x[a] for a in partition_a), "Minimize selected nodes"

    # Constraints: each node in partition B must be covered by at least one node in partition A
    for b in partition_b:
        problem += pulp.lpSum(x[a] for a in partition_a if b in edges[a]) >= 1, f"Cover {b}"

    # Solve the problem
    problem.solve()

    # Extract the selected nodes in partition A
    selected = [a for a in partition_a if x[a].value() == 1]
    
    return selected

total_dezenas = 19
tamanho_aposta = 15
acertando = 15

garante = 14

partition_a = list(gerar_cartoes(total_dezenas, tamanho_aposta))
partition_b = list(gerar_cartoes(total_dezenas, acertando))

edges = {}
for i in range(len(partition_a)):
    edges[partition_a[i]] = set()
    for j in range(len(partition_b)):
        if partition_a[i].qtde_acertos(partition_b[j]) >= garante:
            edges[partition_a[i]].add(partition_b[j])

result = exact_set_cover(set(partition_a), set(partition_b), edges)
print("Selected nodes from partition A:", result)
