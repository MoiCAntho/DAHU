from giacpy import *
f=Pygen("factor(normal(((x+y+z+1)^35+1)*(x+y+z+1)^34+2))")
#f.threadeval()
a=giac('(u,v)->a[u,v]')
b=giac('(u,v)->b[u,v]')
n=6;
A=matrix(n,n,a)
B=matrix(n,n,b)
C=A*B

def TT(n):
    l=[]
    for i in range(n):
        l.append(giac(i))
    return l

def TTold(n):
    l=[]
    for i in range(n):
        l.append(Pygen(i).eval())
    return l

