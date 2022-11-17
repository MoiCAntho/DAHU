## Module : Partie Mecanique

import main
import maths
import erreurs as er
from numpy import diff

## Choisir quel type de mecanique 
# -du point
# -du solide
# -des fluides
# ...##

## Classes ##

class Torseur :

    def __init__(self,R=None,M=None,pt=None,ty=None) : #Initialisation d'un torseur (genere le torseur nul)
        self.R = R
        self.M = M
        self.pt = pt
        self.ty = ty
        tor = ([R,M],pt)
        self.Torseur = tor
    
    def __getitem__(self,index) : #Recuperation d'une valeur
        return self.Torseur[index]

    def __setitem__(self,index,valeur) : #Affectation d'une valeur
        self.Torseur[index] = valeur

    def __add__(self,autre) : #Definition de l'addition
        if isinstance(autre,Torseur) == True :
            if self[1] == autre[1] :
                tor = Torseur()
                tor[0][1] = self[0][1] + autre[0][1]
                tor[0][2] = self[0][2] + autre[0][2]
                tor[1] = self[1] + autre[1]
                return tor
            else :
                er.Error_mec_1()
        else :
            pass

## Generations des torseurs usuelles ##

## Formules diverses ##

    def Transport(self) :
        if self.ty == "Force" :
            pass

# Faire les filtres pour diverses vérifications dans les fonctions (rajouter les erreurs, s'il faut)

def extractm(chemin):
    df = main.importdata(chemin)

# paramètres cinématiques (calculs numeriques)

def vitessept(pos,t):
    v=diff(pos)/t
    return v

def accelpt(vi,t):
    a = diff(vi)/t
    return a

# Graphes en tout genres