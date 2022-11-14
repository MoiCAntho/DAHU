## Erreurs module ##

## Erreurs générales ##

# Erreur 1 : Mauvais type de variable 
def Error_1(ty=None,te=None):
    print("Erreur_module_1 : Mauvais type de variable.\n")
    if ty!=None and te!=None:
        print("La variable doit etre du type : "+ty+" or l'argument est du type "+te+" .")
    elif ty!=None :
        print("La variable doit etre du type : "+ty)

# Erreur 2 : Chemin non valide
def Error_2():
    print("Erreur_module_2 : Le chemin en argument n'est pas un chemin valide")

# Erreur 3 : pas de fichier a destination
def Error_3():
    print("Erreur_module_3 : Ce chemin n'abouti a aucun fichier exploitable")

# Erreur 4 : extension non reconnu (pas prise en charge)
def Error_4():
    print("Erreur_module_4 : Le format du fichier n'est pas pris en charge")

# Erreur 5 : argument manquant
def Error_5():
    print("Erreur_module_5 : un ou plusieurs arguments manquants")

# Erreur 6 : argument non reconnu
def Error_6():
    print("Erreur_module_6 : Argument(s) non reconnue(s)")

## Erreurs partie maths.py ##

def Error_ma_1():
    print("Erreur_maths_1 : Mauvaises dimensions")

def Error_ma_2(ty=None):
    print("Erreur_maths_2 : "+ty+" ne peut etre opéré(e) que par "+ty)

def Error_ma_3():
    print("Erreur_maths_3 : Division par 0")

def Error_ma_4():
    print("Erreur_maths_4 : Necessite d'une matrice carree")

def Error_ma_5():
    print("Erreur_maths_5 : Mauvaises dimensions")
