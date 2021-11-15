import numpy as np
from collections import defaultdict

def floyd_warshall_original(G):
    dist = defaultdict(lambda: defaultdict(lambda: np.inf))

    for u in G:
        dist[u][u] = 0

    for u, v, d in G.edges(data=True):
        w = 1
        if d.get('weight'):
            w = d.get('weight')

        dist[u][v] = w
        dist[v][u] = w

    for k in G:
        for i in G:
            for j in G:
                distance = dist[i][k] + dist[k][j]
                if dist[i][j] > distance:
                    dist[i][j] = distance
    return dist


def floyd_warshall_improved(G):
    dist = defaultdict(lambda: defaultdict(lambda: np.inf))

    for u, v, d in G.edges(data=True):
        w = 1
        if d.get('weight'):
            w = d.get('weight')
            
        dist[u][v] = w
        dist[v][u] = w
    
    array_out = defaultdict(lambda: [])
    array_in = defaultdict(lambda: [])

    for i in G:
        for j in G:
            if i == j:
                dist[i][j] = 0
                continue
            if dist[i, j] != np.inf:
                array_out[i].append(j)
                array_in[j].append(i)

    for k in G:
        for i in array_in[k]:
            for j in array_out[k]:
                distance = dist[i][k] + dist[k][j]
                if dist[i][j] > distance:
                    dist[i][j] = distance
    return dist