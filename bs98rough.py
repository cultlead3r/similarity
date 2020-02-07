# other imports
from mcs import maximum_common_induced_subgraph
import os
import networkx as nx
import matplotlib.pyplot as plt
import sys


# testing calculating bs98 with zel90 mcis
def distances(G1, G2, verbose=False):
    # suppress the print statements within MCIS call
    if verbose is not True:
        sys.stdout = open(os.devnull, 'w')

    if(len(G1) != len(G2)):
        return ("Error: Graphs must be of same size")

    N = len(G1)
    communs = maximum_common_induced_subgraph(G1, G2, 4, False, True)
    K = len(communs[0][0])
    contracDis = N - K

    bsd = (1-(len(communs[0][0])/max(len(G1), len(G2))))

    # re-enable output
    sys.stdout = sys.__stdout__
    return contracDis, bsd


# from stackoverflow, might work, seems to not be totally accurate
def mcs_distance2(G1, G2):
    matching_graph = nx.Graph()

    for e1, e2 in G2.edges():
        if G1.has_edge(e1, e2):
            matching_graph.add_edge(e1, e2, weight=1)

    # connected_component_subgraphs is DEPRECATED
    # graphs = list(connected_component_subgraphs(matching_graph))

    graphs = (matching_graph.subgraph(c) for c in nx.connected_components(matching_graph))

    mcs_length = 0
    mcs_graph = nx.Graph()
    for graph in enumerate(graphs):

        if len(graph.nodes()) > mcs_length:
            mcs_length = len(graph.nodes())
            mcs_graph = graph

    distance = (1-(len(mcs_graph)/(max(len(G1),len(G2)))))

    return distance


# brute force, not working correctly
def mcs_distance3(G1, G2):

    # connected_component_subgraphs is DEPRECATED
    # g1 = list(nx.connected_component_subgraphs(G1))
    # g2 = list(nx.connected_component_subgraphs(G2))
    g1 = (G1.subgraph(c) for c in nx.connected_components(G1))
    g2 = (G2.subgraph(c) for c in nx.connected_components(G2))

    # print(g1)

    possible_mcs = []
    for graph1 in g1:
        for graph2 in g2:
            if nx.is_isomorphic(graph1, graph2) is True:
                possible_mcs.append(graph1)

    mcs_graph = nx.Graph()
    for g in possible_mcs:
        if len(g) > len(mcs_graph):
            mcs_graph = g

    distance = (1-len(mcs_graph)/(max(len(G1), len(G2))))

    return distance


# M = nx.dense_gnm_random_graph(10,20)
# M2 = nx.dense_gnm_random_graph(10,20)

M = nx.Graph()

M.add_edges_from([(0,1),
                  (1,2),
                  (1,3),
                  (2,4),
                  (4,3),
                  (0,6),
                  (6,5),
                  (5,0),
                  (0,8),
                  (1,9),
                  (2,7),
                 ])

M2 = nx.Graph()

M2.add_edges_from([(0,1),
                   (1,2),
                   (2,3),
                   (3,4),
                   (4,5),
                   (3,7),
                   (4,8),
                   (8,7),
                   (8,9),
                   (7,6)
                  ])
# nx.draw(M)
# plt.show()
# nx.draw(M2)
# plt.show()

Z, BS1 = distances(M, M2, verbose=False)
# BS2 = mcs_distance2(M, M2)
BS3 = mcs_distance3(M, M2)

print("Zel90:", Z)
print("BS1:", BS1)
# print(BS2)
print("BS3 (brute force):", BS3)