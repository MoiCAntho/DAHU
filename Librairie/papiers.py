from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.graphics import line, circle, rect
from reportlab.pdfgen import canvas

class Papier :

    def __init__(self,format=A4,nom="1234.pdf") :
        self.pdf = canvas.Canvas(nom,pagesize=format)
        return self