class Box:
    def __init__(self, x1,y1,x2,y2):
        "Die notwendigen Parameter werden initialisiert."
        self.x1    = x1
        self.y1    = y1
        self.x2    = x2
        self.y2    = y2
        self.recalculate()
        self.c = None
        
    def __hash__(self):
        "hash() wird überladen."
        return hash(self.getYOLOTF())
    
    def __eq__(self, other):
        " == wird überladen."
        if type(other) == Box:
            return self.getYOLOTF() == other.getYOLOTF()
        else:
            return self.getYOLOTF() == str(other)
    
    def __ne__(self, other):
        " != wird überladen."
        return not(self == other)
        
    def recalculate(self):
        "Kalkuliert die Fläche und die vier Eckpunkte der Box."
        self.w = self.x2-self.x1
        self.h = self.y2-self.y1
        self.area = max(0, self.x2 - self.x1 + 1) * max(0, self.y2 - self.y1 + 1) #self.w * self.h
        self.tl = (self.x1, self.y1)
        self.tr = (self.x1+self.w, self.y1)
        self.bl = (self.x1, self.y1+self.h)
        self.br = (self.x1+self.w, self.y1+self.h)
        self.points = (self.tl, self.tr, self.bl, self.br)
    
    def getYOLOTF(self):
        "Gibt eine YOLOTF-kompatible Form der Box zurück."
        return str(self.x1)+","+str(self.y1)+","+str(self.x2)+","+str(self.y2)+","+str(self.c)
    
    def draw(self, img, color=(0,255,0), thickness=1):
        "Zeichnet die Box in das übergebene Bild."
        return cv2.rectangle(img.copy(), (self.x1, self.y1), (self.x2, self.y2), color, thickness)
    
    def resize(self, ratio):
        "Vergrößert/verkleinert die Box um übergebenen Faktor."
        self.x1 = int(self.x1*ratio)
        self.x2 = int(self.x2*ratio)
        self.y1 = int(self.y1*ratio)
        self.y2 = int(self.y2*ratio)
        
    def move(self, px, axis=0):
        "Verschiebt Box um übergebene Pixelanzahl in übergebene Richtung"
        if axis == 1:     # horizontal
            self.x1 += px
            self.x2 += px
        elif axis == 0:   # vertikal
            self.y1 += px
            self.y2 += px
            
    def getIntersection(self, other):
        "Gibt die mit übergebener Box entstehende Überlagerung zurück."
        a, b = self, other
        x1 = max(min(a.x1, a.x2), min(b.x1, b.x2))
        y1 = max(min(a.y1, a.y2), min(b.y1, b.y2))
        x2 = min(max(a.x1, a.x2), max(b.x1, b.x2))
        y2 = min(max(a.y1, a.y2), max(b.y1, b.y2))
        if x1<x2 and y1<y2:
            return Box(x1, y1, x2, y2)
        else:
            return Box(0,0,0,0)
    
    def getUnionArea(self, other):
        "Gibt die mit übergebener Box gemeinsame Fläche zurück."
        return self.area + other.area - self.getIntersection(other).area
    
    def getIOU(self, other):
        "Gibt die IOU, bzw. den Jaccard-Index der beiden Boxen zurück."
        return self.getIntersection(other).area / float(self.getUnionArea(other))
    
    def hasPoint(self, p):
        "Es wird überprüft, ob sich der übergebene Bildpunkt in der Box befindet."
        if (self.x1 <= p[0] <= self.x2) and (self.y1 <= p[1] <= self.y2):
            return True
        else:
            return False
        
    def hasBox(self, other):
        "Es wird überprüft, ob sich die übergebene Box in dieser Box befindet."
        if (self.hasPoint(other.tl) == True) and (self.hasPoint(other.br) == True):
            return True
        else:
            return False
        
    def overlapsWith(self, other):
        "Es wird überprüft, ob sich die Boxes überschneiden."
        if (self.hasPoint(other.tl) == True) or (self.hasPoint(other.tr) == True) or (self.hasPoint(other.bl) == True) or (self.hasPoint(other.br) == True):
            return True
        else:
            return False