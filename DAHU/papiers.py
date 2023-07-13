from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
from math import tan

## Formats et themes predefinis ## 

A4 = (297*mm,210*mm)

defaut = {} #Noir

class Papier :

    def __init__(self, format=A4, nom="000.pdf", mar=[10*mm,6*mm,6*mm,6*mm]): # Template papier graphes
        marge = [format[1]-mar[0],0+mar[1],0+mar[2],format[0]-mar[3]] # marge [haut,bas,gauche,droite]
        pdf = canvas.Canvas(nom,pagesize=landscape(format))
        rect = [mar[2],mar[1],format[0]-(mar[2]+mar[3]),format[1]-(mar[0]+mar[1])]
        pdf.rect(rect[0],rect[1],rect[2],rect[3])
        pdf.setFont("Helvetica",6)
        pdf.drawString(format[0]-30*mm,marge[1]-(marge[1]/5),"DAHU.py")
        self.pdf = pdf
        self.marge = marge
        self.format = format
        self.cadre = rect
        pdf.translate(0,0)

    def save(self) :
        self.pdf.save()

def milli(format=A4, nom="milli.pdf", mar=[10*mm,6*mm,6*mm,6*mm]):
    pap = Papier(format,nom,mar)
    ## Trace des lignes horizontales
    print(pap.marge)
    c = 0
    for i in range(int(pap.cadre[1]),int(pap.cadre[3])):
        if c%5 == 0 or c == 0 :
            pap.pdf.setLineWidth(0.3*mm)
            c+=1
        else :
            pap.pdf.setLineWidth(0.1 * mm)
            c+=1
        pap.pdf.line(pap.cadre[0], i * mm, pap.cadre[2], i * mm)








    # for i in range(int(pap.marge[2]),int(pap.marge[3])) :
    #     if c%5 == 0 or c == 0 :
    #         pap.pdf.setLineWidth(0.3*mm)
    #         pap.pdf.line(i*mm,pap.marge[0],i*mm,pap.marge[1])
    #         c += 1
    #     else :
    #         pap.pdf.setLineWidth(0.1*mm)
    #         pap.pdf.line(i*mm,5*mm,i*mm,190*mm)
    #         c+= 1
    c = 0
    # for i in range(int(marges[2]),int(marges[3])) :
    #     if i%5 == 0 or c == 0 :
    #         pap.pdf.setLineWidth(0.3*mm)
    #         pap.pdf.line(3.5*mm,i*mm,293.5*mm,i*mm)
    #         c += 1
    #     else :
    #         pap.pdf.setLineWidth(0.1*mm)
    #         pap.pdf.line(3.5*mm,i*mm,293.5*mm,i*mm)
    #         c += 1
    return pap

def semilog(format,nom,theme) :
    pass

def loglog(format,nom,theme) :
    pass

def polaire(format=A4,nom="polaire.pdf",mar=[20,6,6,6],theme=defaut) :
    pdf = Papier(format,nom,mar)
    a = pdf.pdf
    b = pdf.cadre
    a.translate(mar[2]*mm,mar[1]*mm)
    xc = b[2]/2
    yc = b[3]/2
    for i in range(200) :
        a.circle(xc,yc,i*mm)
    a.line(xc,0,xc,b[3])
    a.line(0,yc,b[2],yc)
    for i in [30,40,60,120,130,150] :
        a.line(xc,yc,b[2],(xc*tan(i))+yc)
    a.save()


#pdf.setFont("Helvetica",8)
#pdf.drawString(260*mm,1.5*mm,"DAHU.py")
#canvas.Canvas(nom,pagesize=landscape(format))

milli().save()