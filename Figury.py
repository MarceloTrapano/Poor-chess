import pygame
import os
from math import fabs

class Figura:
    def __init__(self,Kolor,pole_startowe_x,pole_startowe_y):
        self.kolor = Kolor
        self.x = pole_startowe_x
        self.y = pole_startowe_y
        self.zbite = False
        self.hitbox = pygame.Rect(self.x,self.y,75,75)

    def rusz(self,pole_x,pole_y):
        self.x = pole_x
        self.y = pole_y

    def zbij(self):
        self.x = 2137
        self.y = 2137
        self.zbite = True
        return "*"

class Wieza(Figura):
    def __init__(self,Kolor,pole_startowe_x,pole_startowe_y):
        super().__init__(Kolor,pole_startowe_x,pole_startowe_y)
        self.nazwa = "W"
        self.zbite = False
        if Kolor:
            self.rook = pygame.image.load(os.path.join('Obrazki','WiezaB.png'))
        else:
            self.rook = pygame.image.load(os.path.join('Obrazki','WiezaC.png'))
        self.rook = pygame.transform.scale(self.rook,(75,75))

    def rusz(self,pole_x,pole_y):
        if not self.zbite:
            if pole_y == self.y and pole_x == self.x:
                return False
            elif pole_y == self.y or pole_x == self.x:
                self.x = pole_x
                self.y = pole_y
                return True
        else:
            return 2

class Skoczek(Figura):
    def __init__(self, Kolor, pole_startowe_x, pole_startowe_y):
        super().__init__(Kolor, pole_startowe_x, pole_startowe_y)
        self.nazwa = "S"
        if Kolor:
            self.rook = pygame.image.load(os.path.join('Obrazki','SkoczekB.png'))
        else:
            self.rook = pygame.image.load(os.path.join('Obrazki','SkoczekC.png'))
        self.rook = pygame.transform.scale(self.rook, (75, 75))

    def rusz(self,pole_x,pole_y):
        sprawdzacz = 0
        if not self.zbite:
            if pole_y == self.y and pole_x == self.x:
                return False
            else:
                odleglosc_x = self.x - pole_x
                odleglosc_y = self.y - pole_y
                skoki=[[-150,75],[-75,150],[75,150],[150,75],[150,-75],[75,-150],[-75,-150],[-150,-75]] # mo¿liwe ruchy skoczka
                for s in skoki:
                    if s[0] == odleglosc_x and s[1] == odleglosc_y:
                        self.x = pole_x
                        self.y = pole_y
                        sprawdzacz = 1
                if sprawdzacz:
                    return True
                else:
                    return False
        else:
            return 2

class Goniec(Figura):
    def __init__(self, Kolor, pole_startowe_x, pole_startowe_y):
        super().__init__(Kolor, pole_startowe_x, pole_startowe_y)
        self.nazwa = "G"
        if Kolor:
            self.rook = pygame.image.load(os.path.join('Obrazki','GoniecB.png'))
        else:
            self.rook = pygame.image.load(os.path.join('Obrazki','GoniecC.png'))
        self.rook = pygame.transform.scale(self.rook, (75, 75))
    def rusz(self,pole_x,pole_y):
        if not self.zbite:
            if pole_y == self.y and pole_x == self.x:
                return False
            else:
                odleglosc_x = self.x - pole_x
                odleglosc_y = self.y - pole_y
                if fabs(odleglosc_x) == fabs(odleglosc_y):
                    self.x = pole_x
                    self.y = pole_y
                    return True
                else:
                    return False
                
        else:
            return 2

class Pion(Figura):
    def __init__(self, Kolor, pole_startowe_x, pole_startowe_y):
        super().__init__(Kolor, pole_startowe_x, pole_startowe_y)
        self.nazwa = " "
        self.podwojny = False
        if Kolor:
            self.rook = pygame.image.load(os.path.join('Obrazki','PionB.png'))
        else:
            self.rook = pygame.image.load(os.path.join('Obrazki','PionC.png'))
        self.rook = pygame.transform.scale(self.rook, (75, 75))
    def rusz(self,pole_x,pole_y):
        if not self.zbite:
            odleglosc_y = self.y - pole_y
            odleglosc_x = self.x - pole_x
            if pole_y == self.y and pole_x == self.x:
                return False
            elif pole_x == self.x:
                if self.kolor:
                    if odleglosc_y == 75 or (odleglosc_y == 150 and self.y == 450):
                        self.y = pole_y
                        if odleglosc_y == 150:
                            self.podwojny = True
                            return True
                        self.podwojny = False
                        return True
                    else:
                        return False
                else:
                    if odleglosc_y == -75 or (odleglosc_y == -150 and self.y == 75):
                        self.y = pole_y
                        if odleglosc_y == -150:
                            self.podwojny = True
                            return True
                        self.podwojny = False
                        return True
                    else:
                        return False
            else:
                if self.kolor: 
                    if odleglosc_x in [-75,75] and odleglosc_y == 75:
                        self.x = pole_x
                        self.y = pole_y
                    else:
                        return False
                else: 
                    if odleglosc_x in [-75,75] and odleglosc_y == -75:
                        self.x = pole_x
                        self.y = pole_y
                    else:
                        return False
        else:
            return 2

class Hetman(Figura):
    def __init__(self, Kolor, pole_startowe_x, pole_startowe_y):
        super().__init__(Kolor, pole_startowe_x, pole_startowe_y)
        self.nazwa = "H"
        self.ruch_gonca = False
        self.ruch_wiezy = False
        if Kolor:
            self.rook = pygame.image.load(os.path.join('Obrazki','HetmanB.png'))
        else:
            self.rook = pygame.image.load(os.path.join('Obrazki','HetmanC.png'))
        self.rook = pygame.transform.scale(self.rook, (75, 75))

    def rusz(self,pole_x,pole_y):
        if not self.zbite:
            if pole_y == self.y and pole_x == self.x:
                return False
            else:
                odleglosc_x = self.x - pole_x
                odleglosc_y = self.y - pole_y
                if (fabs(odleglosc_x) == fabs(odleglosc_y)):
                    self.x = pole_x
                    self.y = pole_y
                    self.ruch_gonca = True
                    return True
                elif pole_y == self.y or pole_x == self.x: 
                    self.x = pole_x
                    self.y = pole_y
                    self.ruch_wiezy = True
                    return True
                else:
                    return False
                
        else:
            return 2

class Krol(Figura):
    def __init__(self, Kolor, pole_startowe_x, pole_startowe_y):
        super().__init__(Kolor, pole_startowe_x, pole_startowe_y)
        self.nazwa = "K"
        self.zbite = False
        self.szach = False
        self.roszada_krotka = True
        self.roszada_dluga = True
        if Kolor:
            self.rook = pygame.image.load(os.path.join('Obrazki','KrolB.png'))
        else:
            self.rook = pygame.image.load(os.path.join('Obrazki','KrolC.png'))
        self.rook = pygame.transform.scale(self.rook,(75, 75))

    def rusz(self,pole_x,pole_y):
        self.roszada_krotka = False
        self.roszada_dluga = False
        if not self.zbite:
            if pole_y == self.y and pole_x == self.x:
                return False
            else:
                odleglosc_x = pole_x - self.x
                odleglosc_y = pole_y - self.y
                ruchy=[[-75,-75],[-75,75],[75,75],[75,-75],[75,0],[0,75],[-75,0],[0,-75]]

                for r in ruchy:
                    if r[0] == odleglosc_x and r[1] == odleglosc_y:
                        self.x = pole_x
                        self.y = pole_y
                        return True
                return False
    def zbij(self):
        self.x = 2137
        self.y = 2137
        self.zbite = True
        self.szach = True
        if self.kolor:
            return "0-1"
        else:
            return "1-0"
