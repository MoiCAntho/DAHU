## Module python ##

##Description ...
# Contient pour le moment les classes Expression, Matrice, Vecteur, Graph, Torseur##

##Là où se trouve des '!' se trouvent des fonctionnalitées a tester##

## A faire ##
##
# -faire les commentaires """ ... """ pour la fonction help
# -finir les principales classes
# -se renseigner sur importlib
# -faire fonctionner le module latexify##


## Import nécéssaire pour le fichier main##
from genericpath import isfile
import erreurs as er
from posixpath import splitext
from pandas import read_csv, read_excel
import os

## Mécanique ##

## Physique ##

## Filtres divers A faire ##

#Fonctions communes au sous fichiers #

def importdata(chemin):
    ty = "str"
    if str(type(chemin))=="<class 'str'>" :
        if os.path.exists(chemin) == True : #Vérfification si chemin valide
            if os.path.isfile(chemin) == True :
                position_ext = chemin.find(".") #Trouver la position de l'extension
                ext_file = chemin[position_ext:position_ext+4] #Récupération de l'extension
                if ext_file == ".csv" :
                    df=read_csv(chemin)
                    return df
                elif ext_file == ".xls" or ".odt" :
                    df = read_excel(chemin)
                    return df
                else :
                    er.Error_4()
            else :
                er.Error_3()
        else :
            er.Error_2()
    else:
        er.Error_1(ty)