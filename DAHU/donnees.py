## Donnees DAHU ##

## Contient toutes les données, notamment les constantes, nécessaires au fonctionnement du package
## ainsi que d'autres infos pouvant-être utiles

## Constantes mathématiques ##

pi = 3.14158 #Trouver une approx + fiable
# e =
# phi =

## Constantes universelles ##

cl = 299792458 #Celerite de la lumiere en m/s
ce = 1.602176634*10**(-19) #Charge élémentaire en C
hp = 6.62607015*10**(-34) #Constante de Planck en J.s
csf = 7.2973525664*10**(-3) #Constante de structure fine sans dimension
mu0 = (2*csf*hp)/(ce**2*cl) #Permeabilite du vide en T.m/A
eps0 = 1/(mu0*cl**2) #Permitivité du vide en F/m
Gu = 6.67430*10**(-11) #Constante universelle de gravitation en N.m^2/kg^2
cg = 398600.4418 #Constante geocentrique en km^3/s^2
Mt = 5.972*10**24 #Masse de la terre en kg ou cg/Gu
Rt = 6371000 #Rayon moyen de la terre en m
grav = (Gu*Mt)/(Rt**2) #Acceleration de pesanteur en m/s^2

## Donnees chimiques ##

## Libellés des informations de notre mini tableau
# Z : Numéro atomique
# A : Nombre de masse en unité de masse atomique
# E : Electronegativite##

element = {
    "H":{"Z":1,"A":1.008,"E":2.20},
    "He":{"Z":2,"A":4.002602}
}

## Physique des materiaux ##


## Formats papiers ##

A4 = (297,210) #en mm