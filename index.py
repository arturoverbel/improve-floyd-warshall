import networkx as nx
import matplotlib.pyplot as plt
import collections
import time
import statistics

from algorithms import floyd_warshall_original
from algorithms import floyd_warshall_improved

from networkx.algorithms.shortest_paths.dense import floyd_warshall

def printGraph(G):
    labels = dict()
    for i in list(G.nodes()):
        labels[i] = str(i)
      
    nx.draw_networkx_labels(G, nx.spring_layout(G), labels)
    nx.draw(G, with_labels=True)
    plt.show()

def createGraph(nodes=100, density=0.5):
    edges = (density * nodes * (nodes - 1)) / 2
    return nx.gnm_random_graph(nodes, edges)

def graphSmall():
    graph = nx.Graph()

    graph.add_edge("a", "tt", weight=3)
    graph.add_edge("a", "b", weight=4)
    graph.add_edge("a", "4", weight=5)
    graph.add_edge("tt", "3", weight=4)
    graph.add_edge("b", "3", weight=3)
    graph.add_edge("4", "tt", weight=4)

    print("Nodes of graph: ")
    print(graph.nodes())
    print("Edges of graph: ")
    print(graph.edges())

    pos = nx.spring_layout(graph)
    list_edges = list(graph.edges())
    list_nodes = list(graph.nodes())

    nx.draw_networkx_nodes(graph, pos=pos, nodelist=list_nodes, node_size=600)
    nx.draw_networkx_edges(graph, pos=pos, edgelist=list_edges, node_size=600)

    edge_labels = dict([((u, v,), d['weight']) for u, v, d in graph.edges(data=True)])
    nx.draw_networkx_edge_labels(graph, pos=pos, edge_labels=edge_labels)

    return graph



def printDist(dist):
    for i in dist:
        dd = dict(collections.OrderedDict(sorted(dist[i].items())))
        print(i.ljust(3), list(dd.values()))

def calculateTimeFunction(G, name="", epoc=1, func=floyd_warshall):

    print(name, "------")
    timeCalculatedes = []
    for trying in range(epoc):
        
        start = time.time()
        dist = func(G)
        timeCalculated = time.time() - start

        timeCalculatedes.append(timeCalculated)

    timeResult = statistics.mean(timeCalculatedes)
    print("Time: ", timeResult, "(ms)")

    return timeResult


G = graphSmall()
print(".................... Calculate Floyd-Warshall .......................")

dist = floyd_warshall_original(G)
printDist(dist)

print(".................... Calculate Floyd-Warshall with Library.......................")

dist2 = floyd_warshall(G)
printDist(dist2)


print("\n\n\n\n")
print(".................... Tesgint Time .......................")



epoc = 500
experiments = [
    {"nodes": 500, "density": 1.0},
    {"nodes": 500, "density": 0.7},
    {"nodes": 500, "density": 0.4},
    {"nodes": 1000, "density": 1.0},
    {"nodes": 1000, "density": 0.7},
    {"nodes": 1000, "density": 0.4}
]

for exp in experiments:
    G = createGraph(exp["nodes"], exp["density"])

    calculateTimeFunction(G, name="FW_original", epoc=epoc, func=floyd_warshall_original)
    calculateTimeFunction(G, name="FW_library", epoc=epoc, func=floyd_warshall)
    calculateTimeFunction(G, name="FW_improved", epoc=epoc, func=floyd_warshall_improved)