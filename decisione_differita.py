import numpy as np
import snap


def decisione_differita(G, probs, dist):
    graph = snap.ConvertGraph(snap.PUNGraph, G)

    for e in graph.Edges():## Per ogni nodo e nel grafo G

        if dist == 'uniform':
            x = np.random.uniform()
        else:
            x = np.random.normal()

        src = e.GetSrcNId()
        dst = e.GetDstNId()

        if x < probs[(src, dst)]: # se il numero generato pseudocasualmente è < di una certa soglia
            graph.DelEdge(src, dst) #cancella l'arco

    return graph
