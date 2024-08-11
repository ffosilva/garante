import networkx as nx

from app.garante.core_functions import garante
from app.garante.utils import gerar_cartoes
from app.garante.node import Node


def optimal_cut(graph, partition_a, partition_b):
    # Create a new directed graph for the flow network
    flow_network = nx.DiGraph()

    # Super-source and super-sink
    super_source = 'S'
    super_sink = 'T'

    # Add edges from super-source to all nodes in partition A
    for node in partition_a:
        flow_network.add_edge(super_source, node, capacity=float('inf'))
    
    # Add edges from all nodes in partition B to super-sink
    for node in partition_b:
        flow_network.add_edge(node, super_sink, capacity=1)
    
    # Add edges from partition A to partition B with original capacities
    for u in partition_a:
        for v in graph.successors(u):
            flow_network.add_edge(u, v, capacity=1)

    # Compute the maximum flow and the minimum cut
    flow_value, partition = nx.minimum_cut(flow_network, super_source, super_sink)
    reachable, non_reachable = partition

    # Find the nodes in partition A that need to be removed
    nodes_to_remove = [node for node in partition_a if node not in reachable]

    return nodes_to_remove, flow_value


total_dezenas = 18
tamanho_aposta = 15
acertando = 15

garante = 14

# Example usage
G = nx.DiGraph()
# Example bipartite edges from partition A to partition B
edges = []
partition_a = list(gerar_cartoes(total_dezenas, tamanho_aposta))
partition_b = list(gerar_cartoes(total_dezenas, acertando))

for i in range(len(partition_a)):
    for j in range(len(partition_b)):
        if partition_a[i].qtde_acertos(partition_b[j]) >= garante:
            edges.append((partition_a[i], partition_b[j]))

G.add_edges_from(edges)

# Find the optimal cut
nodes_to_remove, max_flow = optimal_cut(G, partition_a, partition_b)

print("Nodes to remove from partition A:", nodes_to_remove)
print("Maximum Flow:", max_flow)
