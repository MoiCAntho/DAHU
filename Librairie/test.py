import maths as ma
# #Test de la fonction importdonnees#
# f=importdata("C:\\Users\\segur\\Documents\\MEGA\\Université\\MEC204-Mécanique du point II\\TP\\TP 3 Ressorts frottements secs\\données.csv")
# print(f)

# a = ma.Matrice.matriceel([[6, 4, 7, 0, -1],[11, -1, 4, 10, 6],[4, 1, -6, -8, 13],[-10, -8, -15, -3, -14]])
# print(a)
# b = ma.Matrice.mel_transvection_l(3,1,-5,5)
# print(b)
# print(a*b)

#g.plotparam(giacpy.giac("2t+1"),giacpy.giac("4t^2-2"),t)

a = ma.Expression("2t+3")
b = ma.Expression("4t^3+6t")
print(a+b)
print(ma.Expression.subs(a,"t",6))