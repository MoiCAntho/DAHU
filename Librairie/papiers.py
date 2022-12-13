from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

class Papier :

    def __init__(self,format=A4,nom="1234") :
        pdf = canvas.Canvas(nom,pagesize=format)
        return pdf