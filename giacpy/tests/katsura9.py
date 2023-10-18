from giacpy import giac, gbasis, giacsettings
from time import clock

giacsettings.threads=4
#katsura n, change n as pleased..
n=11

x=[]
ideal=[]
for i in range(n+1):
  s= "x" + str(i)
  x.append(giac(s))

# x_0 + 2\sum_{i=1}^n x_i = 1
f=x[0]
for i in range(1,n+1):
  f += 2*x[i]
ideal.append(f-1)

# \sum_{j=-n}^{n-i} x_{|j|}x_{|j+i|} = x_{i} \qquad i=0,\dots,n-1
for i in range(n):
  f=-x[i]
  for j in range(-n,n-i+1):
    f += x[abs(j)]*x[abs(j+i)]
  ideal.append(f.regroup())

print(ideal)

"""
For katsura 9, ideal =
[x0+2*x1+2*x2+2*x3+2*x4+2*x5+2*x6+2*x7+2*x8+2*x9-1, x0**2+2*x1**2+2*x2**2+2*x3**2+2*x4**2+2*x5**2+2*x6**2+2*x7**2+2*x8**2+2*x9**2-x0, 2*x0*x1+2*x1*x2+2*x2*x3+2*x3*x4+2*x4*x5+2*x5*x6+2*x6*x7+2*x7*x8+2*x8*x9-x1, x1**2+2*x0*x2+2*x1*x3+2*x2*x4+2*x3*x5+2*x4*x6+2*x5*x7+2*x6*x8+2*x7*x9-x2, 2*x0*x3+2*x1*x2+2*x1*x4+2*x2*x5+2*x3*x6+2*x4*x7+2*x5*x8+2*x6*x9-x3, x2**2+2*x0*x4+2*x1*x3+2*x1*x5+2*x2*x6+2*x3*x7+2*x4*x8+2*x5*x9-x4, 2*x0*x5+2*x1*x4+2*x1*x6+2*x2*x3+2*x2*x7+2*x3*x8+2*x4*x9-x5, x3**2+2*x0*x6+2*x1*x5+2*x1*x7+2*x2*x4+2*x2*x8+2*x3*x9-x6, 2*x0*x7+2*x1*x6+2*x1*x8+2*x2*x5+2*x2*x9+2*x3*x4-x7, x4**2+2*x0*x8+2*x1*x7+2*x1*x9+2*x2*x6+2*x3*x5-x8]
"""

start = clock()
gb=gbasis(ideal,x)
print(clock()-start, "seconds used")
print("gbasis have %s terms"%(gb.dim()))
print("First polynomial have %s terms and multidegree: %s"%(gb[0].nops(),gb[0].degree(x)))

