import networkx as nx
def graph_from_smiles_string(smiles_string):
    G = nx.Graph()
    B_1 = []
    smilesGraph = smiles(smiles_string)

    for v in smilesGraph.vertices:
        G.add_node(v.id,label = v.stringLabel)
    for e in smilesGraph.edges:
        G.add_edge(e.source.id,e.target.id)
        if e.bondType is BondType.Double:
            tmp = nx.Graph()
            tmp.add_edge(e.source.id,e.target.id)
            tmp.add_edge(e.target.id,e.source.id)
            B_1.append(tmp)
        if e.bondType is BondType.Triple:
            tmp = nx.Graph()
            tmp.add_edge(e.source.id,e.target.id)
            tmp.add_edge(e.target.id,e.source.id)
            B_1.append(tmp)
            B_1.append(tmp)
    return G, B_1

def is_simple_cycle(G):
    return len(G)-1 == len(set(G)) and G[0] == G[-1]

def get_shortest_paths(G):
    tmp = nx.shortest_path(G)
    shortest_paths = []
    for x in G.nodes:
        for path in tmp[x].values():
            shortest_paths.append(path)
    
    return shortest_paths

# Creates vector for edges
def edge_vector(G,subgraph):
    edges = list(G.edges)
    vector = [0]*len(edges)
    for edge in list(subgraph.edges):
        vector[edges.index(edge)] = 1
    return vector

def sublist(lst1, lst2):
    return all([(x in lst2) for x in lst1])

def is_subgraph(b, c):
    b_graph = nx.Graph()
    for cycle in b:
        b_graph = nx.compose(b_graph,cycle)
    return sublist(list(c.nodes),list(b_graph.nodes))

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
                            if len(subgraph.nodes) > 2 and is_simple_cycle(path1+path2):
                                cycles.append(subgraph)
    cycles = sorted(cycles, key=len)
    b = []
    i = 0

    while i < len(cycles):
        if not is_subgraph(b, cycles[i]):
            b.append(cycles[i])
        i+=1
    return b


def inference_invarient(MCB):
    length_two = []
    output = "|"
    tmp = MCB
    while tmp != []:
        next_cycle = tmp.pop(0)
        if len(next_cycle.edges) == 1:
            if tmp[0] == next_cycle:
                output+="2,2|"
                tmp.pop(0)
            else:
                output+="2e|"
            length_two.append(list(next_cycle.edges)[0])
            
        else:
            size = len(next_cycle.edges)
            e  = "e" if set(length_two).isdisjoint(set(next_cycle.edges)) else ""
            output+=str(size)+ e + "|"
    return output

strings = ["CC(=C)C(=O)OC12CC3CC(C1)CC(C3)C2",
    'CN1CNC2C1C(=O)N(C(=O)N2C)C',
    "OC(=O)C1CCCCC1NC5CCC(CC34CC2CC(CC(C2)C3)C4)CC5",
    "C1CCC23CCN(C(C2C1)CC4=C3C=C(C=C4)O)CC(=O)C5=CC=CC=C5", 
    "C12CC3(CC(C1)CC(C2)C3)CC4=CC=C(C=C4)NC5=C(C=CC=C5)C(O)=O",
    "C1=CC(=CC=C1C(CC(C2=CC=CC=C2)(C3=CC=CC=C3)O)NCC)OC",
    "C1(=CC=CC=C1)C(C2=CC=C(C(=C2)C)C)(C#C)OC(NC3CCCCC3)=O",
    ]
G, B_1 = graph_from_smiles_string(strings[6])
#B_1 are the cycles from dobbelt and triple bonds that we prune in the preprocessing, it is a list of MultiGraphs to represent them better
#G is a simple graph that does not have any dobbelt or triple bonds
B_0 = horton(G)

# MCB is the union of B_0 and B_1
MCB = B_1 + B_0
for cycle in MCB:
    print(cycle.edges)
print(inference_invarient(MCB))