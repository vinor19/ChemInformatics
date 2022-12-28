import networkx as nx

#Generates the Networkx graph representation of the smiles string, and returns subgraphs for MCB for double and triple bonds
def graph_from_smiles_string(smiles_string):
    G = nx.Graph()
    B_1 = []
    smilesGraph = smiles(smiles_string)

    for v in smilesGraph.vertices:
        G.add_node(v.id,label = v.stringLabel)
    for e in smilesGraph.edges:
        G.add_edge(e.source.id,e.target.id)
        if e.bondType is BondType.Double: #If double, add graph with the edge representing the double bond to B_1
            tmp = nx.Graph()
            tmp.add_edge(e.source.id,e.target.id)
            B_1.append(tmp)
        if e.bondType is BondType.Triple:  #If triple, add graph with the edge representing the double bond to B_1 twice
            tmp = nx.Graph()
            tmp.add_edge(e.source.id,e.target.id)
            B_1.append(tmp)
            B_1.append(tmp)
    return G, B_1

# If the path contains more or less nodes than path_length-1, and the first node and last node in the path is not the same, then it is not a simple cycle
def is_simple_cycle(G):
    return len(G)-1 == len(set(G)) and G[0] == G[-1]

# Creates vector for edges, would be used for gaussian elimination, but not using that
def edge_vector(G,subgraph):
    edges = list(G.edges)
    vector = [0]*len(edges)
    for edge in list(subgraph.edges):
        vector[edges.index(edge)] = 1
    return vector

# For simplicity, it's a subgraph if they contain the same nodes and edges, using set to simplify process since they are simple cycles
def is_subgraph(b, c):
    nodes, edges = [], []
    for cycle in b:
        nodes += list(cycle.nodes)
        edges += list(cycle.edges)
    return set(c.nodes).issubset(set(nodes)) and set(c.edges).issubset(set(edges))

# Hortons algorithms, takes a graph and returns the minimum cycle basis
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

#Takes a list of subgraphs that make up the MCB of a graph and returns a string representing the invariants
def inference_invarient(MCB):
    length_two = []
    output = "|"
    tmp = MCB
    while tmp != []:
        next_cycle = tmp.pop(0)
        if len(next_cycle.edges) == 1: # From double of triple bond
            if tmp[0] == next_cycle: # was triple bond
                output+="2,2|"
                tmp.pop(0) #Both are captured so need to pop the next as well
            else: # Was double bond
                output+="2e|" 
            length_two.append(list(next_cycle.edges)[0])
        else: # Standard
            size = len(next_cycle.edges)
            e  = "e" if set(length_two).isdisjoint(set(next_cycle.edges)) else "" # If there is a double bond in the cycle, it can't have an "e"
            output+=str(size)+ e + "|"
    return output

strings = ["CC(=C)C(=O)OC12CC3CC(C1)CC(C3)C2",
    'CN1CNC2C1C(=O)N(C(=O)N2C)C',
    "OC(=O)C1CCCCC1NC5CCC(CC34CC2CC(CC(C2)C3)C4)CC5",
    "C1CCC23CCN(C(C2C1)CC4=C3C=C(C=C4)O)CC(=O)C5=CC=CC=C5", # From figur 4.1
    "C12CC3(CC(C1)CC(C2)C3)CC4=CC=C(C=C4)NC5=C(C=CC=C5)C(O)=O", # From figur 4.2
    "C1=CC(=CC=C1C(CC(C2=CC=CC=C2)(C3=CC=CC=C3)O)NCC)OC", # From figur 4.3
    "C1(=CC=CC=C1)C(C2=CC=C(C(=C2)C)C)(C#C)OC(NC3CCCCC3)=O", # From figur 4.4
    ]
for i in range(3,7):
    G, B_1 = graph_from_smiles_string(strings[i])
    #B_1 are the cycles from dobbelt and triple bonds that we prune in the preprocessing, it is a list of MultiGraphs to represent them better
    #G is a simple graph that does not have any dobbelt or triple bonds
    B_0 = horton(G)

    # MCB is the union of B_0 and B_1
    MCB = B_1 + B_0
    # for cycle in MCB:
    #     print(cycle.edges)
    print(inference_invarient(MCB))