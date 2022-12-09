import maths as ma

a = ma.Expression("2t+3",var="t")
b = ma.Expression("4t^3+6t", var="t")
print(a+b)
print(ma.Expression.subs(a,"t","6"))
print(ma.Expression.deriv(b,"t"))