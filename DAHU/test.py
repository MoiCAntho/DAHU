import maths as ma

# a = ma.Expression("2t+3",var="t")
# b = ma.Expression("4t^3+6t", var="t")
# d = ma.Expression("(y)/(x**2)",var=["t","y"])
# e = ma.Expression("(4*t^2-1)/(t^3+1)",var="t")
# f = ma.Expression("(4*t^3-t)/(t^3+1)",var="t")
# print(e.deriv("t").simp())
# print(f.deriv("t").simp())

# # print(a+b)
# # print(a.subs("t","6"))
# # print(b.deriv("t"))
# # print(b.int("t").simp())

# c = Graph()
# c.absaxe(fixe=True,pt = 0)
# c.ordaxes(fixe=True,pt=0)
# c.param(e,f,"t",inter=[-100,100],nbpts=25)
# #c.chmptan(d,"xy",[-10,10],[-10,10],1)
# c.show()

# a = ma.randomatrice(3,3)
# print(a) 
# b = a.pivots()
# print (b)

# h = ma.Expression("2*x**3-6*x*y+2*y**3-3*x-3*y",var=["x","y"])
# print(h)
# a = h.deriv("x").simp()
# b = h.deriv("y").simp()
# print(a)
# print(b)
# print(h)

# f = ma.Expression("e^(x^2-y)*(5-2*x+y)",var=["x","y"])
# a = f.lim("x","+infinity")
# print(a)

a = ma.Polynôme([1,2,3],"t")
print(a)