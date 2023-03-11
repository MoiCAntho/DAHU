import bokeh.plotting as bplt
import matplotlib.pyplot as plt
from numpy import linspace
from maths import Expression, segme

class Graph :
    def __init__(self) :
        self.graph = bplt.figure(x_axis_label='x', y_axis_label='y',
           x_range=(-10, 10), y_range=(-10, 10),
           aspect_ratio=1)

    def absaxe(self,fixe = False,pt = 0) :
        if fixe == True :
            self.graph.xaxis.fixed_location = pt
        pass

    def ordaxes(self,fixe = False,pt = 0) :
        if fixe == True :
            self.graph.yaxis.fixed_location = pt

    def fgraph(self,expr,param,inter=[-10,10],nbpts=10000) :
        a = self.graph
        y = []
        x = linspace(inter[0],inter[1],nbpts)
        for i in x :
            y.append(expr.eval(param,i))
        a.line(x,y)

    def param(self,X,Y,param,inter=[-10,10],nbpts=10000) :
        a = self.graph
        t = []
        for i in linspace(inter[0],inter[1],nbpts) :
            t.append(i)
        x = []
        y = []
        for i in t :
            x.append(X.eval(param,i))
            y.append(Y.eval(param,i))
        print(t)
        print(x)
        print(y)
        a.line(x,y)

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
        bplt.show(self.graph)



def grille(xinter,yinter,unite) :
    if xinter == None :
        xinter = [-10,10]
    if yinter == None :
        yinter = [-10,10]
    if unite == None :
        unite = 1
    grille = {"x":segme(xinter[0],xinter[1],unite),"y":segme(yinter[0],yinter[1],unite)}
    return grille