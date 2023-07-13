from DAHU.maths import Matrice, matriceel

a = matriceel([[5,9,3],[1,7,4],[9,2,3]])
b = a.inverse()
print((a*b).round())