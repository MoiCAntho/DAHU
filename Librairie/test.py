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

a = ma.Expression("5x+4cos(8x)")
print(giacpy.giac("5x+4cos(8x)"))
print(str(a))