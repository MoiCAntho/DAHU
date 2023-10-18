#Dans pyzo j'ai mis shell config PySide
#NB: pour qcas dans pyzo il faut n'importe quel autre shel config
from matplotlib import pyplot

from giacpy import giac
def mplotcurve(plotdata,pyplotoptions='b'):
    x=[]
    y=[]
    if plotdata.type() == 'DOM_LIST':     # s'il y a plusieurs composantes
        for component in plotdata:
            mplotcurve(component)
   
    if plotdata.type()=='DOM_SYMBOLIC':
        if plotdata[0]=='pnt':
            dessin=plotdata[1]
           
            if dessin.type()=='DOM_SYMBOLIC':   # la courbe a une forme parametree avant
                if dessin[0]=='curve':
                    #formeparametrique=dessin[1]     #si on souhaite la recuperer
                    G=dessin[2]                      #ici on utilisel la discretisation deja calculee
                elif dessin[0]=='circle':
                    #arcs de cercles
                    O=dessin.center()[1]
                    rayon=dessin.radius()
                    G=giacpy.seq(O+rayon*giacpy.exp('i*j'),'j',dessin[2],dessin[3]+0.1,0.1)
                   
            elif dessin.type() == 'DOM_LIST':
                if dessin._subtype == 0: # la courbe n'est qu'une liste de points ou segment
                    G=dessin
                elif dessin._subtype == 5: # polygones
                    G=dessin
                #dessin._subtype == 7 is arrows: ->
                #dessin._subtype == 9 is halfline
                elif dessin._subtype == 6:   #line
                    G=dessin                 # TODO elles seront traitees comme des segment
            xG=G.real().round(14).eval()
            yG=G.im().round(14).eval()
            x=[u._double for u in xG]
            y=[u._double for u in yG]
            pyplot.plot(x,y,pyplotoptions)
            pyplot.show()
    return


import giacpy
from giacpy import sin
x,y=giac('x,y')
f=(1/(2+sin(3*x))).integrate()
print(f)
D1=f.plot('x=-10..10')
M=giacpy.ranm(20,2,'-5..5')
D3=(x**3-y**2-x).plotimplicit('x=-10..10,y=-10..10')
mplotcurve(D1)
mplotcurve(giac([D3,giacpy.circle(0,5)]))
D4=giacpy.arc('1+i,2,pi/4')


