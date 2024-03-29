## DAHU : Partie Mathematiques ##

## Faire les docstrings : """...""" ##

## Import des modules & packages essentiels ##
## Packages exterieurs

## Traitement necessaire pour l'inclusion de giacpy en tant que fichier
import sys
import os
# Obtenez le chemin absolu du répertoire racine du projet
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Ajoutez le chemin du répertoire racine à sys.path
sys.path.insert(0, project_root)

import giacpy

## Import des autres packages


import random
import copy
import math

# Utilisation de Giac pour gestion des variables et des expressions et autres pitits trucs #

## Definitions d'objets mathématiques généraux ##

class Expression :
    """Classe permettant de creer et manipuler les expressions"""

    def __init__(self,expr,var,cte = None) : #Création d'une expression à l'aide d'un str (Faire les filtres) !
        self.c = {"var" : var ,"cte" : cte}
        self.Expr = giacpy.giac(expr)
        self.sexpr = str(self.Expr)
        self.derivs = []
        self.ints = []
        self.ty = ""
        if "=" in self.sexpr :
            self.ty = "equa"

    def __getitem__(self,index) :
        return self.Expr[index]

    def __setitem__(self,index,valeur) :
        self.Expr[index] = valeur
    
    def __str__(self) :
        return self.sexpr

    def __len__(self):
        return len(self.sexpr)
    
    def __repr__(self) :
        return self.sexpr

    def __add__(self,autre) :
        if isinstance(autre,Expression) :
            a = self.sexpr
            b = autre.sexpr
            a = giacpy.giac(a)
            b = giacpy.giac(b)
            c = a + b
            self.Expr = c
            self.sexpr = str(c)
            return self
        if isinstance(autre,int) :
            a = "("+self.sexpr+")+"+str(autre)
            self.sexpr = a
            self.Expr = giacpy.giac(a)
            return self
        if isinstance(autre,float) :
            a = "("+self.sexpr+")+"+str(autre)
            self.sexpr = a
            self.Expr = giacpy.giac(a)
            return self
    
    def __radd__(autre,self) :
        if isinstance(autre,Expression) :
            return autre + self
        if isinstance(autre,int) :
            a = str(autre)+"+("+self.sexpr+")"
            self.sexpr = a
            self.Expr = giacpy.giac(a)
            return self
        if isinstance(autre,float) :
            a = str(autre)+"+("+self.sexpr+")"
            self.sexpr = a
            self.Expr = giacpy.giac(a)
            return self

    def __iadd__(self,autre) : #A faire
        pass

    def __sub__(self,autre) : #A faire
        pass

    def __rsub__(self,autre) : #A faire
        pass

    def __isub__(self,autre) : #A faire
        pass

    def __mul__(self,autre) : #!!
        if isinstance(autre,Expression) :
            a = self.sexpr
            b = autre.sexpr
            self.sexpr = a+"*"+b
            self.Expr = giacpy.giac(self.sexpr)
            return self
        if isinstance(autre,int) :
            a = "("+self.sexpr+")*"+str(autre)
            self.sexpr = a
            self.Expr = giacpy.giac(a)
            return self
        if isinstance(autre,float) :
            a = "("+self.sexpr+")*"+str(autre)
            self.sexpr = a
            self.Expr = giacpy.giac(a)
            return self

    def __rmul__(autre,self) : #!!
        if isinstance(autre,Expression) :
            return autre * self
        if isinstance(autre,int) :
            a = str(autre)+"*("+self.sexpr+")"
            self.sexpr = a
            self.Expr = giacpy.giac(a)
            return self
        if isinstance(autre,float) :
            a = str(autre)+"*("+self.sexpr+")"
            self.sexpr = a
            self.Expr = giacpy.giac(a)
            return self

    def __imul__(self,autre) : #A faire
        pass

    def __div__(self,autre) : #A faire
        pass

    def __rdiv__(self,autre) : #A faire
        pass

    def __idiv__(self,autre) : #A faire
        pass

    def __pow__(self,autre) : #A faire
        pass

    def subs(self,var_1,var_2) : #Substitue une variable en une autre
        a = self.sexpr
        b = a.replace(str(var_1),str(var_2))
        return b
    
    def eval(self,var,val) : #Evalue l'expression pour une valeur
        a = self.subs(var,val)
        b = giacpy.giac(a)
        if str(b) == "undef":
            return None
        else :
            return float(b)
    
    ## Calcul infinitesimal : derivees, integrales, limites ...##

    def deriv(self, var) :
        expr1 = giacpy.diff(self.Expr, var)
        self.derivs.append(str(expr1))
        derivexpr = Expression(str(expr1), var=self.c)
        return derivexpr
    
    def int(self, var, a=None, b=None):
        if a == None and b == None :
            self.Expr = giacpy.int(self.Expr,var)
            self.ints.append(str(self.Expr))
            intexpr = Expression(str(self.Expr),var=self.c)
            return intexpr
        else :
            return giacpy.int(self.Expr,var,a,b)

    def simp(self) :
        self.Expr = giacpy.simplify(self.Expr)
        self.sexpr = str(self.Expr)
        return self

    def sucderiv(self,var,nb) :
        for i in range(nb) :
            self.deriv(var)

    def jaco(self): #Défini que pour un champ scalaire (faire les filtres)
        jac = Matrice(len(self.c["var"]),1)
        for i in range(len(self.c["var"])) :
            jac[i][0] = self.deriv(self.c["var"][i]).simp()
        self.derivs.append(jac)
        return jac

    def hessi(self,ordre): #Renvoie la matrice hessienne d'une fonction ! (faire les filtres)
        pass

    def lim(self,var,val): #Renvoie la limite d'une fonction en une valeur (faire les filtres)
        lim = giacpy.limit(self.Expr,var,giacpy.giac(val))
        lim = str(lim)
        return lim
    
    def solve(self) :
        if self.ty == "equa" :
            print(giacpy.solve(self.Expr,self.c["var"]))
        else :
            return None

class Matrice :
    """Classe permettant de creer et manipuler les matrices"""
    
    ## Definition des fonctions elementaires et operations de la classe ##

    def __init__(self,nbl,nbc) : #Initialise une matrice (genere la matrice nulle)
        if str(type(nbl)) == "<class 'int'>" and str(type(nbc)) == "<class 'int'>" :
            self.nbl = nbl
            self.nbc = nbc
            matrice = []
            for i in range(nbl):
                t=[]
                for j in range(nbc):
                    t.append(0)
                matrice.append(t)
            self.Matrice = matrice
        else :
            pass
    
    def __repr__(self) : #Representation lors de l'utilisation de print()
        l = self.nbl
        chr = ""
        for i in range(l) :
            if i != 0 :
                chr += "\n"
            chr += "[ "
            cpt =0
            for j in self.Matrice[i] :
                chr += str(j)
                cpt += 1
                if cpt != len(self.Matrice[i]) :
                    chr += " , "
            chr += " ]"
        return chr
    
    def __getitem__(self,index) :  #Retourne un element de la matrice
        return self.Matrice[index]
    
    def __setitem__(self,index,valeur) : #Affectation d'une valeur
        self.Matrice[index] = valeur
    
    def __len__(self) : #Nombres d'elements de la matrice !
        return self.nbl*self.nbc

    def __add__(self,autre) : #Additions entre matrices
        if isinstance(autre,Matrice) :
            if self.nbc == autre.nbc and self.nbl == autre.nbl :
                mat = Matrice(self.nbl,self.nbc)
                for i in range(self.nbl) :
                    for j in range(self.nbc) :
                        mat[i][j] = self[i][j] + autre[i][j]
                return mat
            else :
                pass
        else :
            pass

    def __iadd__(self,autre) : #Utilisation de l'operateur +=
        if isinstance(autre,Matrice) :
            if self.nbl == autre.nbc and self.nbc == autre.nbl :
                matreturn = self + autre
                return matreturn
            else :
                pass
        else :
            pass
    
    def __sub__(self,autre) : #Soustraction de deux matrices
        if isinstance(autre,Matrice) :
            if self.nbc == autre.nbc and self.nbl == autre.nbl :
                mat = Matrice(self.nbl,self.nbc)
                for i in range(self.nbl) :
                    for j in range(self.nbc) :
                        mat[i][j] = self[i][j] - autre[i][j]
                return mat
            else :
                pass
        else :
            pass
    
    def __isub__(self,autre) : #Utilisation de l'operateur -= !
        return self - autre

    def __mul__(self,autre) : #Multiplications (refaire les filtres)
        if isinstance(autre,Matrice) : #Matrice par matrice
            if self.nbc == autre.nbl :
                n = self.nbc
                mat = Matrice(self.nbl,autre.nbc)
                for i in range(self.nbl) :
                    for j in range(autre.nbc) :
                        x = 0
                        for k in range(n) :
                            x += self[i][k] * autre[k][j]
                        mat[i][j] = x
                return mat
        elif isinstance(autre,int) or isinstance(autre,float) : #Matrice par reel
            mat = Matrice(self.nbl,self.nbc)
            for i in range(self.nbl) :
                for j in range(self.nbc) :
                    mat[i][j] = self[i][j]*float(autre)
            return mat
        else :
            pass

    def __rmul__(autre,self) : #Commutativite de la multiplication par un scalaire (faire les filtres)
        if isinstance(autre,int) :
            return self*autre
        if isinstance(autre,Matrice):
            return autre*self

    def __imul__(self,autre) : #Utilisation de l'operateur *= !
        return self * autre

    def __div__(self,autre) : #Division nécessite la puissance (A faire) :
        pass

    def __pow__(self,pui) : #Mise à la puissance (A finir, necessite la def de l'inverse) !
        if pui == 0 :
            if self.dim()[0] < self.dim()[1] :
                n = self.dim()[0]
            else :
                n = self.dim()[1]
            return matriceid(n)
        if pui > 0 :
            pass
        if pui < 0:
            pass

    def __eq__(self,autre) : #Verification de l'egalite (faire les filtres) !
        # + Verification matrice meme dimension
        for i in range(self.nbl) :
            for j in range(self.nbc) :
                if self[i][j] != autre[i][j] :
                    return False
                else :
                    return True

    def round(self, n=None):
        for i in range(self.nbl):
            for j in range(self.nbc):
                self[i][j] = round(self[i][j],n)
        return self

    def clear(self) :
        for i in range(self.nbl) :
            for j in range(self.nbc) :
                self[i][j] = 0

    def copy(self):
        mat = Matrice(self.nbl,self.nbc)
        mat.Matrice = copy.deepcopy(self.Matrice)
        return mat

    def giac_convert(self) :
        return giacpy.giac(self.Matrice)

    ## Methodes ##

    def mat_augm_lig(self, pos = None):  # Insère une ligne vide à la position mise en agrument
        lig = []
        for i in range(self.nbc):
            lig.append(0)
        if pos != None:
            sto_lig = {}
            for i in range(pos - 1, self.nbl):
                sto_lig[str(i)] = self[i]
            self[pos - 1] = lig
            for k in sto_lig.keys():
                if int(k) + 1 <= self.nbl:
                    self.Matrice.append(sto_lig[k])
                for j in range(self.nbc):
                    self[int(k) + 1] = sto_lig[k]
            self.nbl += 1
        else:
            self.Matrice.append(lig)
            self.nbl += 1

    def mat_augm_col(self, pos = None):
        if pos != None:
            for i in range(self.nbl):
                self.Matrice[i].insert(pos - 1, 0)
            self.nbc += 1
        else:
            for i in range(self.nbl):
                self.Matrice[i].insert(self.nbc, 0)
            self.nbc += 1

    def mat_sup_lig(self, pos = None):
        if pos != None :
            del self.Matrice[pos-1]
            self.nbl -= 1
        else :
            del self.Matrice[self.nbl-1]
            self.nbl -= 1

    def mat_sup_col(self, pos = None):
        if pos != None :
            for i in range(self.nbl) :
                del self.Matrice[i][pos-1]
            self.nbc -= 1
        else :
            for i in range(self.nbl) :
                del self.Matrice[i][self.nbc-1]
            self.nbc -= 1

    def dim(self): #Renvoie la dimension de la matrice !
        return (self.nbl,self.nbc)

    def iscarree(self) : #Vérification qu'une matrice est carree
        if self.nbl == self.nbc :
            return True
        else :
            return False

    def isinversible(self) : #Verification de l'inversibilite d'une matrice (A faire) !
        if self.iscarree() == True and self.det() != 0 :
            return True
        else :
            return False

    def transposee(self) : #Retourne la transposee d'une matrice (faire les filtres)
        mat = Matrice(self.nbc,self.nbl)
        l = 0
        c = 0
        for i in range(self.nbl) :
            for j in range(self.nbc) :
                mat[j][i] = self[i][j]
        return mat

    def pivots(self) : # Renvoie une matrice echelonnee et le nombre de permutation !
        p = 0
        for i in range(self.dim()[0]) :
            for j in range(self.dim()[1]) :
                if i == j and self[i][j] == 0 :
                    for j in range(len(self[1])) :
                        if self[i][j] != 0 :
                            self = self.permutation_lig(i,j,self.dim()[1])
                            p +=1
                if i == j :
                    for k in range(1,self.dim()[0]-1) :
                        self = self.transvection_lig(i,k,(-self[k][i])/self[i][j],self.dim()[1])
        return (self,p)

    def det(self) : #Renvoie le determinant d'une matrice faire les filtres ! 
        if self.iscarree() == True :
            if self.dim() == (2,2) :
                det = self[0][0]*self[1][1] - self[0][1]*self[1][0]
                return det
            else :
                a = self.giac_convert()
                det = giacpy.det(a)
                return int(det)

    def tranvesction_lig(self,ligne_1,ligne_2,valeur) : #Transvecte une ligne avec une autre d'une certaine valeur (faire les filtres) !
        n = self.dim()
        a = mel_transvection(ligne_1,ligne_2,valeur,n[1])
        return a*self

    def tranvesction_col(self,ligne_1,ligne_2,valeur) : #Transvecte une colonne avec une autre d'une certaine valeur (faire les filtres) !
        n = self.dim()
        a = mel_transvection(ligne_1,ligne_2,valeur,n[1])
        return self*a

    def comatrice(self) : #Retourne la matrice de cofacteur d'une matrice !
        mat = Matrice(self.nbl,self.nbc)
        for i in range(self.nbl) :
            for j in range(self.nbc) :
                a = self.copy()
                a.mat_sup_lig(pos = i+1)
                a.mat_sup_col(pos = j+1)
                print(a)
                mat[i][j] = a.det()*(-1)**(i+j)
        return mat

    def inverse(self, arr=True, dig=3): #Nous retourne la matrice inverse (Definir comatrice()) (Faire les filtres) !
        if self.isinversible()==True:
            a = self.comatrice()
            b = 1/(self.det())*(a.transposee())
            if arr == True:
                b.round(dig)
            return b

    def gauss_jordan(self) : #Met la matrice sous forme echelon reduite (A faire) !
        n = self.dim()
        pass

    def eigenval(self) :
        #Vérification matrice carrée
        for i in range(self.dim()[0]) :
            self[i][i] = Expression(str(self[i][i])+"-t",var=["t"])
        det = self.det()
        print(det)
        # Définir résolution polynomiale pour résolution det(A)=0

    def eigenvec(self) :
        pass

    def Spectre(self) : #Renvoie le spectre de la matrice si elle est diagonalisable (A faire) !
        pass

    def diago(self) :
        pass

    def ker(self) :
        pass

    def tr(self) :
        a = 0
        for lig in range(self.nbl) :
            for col in range(self.nbc) :
                if col == lig :
                    a += self[lig][col]
        return a
    
    def pseudo_inverse(self):
        pass


class Vecteur(Matrice) :

    def __init__(self,n) : #Initialisation d'un vecteur (genere le vecteur nul)
        self.l = n
        vec = super().__init__(n,1)
        self.Vecteur = vec
    
    def __getitem__(self, index):
        return self[index]
    
    def __setitem__(self, index, valeur):
        self[index] = valeur

    def __len__(self) :
        return self.l

    def __mul__(self, autre): #Produit par un réel et produit scalaire !
        if isinstance(autre,int) :
            vec = Vecteur(len(self))
            for i in range(len(self)) :
                vec[i] = autre*self[i]
            return vec
        if isinstance(autre,Vecteur) :
            if len(self) == len(autre) :
                vec = Vecteur(len(self))
                sca = 0
                for i in range(len(self)) :
                    sca += autre[i]*self[i]
                return sca

    def __repr__(self):
        return super().__repr__()
    
    def VecPts(pts) : #Prend en argument une liste de tuples representant les coordonnees de chaques points (faire les filtres) !
        n = len(pts) 
        # + Verification de la dimension de chaque pts
        vec = Vecteur(n)
        for i in range(n) :
            x = 0
            for j in range(n) :
                x -= pts[-j][i]
            vec[i] = x
        return vec

class Complexe :
    def __init__(self,a = 0,b = 0) : #Initialise un nombre complexe (forme algébrique) (Faire filtres) !
        self.a, self.b = a, b
    
    def __repr__(self) : #Definition pour la fonction print !
        return str(self)

    def __add__(self,autre) : #Addition de deux complexes !
        return self.a + autre.a, self.b + autre.b
    
    def __str__(self) : #Conversion en str !
        if self.a != 0 and self.b != 0 :
            return "z = "+str(float(self.a))+" + "+str(float(self.b))+"i"
        elif self.a == 0 and self.b !=0 :
            return "z = "+str(float(self.b))+"i"
        elif self.a != 0 and self.b == 0 :
            return "z = "+str(float(self.a))
        else :
            return "z = 0"
    
    def module(self) : #Definir la racine carree
        a = (self.a)**2+(self.b)**2
        return Fonction.sqrt(a)

    def expo(self) :
        if self.b != 0 and self.a != 0 :
            self.r = self.module()
            self.th = self.a/self.r
        elif self.b == 0 and self.a != 0 :
            self.r = self.a
            self.th = 0
        elif self.a == 0 and self.b != 0 :
            self.r = self.b
            self.th = (math.pi)/2
        return (self.r, self.th)

class Graphe :
    def __init__(self):
        pass

class Fonction(Expression) :
    def __init__(self,nom,expr,var) :
        self.Fonction = {"{}".format(nom) : expr, "var" : var}
        self.df = [] #Liste d'intervalles ou 1 intervalle (domaine de def)
        self.lim = [] #Liste des limites associées aux valeurs limval
        self.limval = []

    ## Definition des fonction usuelles ##
    def sqrt(val = None) :
        pass

    def ln() :
        pass

    def cos() :
        pass

    def sin() :
        pass

    def abs(val = None) : #Fonction valeur absolue faire filtres
        if val != None :
            a = val**2
            b = Fonction.sqrt(a)
            return b
    
    def etude() :
        pass

    ## Définition des différents types de fonctions

class Polynôme() :
    def __init__(self,coef,var):
        self.coef = coef
        p = ""
        for i in range(len(self.coef)) :
            a = float(self.coef[i])
            p = p + "(" + str(a) + ")*" + var + "^(" + str(len(self.coef)-i)+ ")"
            if i != len(self.coef) :
                p += "+"
        b = [var]
        print(p)
        self.expr = Expression(p,b)
        self.expr = self.expr.simp()
    
    def __repr__(self):
        return self.expr.sexpr

class Ensemble :

    def __init__(self) :
        pass

class Intervalle(Ensemble) :

    def __init__(self) :
        pass


## Définitions de quelques opérations ##

def prodvec(vec1,vec2) : #Produit vectoriel de deux vecteurs de R3 (faire les filtres) !
    if True :
        if len(vec1) == len(vec2) == 3 :
            vec = Vecteur(3)
            vec[0] = vec1[1]*vec2[2] - vec1[2]*vec2[1]
            vec[1] = vec1[2]*vec2[0] - vec1[0]*vec2[2]
            vec[2] = vec1[0]*vec2[1] - vec1[1]*vec2[0]
        return vec


## Génération de matrices ##


def randomatrice(lignes,colonnes,xmin=-15,xmax=15) : #Generation d'une matrice aux coefficients aleatoires
    mat = Matrice(lignes,colonnes)
    for i in range(lignes) :
        for j in range(colonnes) :
            mat[i][j] = random.randint(xmin,xmax)
    return mat

def matrice123(lignes,colonnes) : #Generation d'une matrice suivant la suite des entiers naturels !
    mat = Matrice(lignes,colonnes)
    t = 1
    for i in range(lignes) :
        for j in range(colonnes) :
            mat[i][j] = t
            t += 1
    return mat
    
def matriceid(n) : #Generation de la matrice identite de dimension n !
    mat = Matrice(n,n)
    for i in range(n) :
        for j in range(n) :
            if i == j :
                mat[i][j] = 1
            else :
                mat[i][j] = 0
    return mat

def matriceel(element) : #Generation d'une matrice à partir d'une liste de liste d'elements
    cpt = 0
    cd = True
    for i in element :
        if cpt == 0 :
            a = len(i)
            cpt += 1
        else :
            if a != len(i) :
                cd = False
    if cd != False :
        mat = Matrice(len(element),a)
        for i in range(len(element)) :
            for j in range(a) :
                mat[i][j] = element[i][j]
        return mat
    else :
        pass

def mat_creuse_1(ligne, colonne, valeur,n) : #Matrice creuse contenant 1 valeur à la position (ligne,colonne)
    mat = Matrice(n,n)
    mat[ligne][colonne] = valeur
    return mat

## Attention pour utiliser les mel il faut poser la multiplication dans le bon sens mel*mat !! ##

def mel_permutation(ligne_1,ligne_2,n) : #Matrice elementaire de permutation de deux lignes (faire les filtres)
    mat = matriceid(n)
    for col in range(n) : 
        mat[ligne_1 -1][col], mat[ligne_2 -1][col] = mat[ligne_2 -1][col], mat[ligne_1 -1][col]
    return mat

def mel_dilatation(ligne,valeur,n) : #Matrice elementaire de dilatation d'une ligne (faire les filtres)
    mat = matriceid(n)
    for i in range(n) :
        if i == ligne-1 :
            for j in range(n) :
                mat[i][j] *= valeur
    return mat

def mel_transvection(ligne_1,ligne_2,valeur,n) : #Matrice elementaire de transvections de 2 lignes (l1 prend la valeur de l1-valeur*l2) (faire les filtres) !
    a = valeur * mat_creuse_1(ligne_2,ligne_1,1,n)
    mat = matriceid(n) +  a
    return mat

def matrice_augmentee(mat_1,mat_2) :
    m_a = []
    m_a.append(mat_1)
    m_a.append(mat_2)
    return m_a

## Fonctions de Calcul algebrique ##


def taylor(expr,var,pt,ordre) :
    expr.sucderiv(var,ordre)

def approx_fourrier():
    pass


## Fonctions Arithmétiques ##


def PGCD(nb_1,nb_2) : #Renvoie le plus grand diviseur commun de deux nombres
    pass

def PPCM(nb_1,nb_2) : #Renvoie le plus petit commun multiple de deux nombres
    pass

def eratostene(n) : #Renvoie une liste contenant tous les nombres premier de 1 jusqu'a n par le crible d'eratostene
    pass

def segme(start,stop,nbpts): #Definit un découpage sur un segment entre deux valeurs Faire les filtres
    delta_x = (stop - start)/(nbpts-1)
    segme = [start+i*delta_x for i in range(0,nbpts)]
    return segme


## Statistiques

def moyenne(x,n=None):
    if n == None :
        j = 0
        for i in len(x):
            j += x[i]
        moy = j/len(x)
        return moy
    else :
        if len(x) == len(n) :
            j = 0
            for i in len(n) :
                j+=x[i]*n[i]
            moy = j/len(n)
        
        return moy

def variance():
    pass

def ecart_type():
    pass

def covariance():
    pass

def coef_correlation() :
    pass

def choix_reg():
    pass

## Analyse numérique et de donnees

def num_deriv(x,y=None,pas=None) : #Prend une liste donnees
    deriv = []
    if y != None and pas == None :
        if len(x) == len(y) :
            for i in range(1,len(x)-1) :
                deriv.append((x[i]-x[i-1])/(y[i]-y[i-1]))
            return deriv
        else :
            print("Erreur")
    elif y == None and pas != None :
        for i in range(1,len(x)-1) :
            deriv.append((x[i]-x[i-1])/pas)
    else :
        print("Erreur")

def regr() : #Regression linéaire, logarithmique, exponentielle ou puissance à partir de données
    pass

def MCNL () : #Curvefit avec la méthode des moindres carrées non linéaire
    pass


## Autres & vrac

def red_gauss(q) :
    return giacpy.gauss(q.Expr,q.c["var"])

def trigo_fourier(f, var, per = 2*math.pi, dep = 0) : #Donne les coefficients trigonométriques de Fourier généraux sous la forme d'une liste (dans l'intervale -pi pi, donc série est 2pi périodique) Faire les filtres
    coef = []
    a0 = (1 / per) * f.int(var, dep, dep + per)
    an = Expression(str(giacpy.fourier_an(f.Expr, var, per, "p", dep)),["p"])
    bn = Expression(str(giacpy.fourier_bn(f.Expr, var, per, "p", dep)),["p"])
    coef.append(a0)
    coef.append(an)
    coef.append(bn)
    return coef

def fourier_an(f, varex, var="n", int=[-math.pi,math.pi],):
    a = Expression("cos(nx)",["x"])
    a = f*a
    print(a)
    an = a.int(varex,int[0],int[1])
    return an


def somme(expr,indic,dep,max) : #Utilisation de la somme sigma
    if indic in expr.c["var"] :
        modifex = Expression(expr.sexpr,var=expr.c["var"].remove(indic))
    ssomme = ""
    for i in range(dep,max) :
        a = expr.subs(indic,i+1)
        if i == max-1 :
            ssomme += str(a)
        else :
            ssomme += str(a) + "+"
    somme = Expression(ssomme,var=modifex.c["var"])
    return somme

def serie_fourier(coefs,max) :
    a = Expression(str(coefs[1])+"*cos(px)"+"+"+str(coefs[2])+"*sin(px)",var=["p","x"])
    serie = coefs[0]+somme(a,"p",0,max)
    return serie

def briggs(nb, it=25) : #Approxime le logarithme neperien d'un nombre, precision a 8 decimales
    a = 1/nb
    n=0
    while n < it :
        a = math.sqrt(a)
        n += 1
    return (1-a)*2**it


