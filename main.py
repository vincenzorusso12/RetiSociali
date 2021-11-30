import math
import os
import matplotlib.pyplot as plt
import numpy as np
import snap
import time
from TPI import TPI
from decisione_differita import decisione_differita

start_time = time.time()

np.random.seed()

G = snap.LoadEdgeList(snap.PUNGraph, 'CA-GrQc.txt', 0, 1)
deg = [v.GetDeg() for v in G.Nodes()]

##Statistiche del grafo
print("Numero di nodi: ", G.GetNodes())
print("Numero di archi: ", G.GetEdges())
print("Grado medio del grafo è ",np.mean(deg))
print("Grado massimo: ", G.GetNI(snap.GetMxDegNId(G)).GetDeg())
print("Diametro (approssimato): ", snap.GetBfsFullDiam(G, 10))
print("Triangoli: ", snap.GetTriads(G))
print("Coefficiente di clustering: ", snap.GetClustCf(G))

const_x, frac_x = [], []

const_uniform_y, const_normal_y = [], []
frac_uniform_y, frac_normal_y = [], []
deterministic_y = []

uniform_probs = {(e.GetSrcNId(), e.GetDstNId()): np.random.uniform() for e in G.Edges()}
normal_probs = {(e.GetSrcNId(), e.GetDstNId()): np.random.normal() for e in G.Edges()}

#deg = [v.GetDeg() for v in G.Nodes()]
iter = math.floor(np.mean(deg))#math ceiling
# deve essere <= di u, perchè la mia resistenza 
print("Il grado medio del grafo è ",iter ) #circa 5.3

step = 1 ## di quanto aumenta la threshold a ogni step?
lanci= 1 ## quanti lanci faccio a ogni step?

print(step, " step")
print(lanci, " lanci")

for i in range(1, (int) (iter+1), step):##ciclo sui valori delle threshold
    constant_threshold = {v.GetId(): i for v in G.Nodes()}
    fraction_threshold = {v.GetId(): v.GetDeg() * i / iter for v in G.Nodes()}
    #print(constant_threshold)
    #print(fraction_threshold)

    const_uniform_sum, const_normal_sum = 0, 0
    frac_uniform_sum, frac_normal_sum = 0, 0
    deterministic_sum = 0

##TPI Deterministico Constant
    deterministicTPI = TPI(G, constant_threshold)
    active = [value for key, value in deterministicTPI.items() if value >= constant_threshold[key]]
    deterministic_sum = deterministic_sum + sum(active)


## TPI Probabilistico
    for j in range(0, lanci):##ciclo sui lanci della monetina
        g_uniform = decisione_differita(G, uniform_probs, dist='uniform')
        g_normal = decisione_differita(G, normal_probs, dist='normal')

        s = TPI(g_uniform, constant_threshold)
        active = [value for key, value in s.items() if value >= constant_threshold[key]]
        const_uniform_sum = const_uniform_sum + sum(active)

        s = TPI(g_normal, constant_threshold)
        active = [value for key, value in s.items() if value >= constant_threshold[key]]
        const_normal_sum = const_normal_sum + sum(active)

        s = TPI(g_uniform, fraction_threshold)
        active = [value for key, value in s.items() if value >= constant_threshold[key]]
        frac_uniform_sum = frac_uniform_sum + sum(active)

        s = TPI(g_normal, fraction_threshold)
        active = [value for key, value in s.items() if value >= constant_threshold[key]]
        frac_normal_sum = frac_normal_sum + sum(active)

    const_uniform_avg = const_uniform_sum / lanci
    const_normal_avg = const_normal_sum / lanci
    frac_uniform_avg = frac_uniform_sum / lanci
    frac_normal_avg = frac_normal_sum / lanci
    #non divido deterministic sum

    const_x.append(i)
    print("i vale ",i)
    frac_x.append(i / iter)
    print("i/iter vale  ",i/iter)

    const_uniform_y.append(const_uniform_avg)
    const_normal_y.append(const_normal_avg)

    frac_uniform_y.append(frac_uniform_avg)
    frac_normal_y.append(frac_normal_avg)

    deterministic_y.append(deterministic_sum)

plt.xlabel('Threshold')
plt.ylabel('TPI costo totale (nodi attivi)')

print(" const x vale ", const_x)

plt.plot(const_x, const_uniform_y, marker='.', label='Uniform')
plt.plot(const_x, const_normal_y, marker='.', label='Normal')
plt.plot(const_x, deterministic_y, marker='.', label='Deterministic')


plt.title('Threshold costante')
plt.legend(title='Distribuzione di probabilità', loc='lower right', fontsize='small', fancybox=True)

if os.path.isfile('grafico_threshold_costante.png'):
   os.remove('grafico_threshold_costante.png')
plt.savefig('grafico_threshold_costante.png')

fig = plt.figure()


plt.xlabel('Threshold')
plt.ylabel('TPI costo totale (nodi attivi)')

print(" frac x vale", frac_x)
plt.plot(frac_x, frac_uniform_y, marker='.', label='Uniform')
plt.plot(frac_x, frac_normal_y, marker='.', label='Normal')
plt.plot(frac_x, deterministic_y, marker='.', label='Deterministic')

plt.title('Threshold proporzionale al grado')
plt.legend(title='Distribuzione di probabilità', loc='lower right', fontsize='small', fancybox=True)
if os.path.isfile('grafico_proporzionale_al_grado.png'):
   os.remove('grafico_proporzionale_al_grado.png')
plt.savefig('grafico_proporzionale_al_grado.png')
print("--- %s seconds ---" % (time.time() - start_time))
