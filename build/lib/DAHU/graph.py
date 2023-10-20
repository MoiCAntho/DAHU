# import bokeh.plotting as bplt
import matplotlib.pyplot
from maths import Expression, segme




class Graph :
    def __init__(self) :
        pass

    def plotparam(x,y,param,inter=[-10,10]) :
        X, Y = [], []
        for i in range(abs(inter[0])+abs(inter[1])):
            X.append(x.eval())

        matplotlib.pyplot.plot(X,Y)

        pass

    def plot():
        pass



f = Expression("(8.314*T)/(1.400*10^5)", ["T"])


x = [i for i in range(-10,10)]
y = [f.eval("T",i) for i in range(-10,10)]


matplotlib.pyplot.figure()
matplotlib.pyplot.plot(x,y)
matplotlib.pyplot.show()