## Partie permettant de communiquer avec les microcontroleurs

import serial.tools.list_ports

class Board :
    def __init__(self,nom = None, port = None, v = None, serie = None) :
        self.nom = nom
        self.port = port
        self.vite = v
        self.serie = serie
    
    def __str__(self) :
        return str(self.nom)+","+str(self.port)+","+str(self.vite)
    
    def __repr__(self) :
        return str(self)
    
    def open(self) : #Ouverture du port serie
        if self.vite == None :
            self.serie = serial.Serial(self.port)
        else :
            self.serie = serial.Serial(self.port,self.baudrateconv())

    def close(self) : #Fermeture du port serie
        self.serie.close()
        pass

    def detectBoard(self,carte) :
        a = portactifs()
        usb = []
        for p in a :
            if carte in p.description :
                usb.append(p)
        if len(usb) == 1 :
            self.nom = p.description
            self.port = p.device
        else :
            pass
    
    def vitesse(self):
        self.open()
        self.vite = int(self.serie.baudrate)
        self.close()

    def baudrateconv(self) :
        self.vitesse()
        return serial.SerialBase.BAUDRATES.index(self.vite) + 1

    ## Méthodes d'envoie de donnees
    
    def sendTrue(self) :
        pass

    def sendFalse(self) :
        pass

    def sendStr(self,str) :
        self.serie.write(str.encode("utf-8"))

    ## Méthodes de réception de donnees

    def recepInt(self) :
        pass

    def recepFloat(self) :
        pass

def portactifs() :
    return list(serial.tools.list_ports.comports())




ard = Board()
ard.detectBoard("USB")

ard.open()
ard.sendStr("Start")
ard.close()
