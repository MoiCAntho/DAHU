from calendar import LocaleTextCalendar
from main import importdata
# import meca as me
import maths as ma
import phy as p
# import latexify as ltx 

# #Test de la fonction importdonnees#
# f=importdata("C:\\Users\\segur\\Documents\\MEGA\\Université\\MEC204-Mécanique du point II\\TP\\TP 3 Ressorts frottements secs\\données.csv")
# print(f)

d = ma.Matrice.matriceel([[3,6,3,3],[9,1,0,10],[9,10,1,1]])
a = ma.Matrice.matrice123(3,3)
c = ma.Matrice.mel_transvection_l(2,5,10,6)

print(c)
