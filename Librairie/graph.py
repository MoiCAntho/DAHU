import matplotlib.pyplot as plt
from numpy import linspace
from maths import Expression, segme

class Graph :
    def __init__(self) :
        self.fig,self.ax = plt.subplots()

    def absaxe(self) :
        pass

    def ordaxes(self) :
        pass

    def param(self,X,Y,param,inter=[-10,10],nbpts=10000) :
        a = self.ax
        t = []
        for i in linspace(inter[0],inter[1],nbpts) :
            t.append(i)
        x = []
        y = []
        for i in t :
            x.append(X.eval(param,i))
            y.append(Y.eval(param,i))
        a.plot(x,y)

    def polar(self,r,param) :
        pass

    # def chmptan(self,yprim,param,xinter,yinter,unite) :
    #     a = self.ax
    #     g = grille(xinter,yinter,unite)
    #     b = unite-0.2
    #     yprim = ma.yprim.subs(param,"x")
    #     for i in range(len(g["x"])) :
    #         for j in range(len(g["y"])) :
    #             c = yprim.subs(param[0],i)
    #             d = yprim.eval(param[1],j)
    #             a.quiver(g["x"][i],g["y"][j],b,c)

    def show(self) :
        plt.show()



def grille(xinter,yinter,unite) :
    if xinter == None :
        xinter = [-10,10]
    if yinter == None :
        yinter = [-10,10]
    if unite == None :
        unite = 1
    grille = {"x":segme(xinter[0],xinter[1],unite),"y":segme(yinter[0],yinter[1],unite)}
    return grille