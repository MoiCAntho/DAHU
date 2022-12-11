import matplotlib.pyplot as plt
from numpy import linspace
import maths as ma

class Graph :
    def __init__(self) -> None:
        pass


def param(X,Y,param,inter=[-10,10],nbpts=10000): #Faire les filtres
    t = []
    for j in linspace(inter[0],inter[1],nbpts) :
        t.append(j)
    x = []
    y = []
    for i in t :
        x.append(X.eval(param,i))
        y.append(Y.eval(param,i))
    print(type(x[1]))
    fig, axes = plt.subplots()
    axes.set_xlim(inter[0],inter[1])
    axes.set_ylim(y[0],y[-1])
    axes.plot(x,y)
    plt.show()
    



class Papier :
    def __init__(args):
        pass
        