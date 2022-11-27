from calendar import LocaleTextCalendar
from main import importdata
# import meca as me
import giacpy
import maths as ma
import phy as p
# import latexify as ltx 

# #Test de la fonction importdonnees#
# f=importdata("C:\\Users\\segur\\Documents\\MEGA\\Université\\MEC204-Mécanique du point II\\TP\\TP 3 Ressorts frottements secs\\données.csv")
# print(f)

a = ma.Matrice.matriceel([[6, 4, 7, 0, -1],[11, -1, 4, 10, 6],[4, 1, -6, -8, 13],[-10, -8, -15, -3, -14]])
print(a)
b = ma.Matrice.mel_transvection_l(3,1,-5,5)
print(b)
print(a*b)