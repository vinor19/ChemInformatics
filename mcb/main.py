import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
def graph_from_smiles_string(smiles):
    G = nx.MultiGraph()
    smilesGraph = graphDFS(smiles)

    for v in smilesGraph.vertices:
        G.add_node(v.id)

    for e in smilesGraph.edges:
        G.add_edge(e.source.id,e.target.id)
        if e.bondType is BondType.Double:
            G.add_edge(e.source.id,e.target.id)
        if e.bondType is BondType.Triple:
            G.add_edge(e.source.id,e.target.id)
    return G

def is_simple_cycle(G):
    return len(G)-1 == len(set(G)) and G[0] == G[-1]

def get_shortest_paths(G):
    tmp = nx.shortest_path(G)
    shortest_paths = []
    for x in G.nodes:
        for path in tmp[x].values():
            shortest_paths.append(path)
    
    return shortest_paths

# def incidence_matrix(G, size):
#     matrix = [np.zeros(size)]*size
#     for (x,y,_) in G.edges:
#         matrix[x][y] = 1
#     return matrix

# def is_linear_independant(matrix1, matrix2):
#     sum = 0
#     for x in range(len(matrix1[0])):
#         for y in range(len(matrix1[0])):
#             sum += (matrix1[x][y] + matrix2[x][y])%2
#     return sum != 0
def sublist(lst1, lst2):
    return all([(x in lst2) for x in lst1])

def is_subgraph(b, c):
    b_graph = nx.MultiGraph()
    for cycle in b:
        b_graph = nx.compose(b_graph,cycle)
    return sublist(list(c.nodes),list(b_graph.nodes)) and sublist(list(c.edges), list(b_graph.edges))

def horton(G):
    shortest_paths = nx.shortest_path(G)
    cycles = []
    for z in G.nodes:
        if z in shortest_paths.keys():
            for e in G.edges:
                if e[0] in shortest_paths[z].keys():
                    path1 = shortest_paths[z][e[0]]
                    if e[1] in shortest_paths.keys():
                        if z in shortest_paths[e[1]].keys():
                            path2 = shortest_paths[e[1]][z]
                            subgraph = G.subgraph(path1+path2)
                            if len(subgraph.nodes) > 2 and nx.is_simple_path(G,path1+path2[:-1]):
                                cycles.append(subgraph)
    cycles = sorted(cycles, key=len)

    b = []
    i = 0

    while i < len(cycles):
        if not is_subgraph(b, cycles[i]):
            b.append(cycles[i])
        i+=1
    return b

strings = ["CC(=C)C(=O)OC12CC3CC(C1)CC(C3)C2",'CN1CNC2C1C(=O)N(C(=O)N2C)C',"OC(=O)C1CCCCC1NC5CCC(CC34CC2CC(CC(C2)C3)C4)CC5"]
G = graph_from_smiles_string(strings[0])
cycles = horton(G)
for cycle in cycles:
    print(cycle.nodes,cycle.edges)