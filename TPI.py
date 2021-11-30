
def TPI(G, threshold):
    ##inizializzazione
    k = threshold.copy()
    s = {v.GetId(): 0 for v in G.Nodes()}
    delta = {v.GetId(): v.GetDeg() for v in G.Nodes()}
    neighbours = {v.GetId(): {v.GetNbrNId(i) for i in range(0, v.GetDeg())} for v in G.Nodes()}

    U = {v.GetId() for v in G.Nodes()}

    while U:##finchè ci sono nodi, non li ho rimossi tutti 
        for v in U:
            if k[v] > delta[v]:##caso 1 threshold > grado vado ad incentivare v 
                s[v] = s[v] + k[v] - delta[v]#es k=4 e delta v=3 aumento l'incentivo di v di 1=4-3
                k[v] = delta[v]#lo porto da s[v] a s[v+1] è come se gli avessi diminuitio il threshold

                if k[v] == 0:#il threshold è pari a 0 v si è attivato e lo rimuouvo
                    U.remove(v)

                break
        else:#caso 2 threshold residui <= del grado
            tmp = {u: (k[u] * (k[u] + 1)) / (delta[u] * (delta[u] + 1)) for u in U}# uso un criterio di selezione sulla somma dei threshold massimi che voglio accumulare 
            v = max(tmp, key=tmp.get)

            for u in neighbours[v].copy():
                delta[u] = delta[u] - 1
                neighbours[u].remove(v)

            U.remove(v)



    return s