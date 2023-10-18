from giacpy import giac
x,y,z=giac('x,y,z')
n=25
f=(x+y+z+1)**n+1
g=(f*(f+1)).ratnormal()
from time import time
t=time()
print(g.factor().nops())
print("n=",n,"temps:",time()-t)
n=30
f=(x+y+z+1)**n+1
g=(f*(f+1)).ratnormal()
from time import time
t=time()
print(g.factor().nops())
print("n=",n,"temps:",time()-t)
