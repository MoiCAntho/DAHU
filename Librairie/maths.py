## Librairie : Partie Mathematiques ##

## Faire les docstrings : """...""" ##

## Contient les algorithmes de calcul numerique ##
import math
import giacpy as g
import erreurs as er
import random as r

# Utilisation de Giac pour gestion des variables et des expressions

class Expression :

    def __init__(self,expr,var,cte) : #Création d'une expression à l'aide d'un str (Faire les filtres) !
        c = {"var" : var ,"cte" : cte}
        self.expr = expr
        self.Expression = g.giac(expr)

    def __getitem__(self,index) :
        return self.Expression[index]

    def __setitem__(self,index,valeur) :
        self.Expression[index] = valeur
    
    def __str__(self) :
        return self.expr

    def __len__(self):
        return len(self.expr)
    
    def __repr__(self) :
        a = str(self)
        return self

    def __add__(self,autre) :
        a = self.expr
        b = autre.expr
        a = g.giac(a)
        b = g.giac(b)
        c = a + b
        self.Expression = c
        self.expr = str(c)
        return self

    def subs(self,var_1,var_2) :
        a = str(self.expr)
        b = a.replace(var_1,var_2)
        return b
    
    def eval(self,var,val) :
        return g.giac(self.subs(var,val))

## Definition d'objets généraux ##

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
            er.Error_1()
    
    def __repr__(self) : #Representation lors de l'utilisation de print()
        c = self.nbc
        l = self.nbl
        chr = ""
        for i in self.Matrice :
            chr += str(i)+"\n"
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
                er.Error_ma_6()
        else :
            er.Error_ma_2(ty="Matrice")

    def __iadd__(self,autre) : #Utilisation de l'operateur +=
        if isinstance(autre,Matrice) :
            if self.nbl == autre.nbc and self.nbc == autre.nbl :
                matreturn = self + autre
                return matreturn
            else :
                er.Error_ma_6()
        else :
            er.Error_ma_2(ty="Matrice")
    
    def __sub__(self,autre) : #Soustraction de deux matrices
        if isinstance(autre,Matrice) :
            if self.nbc == autre.nbc and self.nbl == autre.nbl :
                mat = Matrice(self.nbl,self.nbc)
                for i in range(self.nbl) :
                    for j in range(self.nbc) :
                        mat[i][j] = self[i][j] - autre[i][j]
                return mat
            else :
                er.Error_ma_6()
        else :
            er.Error_ma_2(ty="Matrice")
    
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
        elif str(type(autre)) == "<class 'float'>" or str(type(autre)) == "<class 'int'>" : #Matrice par reel
            mat = Matrice(self.nbl,self.nbc)
            for i in range(self.nbl) :
                for j in range(self.nbc) :
                    mat[i][j] = self[i][j]*float(autre)
            return mat
        else :
            er.Error_6()

    def __rmul__(self,autre) : #Commutativite de la multiplication par un scalaire (faire les filtres)
        if isinstance(autre,int) :
            return self*autre

    def __imul__(self,autre) : #Utilisation de l'operateur *= !
        return self * autre

    def __div__(self,autre) : #Division nécessite la puissance (A faire) :
        pass

    def __pow__(self) : #Mise à la puissance (A faire, necessite la def de l'inverse) !
        pass

    def __eq__(self,autre) : #Verification de l'egalite (faire les filtres) !
        # + Verification matrice meme dimension
        for i in range(self.nbl) :
            for j in range(self.nbc) :
                if self[i][j] != autre[i][j] :
                    return False
                else :
                    return True
    
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

    ## Generations de Matrices particulieres ##

    def randomatrice(lignes,colonnes,xmin=-15,xmax=15) : #Generation d'une matrice aux coefficients aleatoires
        mat = Matrice(lignes,colonnes)
        for i in range(lignes) :
            for j in range(colonnes) :
                mat[i][j] = r.randint(xmin,xmax)
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
            er.Error_ma_5()

    def mel_permutation_l(ligne_1,ligne_2,n) : #Matrice elementaire de permutation de deux lignes (faire les filtres)
        mat = Matrice.matriceid(n)
        for col in range(n) : 
            mat[ligne_1 -1][col], mat[ligne_2 -1][col] = mat[ligne_2 -1][col], mat[ligne_1 -1][col]
        return mat

    def mel_dilatation_l(ligne,valeur,n) : #Matrice elementaire de dilatation d'une ligne (faire les filtres)
        mat = Matrice.matriceid(n)
        for i in range(n) :
            if i == ligne-1 :
                for j in range(n) :
                    mat[i][j] *= valeur
        return mat

    def mat_creuse_1(ligne, colonne, valeur,n) : #Matrice creuse contenant 1 valeur à la position (ligne,colonne)
        mat = Matrice(n,n)
        mat[ligne][colonne] = valeur
        return mat

    def mel_transvection_l(ligne_1,ligne_2,valeur,n) : #Matrice elementaire de transvections de 2 lignes (l1 prend la valeur de l1-valeur*l2) (faire les filtres) !
        mat = Matrice.matriceid(n)+valeur*Matrice.mat_creuse_1(ligne_1-1,ligne_2-1,1,n)
        return mat

    # def mel_permutation_c(colonne_1,colonne_2,n) : #A faire
    #     pass
    
    # def mel_dilatation_c(colonne,valeur,n) :
    #     pass

    # def mel_transvection_c(colonne_1,colonne_2,valeur,n) :
    #     pass


    ## Methodes ##

    def dim(self): #Renvoie la dimension de la matrice !
        return (self.nbl,self.nbc)

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
                            self *= Matrice.mel_permutation_l(i,j,self.dim()[1])
                            p +=1
                if i == j :
                    for k in range(1,self.dim()[0]-1) :
                        self *= Matrice.mel_transvection_l(i,k,(-self[k][i])/self[i][j],self.dim()[1])
        return (self,p)

    def det(self) : #Renvoie le determinant d'une matrice faire les filtres ! 
        if self.iscarree() == True :
            if self.dim() == (2,2) :
                det = self[0][0]*self[1][1] - self[0][1]*self[1][0]
                return det
            else :
                det = 1
                for col in range(self.nbc) :
                    pass

    def triangsup(self) : #finir et faire les autres matrices elementaires pour col et ligne/colo
        nbl = self.nbl
        nbc = self.nbc
        cpt = 0
        for col in range(nbc) :
            a = self[col][col]
            cpt += 1
            for lig in range(nbl) :
                if col != lig :
                    self *= Matrice.mel_transvection_l(lig,cpt,a)
        return self

    def comatrice(self) : #Retourne la matrice de cofacteur d'une matrice (A faire) !
        pass

    def inverse(self) : #Nous retourne la matrice inverse (Definir comatrice()) (Faire les filtres) !
        if self.isinversible() == True :
            a = self.comatrice()
            b = 1/(self.det())*(a.transposee())
            self.Matrice = b

    def gauss_jordan(self) : #Met la matrice sous forme echelon reduite (A faire) !
        n = self.dim()
        pass

    def Spectre(self): #Renvoie le spectre de la matrice si elle est diagonalisable (A faire) !
        pass

    ## Fonctions ##

    def LignePlusGrand(matrice,col) : #Renvoie le numero de la ligne contenant le plus grand coefficient d'une colonne
        nbl = matrice.dim()[0]
        plusgrand = Fonction.abs(matrice[col][col])
        lignePlusGrand = col
        for ln in range(col+1,nbl) :
            if Fonction.abs(matrice[ln][col]) > plusgrand :
                plusgrand = Fonction.abs(matrice[ln][col])
                lignePlusGrand = ln
        return lignePlusGrand


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
    ## Formules et opérations sur les vecteurs ##
    
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

    def prodvec(vec1,vec2) : #Produit vectoriel de deux vecteurs de R3 (faire les filtres) !
        if er.Error_ma_1(Vecteur,vec1,vec2) :
            if len(vec1) == len(vec2) == 3 :
                vec = Vecteur(3)
                vec[0] = vec1[1]*vec2[2] - vec1[2]*vec2[1]
                vec[1] = vec1[2]*vec2[0] - vec1[0]*vec2[2]
                vec[2] = vec1[0]*vec2[1] - vec1[1]*vec2[0]
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
            self.th = math.pi/2
        return (self.r, self.th)
        pass


class Fonction :
    def __init__(self,nom,expr,var) :
        self.Fonction = {"{}".format(nom) : expr, "var" : var}

    ## Definition des fonction usuelles ##
    def sqrt(val = None) :
        if val != None  :
            cpt = 0
            a = math.floor(val)
            while cpt < 100 :
                a = (a+(val)/a)/2
            return a

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

class Polynôme :
    def __init__(self):
        pass
        

class Ensemble :

    def __init__(self) :
        pass

class Intervalle(Ensemble) :

    def __init__(self) :
        pass

## Fonctions de Calcul algebrique ##


## Fonctions Arithmétiques ##

def PGCD(nb_1,nb_2) :
    pass

def PPCM(nb_1,nb_2) :
    pass

def eratostene(n) :
    pass