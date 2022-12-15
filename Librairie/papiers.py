from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm

## Formats predefinis ## 

A4 = (297*mm,210*mm)

class Papier :

    def __init__(self,format=A4,nom="000.pdf",mar=[10,6,6,6]) :
        marge = [format[1]-mar[0]*mm,0*mm+mar[1]*mm,0*mm+mar[2]*mm,format[0]-mar[3]*mm]
        pdf = canvas.Canvas(nom,pagesize=landscape(format))
        rect = [marge[2],marge[1],format[0]-(mar[2]+mar[2])*mm,format[1]-(mar[0]+mar[1])*mm]
        pdf.rect(rect[0],rect[1],rect[2],rect[3])
        self.pdf = pdf
        self.marge = marge
        self.format = format
        self.cadre = rect
        pdf.translate(0,0)
        return None
    
    def save(self) :
        self.pdf.save()

pdf = Papier()
pdf.save()
