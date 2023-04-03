## Erreurs DAHU ##

## Gestion des erreurs du package.

## -Refaire entièrement la gestion d'erreurs en y implementant les filtres
# -Utiliser le module inspect qui permet d'introspecter le code et permet notamment de
# recuperer le numero de la ligne en cours d'execution##

## Erreurs générales ##

# Erreur : Mauvais type de variable

# Erreur : Chemin non valide

# Erreur : Aucun fichier a destination

# Erreur : Extension non reconnu (pas prise en charge)

# Erreur : Argument(s) manquant(s)

## Erreurs maths 

# Erreur_ma : Mauvais objets pour opération

# Erreur_ma : Division par 0

# Erreur_ma : Mauvaise dimensions

# Erreur_ma : Matrice non carrée

# Erreur_ma : Matrice non inversible

# Erreur_ma : Matrice inversible

## Erreurs meca

## Erreurs phy

## Erreurs elec





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

def Error_ma_1(clas,el1,el2=None) :
    if el2 != None :
        if isinstance(el1,clas) and isinstance(el2,clas) :
            return True
    else :
        if isinstance(el1,clas) :
            return True
    print("Erreur_maths_1 : Cette action necessite un(des) objet de la classe : "+str(clas))

def Error_ma_2():
    print("Erreur_maths_1 : Mauvaises dimensions")

def Error_ma_3(ty=None):
    print("Erreur_maths_2 : "+ty+" ne peut etre opéré(e) que par "+ty)

def Error_ma_4():
    print("Erreur_maths_3 : Division par 0")

def Error_ma_5():
    print("Erreur_maths_4 : Necessite d'une matrice carree")

def Error_ma_6():
    print("Erreur_maths_5 : Mauvaises dimensions")
