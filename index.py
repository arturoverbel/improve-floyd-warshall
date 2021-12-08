import networkx as nx
import matplotlib.pyplot as plt
import collections
import time
import statistics
import sys
from datetime import datetime

from algorithms import floyd_warshall_original
from algorithms import floyd_warshall_improved
from algorithms import floyd_warshall_best_improved

from networkx.algorithms.shortest_paths.dense import floyd_warshall

def getNow():
    return datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

def printGraph(G):
    pos = nx.spring_layout(G)
    list_edges = list(G.edges())
    list_nodes = list(G.nodes())

    nx.draw_networkx_nodes(
        G, 
        pos=pos, 
        nodelist=list_nodes,
        node_size=1200,
        node_color= 'white',
        edgecolors= 'black'
    )
    nx.draw_networkx_edges(G, pos=pos, edgelist=list_edges, node_size=600)

    edge_labels = dict([((u, v,), d['weight']) for u, v, d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)

    labels = dict()
    for i in list(G.nodes()): labels[i] = str(i)
      
    nx.draw_networkx_labels(G, pos, labels)

    plt.show()

def createGraph(nodes=100, density=0.5):
    edges = (density * nodes * (nodes - 1)) / 2
    return nx.gnm_random_graph(nodes, edges)

def graphSmall():
    graph = nx.DiGraph()

    graph.add_edge('a', 'tt', weight=3)
    graph.add_edge('a', 'b', weight=4)
    graph.add_edge('a', '4', weight=5)
    graph.add_edge('tt', '3', weight=4)
    graph.add_edge('b', '3', weight=2)
    graph.add_edge('4', 'tt', weight=4)

    print('Nodes of graph: ')
    print(graph.nodes())
    print('Edges of graph: ')
    print(graph.edges())

    #printGraph(graph)

    return graph

def graphExample():
    graph = nx.DiGraph()

    graph.add_edge('1', '2', weight=2)
    graph.add_edge('1', '4', weight=5)
    
    graph.add_edge('2', '1', weight=6)
    graph.add_edge('2', '3', weight=3)
    graph.add_edge('2', '4', weight=-1)
    graph.add_edge('2', '5', weight=2)

    graph.add_edge('3', '4', weight=2)
    graph.add_edge('3', '5', weight=-2)

    graph.add_edge('4', '1', weight=-1)
    graph.add_edge('4', '2', weight=1)
    graph.add_edge('4', '3', weight=2)
    graph.add_edge('4', '5', weight=-1)
    
    graph.add_edge('5', '1', weight=1)

    print('Nodes of graph: ')
    print(graph.nodes())
    print('Edges of graph: ')
    print(graph.edges())

    printGraph(graph)

    return graph

def printDist(dist):
    keys = dist.keys()
    for i in dist:
        dd = dict(dist[i].items())
        arrayToPrint = []
        for k in keys: arrayToPrint.append(dd[k])
        print(i.ljust(3), arrayToPrint)

def calculateTimeFunction(G, epoc=1, func=floyd_warshall):
    timeCalculatedes = []
    for trying in range(epoc):
        
        start = time.time()
        dist = func(G)
        timeCalculated = time.time() - start

        timeCalculatedes.append(timeCalculated)

    timeResult = statistics.mean(timeCalculatedes)
    
    return timeResult

def testing():
    G = graphExample()
    print(".................... Calculate Floyd-Warshall .......................")


    dist = floyd_warshall_original(G)
    printDist(dist)

    print(".................... Calculate Floyd-Warshall with Library.......................")

    dist2 = floyd_warshall(G)
    printDist(dist2)

    print(".................... Calculate Floyd-Warshall Improved.......................")

    dist3 = floyd_warshall_improved(G)
    printDist(dist3)

    print(".................... Calculate Floyd-Warshall Improved Best K .......................")

    dist4 = floyd_warshall_best_improved(G)
    printDist(dist4)


exp = "test" if len(sys.argv) <= 1 else sys.argv[1]
epoc = 10 if len(sys.argv) <= 2 else int(sys.argv[2])

experiments = {
    "hard": [
        {"nodes": 500, "density": 1.0},
        {"nodes": 500, "density": 0.7},
        {"nodes": 500, "density": 0.4},
        {"nodes": 1000, "density": 1.0},
        {"nodes": 1000, "density": 0.7},
        {"nodes": 1000, "density": 0.4}
    ],
    "medium": [
        {"nodes": 100, "density": 1.0},
        {"nodes": 100, "density": 0.7},
        {"nodes": 100, "density": 0.4}
    ],
    "easy": [
        {"nodes": 50, "density": 1.0},
        {"nodes": 50, "density": 0.7},
        {"nodes": 50, "density": 0.4}
    ]
}

if exp == "test":
    testing()
    exit()

f = open("status.txt", "w")
f.write("[" + getNow() + "] Running...")
f.close()

resultString = "\n START " + getNow()
resultString += "\n*************************************\n";
for exp in experiments[exp]:
    G = createGraph(exp["nodes"], exp["density"])
    resultString += "\n-----------------------------------------------"
    logInfoGraph = "\ngraph: [nodes=" + str(exp["nodes"]) + ", density=" + str(exp["density"]) + ", epoc=" + str(epoc) + "]"
    print(logInfoGraph)
    print("Loading ... ")
    resultString += logInfoGraph

    resultString += "\n\nFW_original ------"
    timeResult = calculateTimeFunction(G, epoc=epoc, func=floyd_warshall_original)
    resultString += "\nTime: " + str(timeResult) + "(ms)"
    
    resultString += "\n[" + getNow() + "]"

    resultString += "\n\nFW_library ------"
    timeResult = calculateTimeFunction(G, epoc=epoc, func=floyd_warshall)
    resultString += "\nTime: " + str(timeResult) + "(ms)"
    resultString += "\n[" + getNow() + "]"
    
    resultString += "\n\nFW_improved ------"
    timeResult = calculateTimeFunction(G, epoc=epoc, func=floyd_warshall_improved)
    resultString += "\nTime: " + str(timeResult) + "(ms)"
    resultString += "\n[" + getNow() + "]"

    resultString += "\n\nFW improved best K ------"
    timeResult = calculateTimeFunction(G, epoc=epoc, func=floyd_warshall_best_improved)
    resultString += "\nTime: " + str(timeResult) + "(ms)"

    resultString += "\n[" + getNow() + "]"

resultString += "\n*************************************";
resultString += "\n DONE " + getNow()
print("\nDONE")

f = open("log.txt", "w")
f.write(resultString)
f.close()

f = open("status.txt", "a")
f.write("\n[" + getNow() + "] DONE!")
f.close()