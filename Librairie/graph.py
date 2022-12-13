import matplotlib.pyplot as plt
from numpy import linspace
import maths as ma

class Graph :
    def __init__(self) :
        pass


def param(X,Y,param,inter=[-10,10],nbpts=10000): #Faire les filtres
    t = []
    for j in linspace(inter[0],inter[1],nbpts) :
        t.append(j)
    print(t[0],t[-1])
    x = []
    y = []
    for i in t :
        a = X.eval(param,i)
        b = Y.eval(param,i)
        x.append(a)
        y.append(b)
    print(x[0],x[-1],y[0],y[-1])
    fig, ax = plt.subplots()
    ax.set_xlim(x[0],x[1])
    ax.set_ylim(y[0],y[-1])
    ax.plot(x,y)
    plt.show()

def polar(R,T,param,inter) :
    pass

def isoclines() :
    pass

def chmp_tan(eq) :
    pass        