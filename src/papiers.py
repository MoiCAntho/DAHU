from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
from math import tan
## Formats et themes predefinis ## 

A4 = (297*mm,210*mm)

defaut = {} #Noir

class Papier :

    def __init__(self,format=A4,nom="000.pdf",mar=[20,6,6,6]) : # Template papier graphes
        marge = [format[1]-mar[0]*mm,0*mm+mar[1]*mm,0*mm+mar[2]*mm,format[0]-mar[3]*mm] # [haut,bas,gauche,droite]
        pdf = canvas.Canvas(nom,pagesize=landscape(format))
        rect = [marge[2],marge[1],format[0]-(mar[2]+mar[2])*mm,format[1]-(mar[0]+mar[1])*mm]
        pdf.rect(rect[0],rect[1],rect[2],rect[3])
        pdf.setFont("Helvetica",6)
        pdf.drawString(format[0]-30*mm,marge[1]-(marge[1]*(mm/5)),"DAHU.py")
        self.pdf = pdf
        self.marge = marge
        self.format = format
        self.cadre = rect
        pdf.translate(0,0)
        return None

    def save(self) :
        self.pdf.save()

def milli(format=A4,nom="milli.pdf",mar=[6*mm,6*mm,6*mm,10*mm]) :
    pdf = canvas.Canvas(nom,pagesize=landscape(format))
    c = 0
    marges = [0+mar[0],0+mar[1],format[0]-mar[2],format[1]-mar[3]]
    print(marges)
    for i in range(format[0],294) :
        if c%5 == 0 or c == 0 :
            pdf.setLineWidth(0.3*mm)
            pdf.line(a*mm,5*mm,a*mm,190*mm)
            c += 1
        else :
            pdf.setLineWidth(0.1*mm)
            pdf.line(a*mm,5*mm,a*mm,190*mm)
            c+= 1
    c = 0
    for i in range(5,191) :
        if i%5 == 0 or c == 0 :
            pdf.setLineWidth(0.3*mm)
            pdf.line(3.5*mm,i*mm,293.5*mm,i*mm)
            c += 1
        else :
            pdf.setLineWidth(0.1*mm)
            pdf.line(3.5*mm,i*mm,293.5*mm,i*mm)
            c += 1
    pdf.setFont("Helvetica",8)
    pdf.drawString(260*mm,1.5*mm,"DAHU.py")
    return pdf

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

milli()