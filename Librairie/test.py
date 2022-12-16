import maths as ma
from graph import Graph

# a = ma.Expression("2t+3",var="t")
# b = ma.Expression("4t^3+6t", var="t")
# d = ma.Expression("(y)/(x**2)",var=["t","y"])
e = ma.Expression("(2t)/(1+t^2)",var="t")
f = ma.Expression("(2+t^3)/(1+t^2)",var="t")
print(e.deriv("t").simp())
print(f.deriv("t").simp())

# print(a+b)
# print(a.subs("t","6"))
# print(b.deriv("t"))
# print(b.int("t").simp())

c = Graph()
c.param(e,f,"t",nbpts=100)
# c.chmptan(d,"xy",[-10,10],[-10,10],1)
c.show()

# a = ma.randomatrice(3,3)
# print(a)
# b = a.pivots()
# print (b)