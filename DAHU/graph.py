from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar, QMenuBar, QStatusBar, QLabel, QWidget, QVBoxLayout
from PyQt6.QtGui import QAction, QIcon, QGuiApplication


import bokeh.plotting as bplt
import matplotlib.pyplot
from maths import Expression, segme, abs

class GraphWindow(QMainWindow) :
    def __init__(self):
        pass



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





def f(x):
    return x**2

x = [i for i in range(-10,10)]
y = [f(i) for i in range(-10,10)]


matplotlib.pyplot.figure()
matplotlib.pyplot.plot(x,y)
matplotlib.pyplot.show()