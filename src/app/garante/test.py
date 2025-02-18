from pyomo.environ import ConcreteModel, Var, Objective, ConstraintList, SolverFactory, Binary, NonNegativeReals, UnitInterval
from itertools import combinations

def fechamento_mega_sena(numeros, tamanho_aposta, garantia, acertados):
    """
    Gera um fechamento otimizado para a Mega-Sena usando Pyomo.

    :param numeros: Lista de números disponíveis (ex.: [1, 2, ..., 60]).
    :param tamanho_aposta: Quantidade de números por aposta (ex.: 6).
    :param garantia: Garantia de acertos no fechamento.
    :param acertados: Quantidade de números acertados no sorteio.
    :return: Solução com as apostas geradas.
    """
    model = ConcreteModel()

    # Variáveis: cada combinação potencial será representada por uma variável binária
    combinacoes = list(combinations(numeros, tamanho_aposta))
    model.x = Var(range(len(combinacoes)), domain=Binary)

    # Função objetivo: minimizar o número total de apostas
    model.obj = Objective(expr=sum(model.x[i] for i in range(len(combinacoes))), sense=1)

    # Restrições: garantir a cobertura mínima
    model.constraints = ConstraintList()
    for sorteio in combinations(numeros, acertados):
        for combinacao in combinations(sorteio, garantia):
            model.constraints.add(
                sum(model.x[i] for i, aposta in enumerate(combinacoes) if set(combinacao).issubset(aposta)) >= 1
            )

    # Resolver o problema
    solver = SolverFactory('glpk')  # Você pode usar outros solvers como 'glpk' ou 'gurobi'
    result = solver.solve(model, tee=True)

    # Coletar as apostas geradas
    apostas = [combinacoes[i] for i in range(len(combinacoes)) if model.x[i].value == 1]
    return apostas

# Exemplo de uso
if __name__ == "__main__":
    qtde_dezenas = 12
    tamanho_aposta = 6           # Cada aposta tem 6 números
    garantia = 5                 # Garantia de 5 acertos
    acertados = 5                # Considerando 5 números sorteados
    numeros = list(range(1, qtde_dezenas + 1))  # Seleção de 12 dezenas

    apostas_geradas = fechamento_mega_sena(numeros, tamanho_aposta, garantia, acertados)

    print(f"Quantidade de apostas geradas: {len(apostas_geradas)}")
    for aposta in apostas_geradas:
        print(aposta)

