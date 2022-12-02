import matplotlib.pyplot as plt
import giacpy as g

class Graph :
    def __init__(self) -> None:
        pass


def plotparam(X,Y,param,inter=[-10,10],nbpts=10000): #Faire les filtres
    t = [x for x in range(nbpts)]
    x = []
    y = []
    for i in t :
        x.append(g.subs(param=t,X))
        y.append(g.subs(param=t,Y))
    graph = plt.plot(x,y)
    print(graph)



class Papier :
    def __init__(args):
        pass
        