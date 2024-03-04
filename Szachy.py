import pygame
import os
import datetime
import Figury as fg
import re
from Problemy import Niejednoznaczne
 
class Deska:
    def __init__(self):
        self.wynik = "*"                                    # Do zapisu koncowego
        self._running = True                                # Obsluga petli
        self._display_surf = None                           # Powierzchnia na ktorej dziala program
        self.size = self.weight, self.height = 600, 700     # Rozmiar okna
        self.FPS = 30                                       # Odswierzanie glownej petli while
        self.ruch = 1                                       # Zlicza posuniecia
        self.licznik = 0                                    # Zmienna do obslugi zliczania posuniec
        self.slownik_x = {"a":0,"b":75,"c":150,"d":225,"e":300,"f":375,"g":450,"h":525}
        self.inv_slownik_x = {i: j for j,i in self.slownik_x.items()}
        self.slownik_y = {"8":0,"7":75,"6":150,"5":225,"4":300,"3":375,"2":450,"1":525}
        self.inv_slownik_y = {i: j for j,i in self.slownik_y.items()}
        self.aktualny_ruch = ""
 
    def on_init(self):                                      # Dodatkowa inicjacja
        pygame.init()                                       # Inicjator srodowiska pygame
        pygame.display.set_caption("Szachy")                # Zmiana podpisu okna
        self.szachy = pygame.image.load(os.path.join('Obrazki','szach.png'))
        self.Deseczka = pygame.image.load(os.path.join('Obrazki','deseczka.png'))   # Wczytanie deski i etc.
        self.Deska = pygame.image.load(os.path.join('Obrazki','deska.png'))
        self.ruchB = pygame.image.load(os.path.join('Obrazki','ruchb.png')) #ruchB i ruchC odpowiada za wyswietlanie czyja jest tura
        self.ruchB = pygame.transform.scale(self.ruchB,(50,50))
        self.ruchC = pygame.image.load(os.path.join('Obrazki','ruchc.png'))
        self.ruchC = pygame.transform.scale(self.ruchC,(50,50))
        self.data = datetime.datetime.now()
        self._wejscie_box = pygame.Rect(50, 650, 140, 32)
        self.color_inactive = pygame.Color('grey52')    # Kolor dla pola nieaktywnego
        self.color_active = pygame.Color('white')       # Kolor dla pola aktywnego
        self.color = self.color_inactive                # Kolor czcionki
        self.active = False                             # Zmienna do sprawdzania aktywnosci pola
        self.text = ''                                  # Tekst jaki bedzie wpowadzac uzytkownik
        self.plik = open("Partia.txt",'w')              # Otwarcie do jakiego pliku ma sie exportowac partia
        self.tura = True                                # Znacznik tury
        self.zapis_ruchow = "1. "                       # Do tego beda sie zapisywac ruchy
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF) # Tworzenie okna
                
    def promocja(self,figura):
        if figura.nazwa == " ":
            if self.aktualny_ruch[len(self.aktualny_ruch)-1] == "B" or self.aktualny_ruch[len(self.aktualny_ruch)-1] == "G": 
                figura = fg.Goniec(figura.kolor,figura.x,figura.y)
                if figura.kolor:
                    self.Lista_Pionkow_Biale.remove(figura)
                else:
                    self.Lista_Pionkow_Biale.remove(figura)
                self.Lista_Goncow.append(figura)
                return True
            elif self.aktualny_ruch[len(self.aktualny_ruch)-1] == "Q" or self.aktualny_ruch[len(self.aktualny_ruch)-1] == "H": 
                figura = fg.Hetman(figura.kolor,figura.x,figura.y)
                if figura.kolor:
                    self.Lista_Pionkow_Biale.remove(figura)
                else:
                    self.Lista_Pionkow_Biale.remove(figura)
                self.Lista_Hetmanow.append(figura)
                return True
            elif self.aktualny_ruch[len(self.aktualny_ruch)-1] == "R" or self.aktualny_ruch[len(self.aktualny_ruch)-1] == "W": 
                figura = fg.Wieza(figura.kolor,figura.x,figura.y)
                if figura.kolor:
                    self.Lista_Pionkow_Biale.remove(figura)
                else:
                    self.Lista_Pionkow_Biale.remove(figura)
                self.Lista_Wiez.append(figura)
                return True
            elif self.aktualny_ruch[len(self.aktualny_ruch)-1] == "N" or self.aktualny_ruch[len(self.aktualny_ruch)-1] == "S": 
                figura = fg.Skoczek(figura.kolor,figura.x,figura.y)
                if figura.kolor:
                    self.Lista_Pionkow_Biale.remove(figura)
                else:
                    self.Lista_Pionkow_Biale.remove(figura)
                self.Lista_Skoczkow.append(figura)
                return True
            else:
                self.tura = not self.tura
                return False
        else:
            self.tura = not self.tura
            return False

    def rozstawienie_figur(self):                       # Odpowiada za inicjacje obiektow klasy figura
        self.CW1 = fg.Wieza(0,0,0)
        self.CW2 = fg.Wieza(0,525,0)
        self.BW1 = fg.Wieza(1,0,525)
        self.BW2 = fg.Wieza(1,525,525)
        self.CS1 = fg.Skoczek(0,75,0)
        self.CS2 = fg.Skoczek(0,450,0)
        self.BS1 = fg.Skoczek(1,75,525)
        self.BS2 = fg.Skoczek(1,450,525)
        self.CG1 = fg.Goniec(0,150,0)
        self.CG2 = fg.Goniec(0,375,0)
        self.BG1 = fg.Goniec(1,150,525)
        self.BG2 = fg.Goniec(1,375,525)
        self.Ca = fg.Pion(0,0,75)
        self.Cb = fg.Pion(0,75,75)
        self.Cc = fg.Pion(0,150,75)
        self.Cd = fg.Pion(0,225,75)
        self.Ce = fg.Pion(0,300,75)
        self.Cf = fg.Pion(0,375,75)
        self.Cg = fg.Pion(0,450,75)
        self.Ch = fg.Pion(0,525,75)
        self.Ba = fg.Pion(1,0,450)
        self.Bb = fg.Pion(1,75,450)
        self.Bc = fg.Pion(1,150,450)
        self.Bd = fg.Pion(1,225,450)
        self.Be = fg.Pion(1,300,450)
        self.Bf = fg.Pion(1,375,450)
        self.Bg = fg.Pion(1,450,450)
        self.Bh = fg.Pion(1,525,450)
        self.BH = fg.Hetman(1,225,525)
        self.CH = fg.Hetman(0,225,0)
        self.BK = fg.Krol(1,300,525)
        self.CK = fg.Krol(0,300,0)
        self.Lista_Kroli = [self.CK,self.BK]
        self.Lista_Hetmanow = [self.BH,self.CH]
        self.Lista_Pionkow_Czarne = [self.Ca,self.Cb,self.Cc,self.Cd,self.Ce,self.Cf,self.Cg,self.Ch]
        self.Lista_Pionkow_Biale = [self.Ba,self.Bb,self.Bc,self.Bd,self.Be,self.Bf,self.Bg,self.Bh]
        self.Lista_Goncow = [self.CG1,self.CG2,self.BG1,self.BG2]
        self.Lista_Wiez = [self.BW1,self.BW2,self.CW1,self.CW2]
        self.Lista_Skoczkow = [self.BS2,self.BS1,self.CS1,self.CS2]
        self.rozstawienie_Biale = [self.BW1,self.BW2,self.BS2,self.BS1,self.BG1,self.BG2,self.BK,self.BH,self.Ba,self.Bb,self.Bc,self.Bd,self.Be,self.Bf,self.Bg,self.Bh]
        self.rozstawienie_Czarne = [self.CW1,self.CW2,self.CS1,self.CS2,self.CG1,self.CG2,self.CK,self.CH,self.Ca,self.Cb,self.Cc,self.Cd,self.Ce,self.Cf,self.Cg,self.Ch]
        # Listy pomocnicze do obslugi figur

    def zmienne_szachowe_x(self,zmienna_x):             # Konwersja notacji szachowych na koordynaty
        if zmienna_x in self.slownik_x:
            return self.slownik_x[zmienna_x]
        else:
            return False

    def roszada_krotka(self):
        laczna_lista = self.rozstawienie_Biale+self.rozstawienie_Czarne
        if self.tura:
            if self.BK.roszada_krotka:
                for i in laczna_lista:
                    if (i.x == 375 or i.x == 450) and i.y == 525:
                        self.tura = not self.tura
                        return False
                self.BK.x = 450
                self.BW2.x = 375
                self.BK.roszada_krotka = False
                self.BK.roszada_dluga = False
                return True
        else:
            if self.CK.roszada_krotka:
                for i in laczna_lista:
                    if (i.x == 375 or i.x == 450) and i.y == 0:
                        self.tura = not self.tura
                        return False
                self.CK.x = 450
                self.CW2.x = 375
                self.CK.roszada_krotka = False
                self.CK.roszada_dluga = False
                return True
        self.tura = not self.tura
        return False

    def roszada_dluga(self):
        laczna_lista = self.rozstawienie_Biale+self.rozstawienie_Czarne
        if self.tura:
            if self.BK.roszada_dluga:
                for i in laczna_lista:
                    if (i.x == 75 or i.x == 150 or i.x == 225) and i.y == 525:
                        self.tura = not self.tura
                        return False
                self.BK.x = 150
                self.BW1.x = 225
                self.BK.roszada_krotka = False
                self.BK.roszada_dluga = False
                return True
        else:
            if self.CK.roszada_dluga:
                for i in laczna_lista:
                    if (i.x == 75 or i.x == 150 or i.x == 225) and i.y == 0:
                        self.tura = not self.tura
                        return False
                self.CK.x = 150
                self.CW1.x = 225
                self.CK.roszada_krotka = False
                self.CK.roszada_dluga = False
                return True
        self.tura = not self.tura
        return False

    def zmienne_szachowe_y(self,zmienna_y):
        if zmienna_y in self.slownik_y:
            return self.slownik_y[zmienna_y]
        else:
            return False

    def Sprawdzenie_Goniec(self,figura,ruch_x,ruch_y):              # Sprawdza czy goniec moze sie poruszyc na dane pole
        odleglosc_x = ruch_x - figura.x                             # robi to przez sprawdzanie czy na drodze jego poruszania
        odleglosc_y = ruch_y - figura.y                             # sie stoi jakas figura
        pozycja_poczatkowa_x = figura.x                             # Jezli na polu na jakim wyladuje jest inna figura to ja zbija
        pozycja_poczatkowa_y = figura.y
        laczna_lista = self.rozstawienie_Biale+self.rozstawienie_Czarne
        if figura in laczna_lista:
            laczna_lista.remove(figura)
        else:
            return False
        if figura.rusz(ruch_x,ruch_y):
            for i in range(75,odleglosc_x+75,75):
                if odleglosc_y < 0:
                    for j in laczna_lista:
                        if i != odleglosc_x:
                            if j.x == i + pozycja_poczatkowa_x and j.y == -i + pozycja_poczatkowa_y:
                                figura.rusz(pozycja_poczatkowa_x,pozycja_poczatkowa_y)
                                return False
                        if i == odleglosc_x:
                            if j.x == i + pozycja_poczatkowa_x and j.y == -i + pozycja_poczatkowa_y and j.kolor != figura.kolor:
                                self.wynik = j.zbij()
                                if j.kolor:
                                    self.rozstawienie_Biale.remove(j)
                                    if j in self.Lista_Pionkow_Biale:
                                        self.Lista_Pionkow_Biale.remove(j)
                                else:
                                    self.rozstawienie_Czarne.remove(j)
                                    if j in self.Lista_Pionkow_Czarne:
                                        self.Lista_Pionkow_Czarne.remove(j)
                                if j in self.Lista_Wiez:
                                    self.Lista_Wiez.remove(j)
                                if j in self.Lista_Skoczkow:
                                    self.Lista_Skoczkow.remove(j)
                                if j in self.Lista_Kroli:
                                    self.Lista_Kroli.remove(j)
                                if j in self.Lista_Goncow:
                                    self.Lista_Goncow.remove(j)
                                if j in self.Lista_Hetmanow:
                                    self.Lista_Hetmanow.remove(j)
                                return True
                        

                elif odleglosc_y>0:
                    for j in laczna_lista:
                        if i != odleglosc_x:
                            if j.x == i + pozycja_poczatkowa_x and j.y == i + pozycja_poczatkowa_y:
                                figura.rusz(pozycja_poczatkowa_x,pozycja_poczatkowa_y)
                                return False
                        if i == odleglosc_x:
                            if j.x == i + pozycja_poczatkowa_x and j.y == i + pozycja_poczatkowa_y and j.kolor != figura.kolor:
                                self.wynik = j.zbij()
                                if j.kolor:
                                    self.rozstawienie_Biale.remove(j)
                                    if j in self.Lista_Pionkow_Biale:
                                        self.Lista_Pionkow_Biale.remove(j)
                                else:
                                    self.rozstawienie_Czarne.remove(j)
                                    if j in self.Lista_Pionkow_Czarne:
                                        self.Lista_Pionkow_Czarne.remove(j)
                                if j in self.Lista_Wiez:
                                    self.Lista_Wiez.remove(j)
                                if j in self.Lista_Skoczkow:
                                    self.Lista_Skoczkow.remove(j)
                                if j in self.Lista_Kroli:
                                    self.Lista_Kroli.remove(j)
                                if j in self.Lista_Goncow:
                                    self.Lista_Goncow.remove(j)
                                if j in self.Lista_Hetmanow:
                                    self.Lista_Hetmanow.remove(j)
                                return True
                       
            for i in range(-75,odleglosc_x-75,-75):
                if odleglosc_y < 0:
                    for j in laczna_lista:
                        if i != odleglosc_x:
                            if j.x == i + pozycja_poczatkowa_x and j.y == i + pozycja_poczatkowa_y:
                                figura.rusz(pozycja_poczatkowa_x,pozycja_poczatkowa_y)
                                return False
                        if i == odleglosc_x:
                            if j.x == i + pozycja_poczatkowa_x and j.y == i + pozycja_poczatkowa_y and j.kolor != figura.kolor:
                                self.wynik = j.zbij()
                                if j.kolor:
                                    self.rozstawienie_Biale.remove(j)
                                    if j in self.Lista_Pionkow_Biale:
                                        self.Lista_Pionkow_Biale.remove(j)
                                else:
                                    self.rozstawienie_Czarne.remove(j)
                                    if j in self.Lista_Pionkow_Czarne:
                                        self.Lista_Pionkow_Czarne.remove(j)
                                if j in self.Lista_Wiez:
                                    self.Lista_Wiez.remove(j)
                                if j in self.Lista_Skoczkow:
                                    self.Lista_Skoczkow.remove(j)
                                if j in self.Lista_Kroli:
                                    self.Lista_Kroli.remove(j)
                                if j in self.Lista_Goncow:
                                    self.Lista_Goncow.remove(j)
                                if j in self.Lista_Hetmanow:
                                    self.Lista_Hetmanow.remove(j)
                                return True
                        

                elif odleglosc_y>0:
                    for j in laczna_lista:
                        if i != odleglosc_x:
                            if j.x == i + pozycja_poczatkowa_x and j.y == -i + pozycja_poczatkowa_y:
                                figura.rusz(pozycja_poczatkowa_x,pozycja_poczatkowa_y)
                                return False
                        if i == odleglosc_x:
                            if j.x == i + pozycja_poczatkowa_x and j.y == -i + pozycja_poczatkowa_y and j.kolor != figura.kolor:
                                self.wynik = j.zbij()
                                if j.kolor:
                                    self.rozstawienie_Biale.remove(j)
                                    if j in self.Lista_Pionkow_Biale:
                                        self.Lista_Pionkow_Biale.remove(j)
                                else:
                                    self.rozstawienie_Czarne.remove(j)
                                    if j in self.Lista_Pionkow_Czarne:
                                        self.Lista_Pionkow_Czarne.remove(j)
                                if j in self.Lista_Wiez:
                                    self.Lista_Wiez.remove(j)
                                if j in self.Lista_Skoczkow:
                                    self.Lista_Skoczkow.remove(j)
                                if j in self.Lista_Kroli:
                                    self.Lista_Kroli.remove(j)
                                if j in self.Lista_Goncow:
                                    self.Lista_Goncow.remove(j)
                                if j in self.Lista_Hetmanow:
                                    self.Lista_Hetmanow.remove(j)
                                return True
                        
        else:
            return False
        return True

    def Sprawdzenie_Wieza(self,Rook,ruch_x,ruch_y): # Analogicznie do gonca
        odleglosc_x = ruch_x - Rook.x
        odleglosc_y = ruch_y - Rook.y
        laczna_lista = self.rozstawienie_Biale+self.rozstawienie_Czarne
        if Rook in laczna_lista:
            laczna_lista.remove(Rook)
        else:
            return False
        for i in range(75,odleglosc_x+75,75):
            for j in laczna_lista:
                if i == odleglosc_x:
                    if j.x == i+Rook.x and j.y == odleglosc_y+Rook.y and j.kolor != Rook.kolor:
                        self.wynik = j.zbij()
                        if j.kolor:
                            self.rozstawienie_Biale.remove(j)
                            if j in self.Lista_Pionkow_Biale:
                                self.Lista_Pionkow_Biale.remove(j)
                        else:
                            self.rozstawienie_Czarne.remove(j)
                            if j in self.Lista_Pionkow_Czarne:
                                self.Lista_Pionkow_Czarne.remove(j)
                        if j in self.Lista_Wiez:
                            self.Lista_Wiez.remove(j)
                        if j in self.Lista_Skoczkow:
                            self.Lista_Skoczkow.remove(j)
                        if j in self.Lista_Kroli:
                            self.Lista_Kroli.remove(j)
                        if j in self.Lista_Goncow:
                            self.Lista_Goncow.remove(j)
                        if j in self.Lista_Hetmanow:
                            self.Lista_Hetmanow.remove(j)
                        return True
                if j.x == i+Rook.x and j.y == Rook.y:
                    return False
        for i in range(-75,odleglosc_x-75,-75):
            for j in laczna_lista:
                if i == odleglosc_x:
                    if j.x == i+Rook.x and j.y == odleglosc_y+Rook.y and j.kolor != Rook.kolor:
                        self.wynik = j.zbij()
                        if j.kolor:
                            self.rozstawienie_Biale.remove(j)
                        else:
                            self.rozstawienie_Czarne.remove(j)
                        return True
                if j.x == i+Rook.x and j.y == Rook.y:
                    return False
        for i in range(75,odleglosc_y+75,75):
            for j in laczna_lista:
                if i == odleglosc_y:
                    if j.y == i+Rook.y and j.x == odleglosc_x+Rook.x and j.kolor != Rook.kolor:
                        self.wynik = j.zbij()
                        if j.kolor:
                            self.rozstawienie_Biale.remove(j)
                        else:
                            self.rozstawienie_Czarne.remove(j)
                        return True
                if j.y == i+Rook.y and j.x == Rook.x:
                    return False
        for i in range(-75,odleglosc_y-75,-75):
            for j in laczna_lista:
                if i == odleglosc_y:
                    if j.y == i+Rook.y and j.x == odleglosc_x+Rook.x and j.kolor != Rook.kolor:
                        self.wynik = j.zbij()
                        if j.kolor:
                            self.rozstawienie_Biale.remove(j)
                        else:
                            self.rozstawienie_Czarne.remove(j)
                        return True
                if j.y == i+Rook.y and j.x == Rook.x:
                    return False
        if not Rook.rusz(ruch_x,ruch_y):
            Rook.rusz(ruch_x-odleglosc_x,ruch_y-odleglosc_y)
            return False
        else:
            Rook.rusz(ruch_x-odleglosc_x,ruch_y-odleglosc_y)
        return True

    def Sprawdzenie_Skoczek(self,figura,x,y):
        laczna_lista = self.rozstawienie_Biale+self.rozstawienie_Czarne
        if figura in laczna_lista:
            laczna_lista.remove(figura)
        pozycja_startowa_x = figura.x
        pozycja_startowa_y = figura.y
        if figura.rusz(x,y):
            for i in laczna_lista:
                if bool(re.search("[a-h](.|)[a-h][1-8]",self.aktualny_ruch)): # Sprawdza czy dany skoczek zostac wybrany w notacji szachowej
                    if i in self.Lista_Skoczkow and i.kolor == figura.kolor and i.x != figura.x and i.y != figura.y:
                        if self.zmienne_szachowe_x(self.aktualny_ruch[1]) == pozycja_startowa_x:
                            continue
                        else:
                            figura.rusz(pozycja_startowa_x,pozycja_startowa_y)
                            return False
                elif bool(re.search("[1-8](.|)[a-h][1-8]",self.aktualny_ruch)):# To samo tylko po innych koordynatach
                    if i in self.Lista_Skoczkow and i.kolor == figura.kolor and i.x != figura.x and i.y != figura.y:
                        if self.zmienne_szachowe_y(self.aktualny_ruch[1]) == pozycja_startowa_y:
                            continue
                        else:
                            figura.rusz(pozycja_startowa_x,pozycja_startowa_y)
                            return False
                   
                        
                if i.x == x and i.y == y:
                    if i.kolor == figura.kolor:
                        figura.rusz(pozycja_startowa_x,pozycja_startowa_y)
                        return False
                    else:
                        self.wynik = i.zbij()
                        if i.kolor:
                             self.rozstawienie_Biale.remove(i)
                             if i in self.Lista_Pionkow_Biale:
                                 self.Lista_Pionkow_Biale.remove(i)
                        else:
                             self.rozstawienie_Czarne.remove(i)
                             if i in self.Lista_Pionkow_Czarne:
                                self.Lista_Pionkow_Czarne.remove(i)
                        if i in self.Lista_Wiez:
                             self.Lista_Wiez.remove(i)
                        if i in self.Lista_Skoczkow:
                             self.Lista_Skoczkow.remove(i)
                        if i in self.Lista_Kroli:
                             self.Lista_Kroli.remove(i)
                        if i in self.Lista_Goncow:
                             self.Lista_Goncow.remove(i)
                        if i in self.Lista_Hetmanow:
                             self.Lista_Hetmanow.remove(i)
                        return True
            return True
        else:
            return False

    def Sprawdzanie_roszady(self):
        if self.CW1.x != 0 or self.CW1.y != 0:
            self.CK.roszada_dluga = False
        if self.CW2.x != 525 or self.CW2.y != 0:
            self.CK.roszada_krotka = False
        if self.BW1.x != 0 or self.BW1.y != 525:
            self.BK.roszada_dluga = False
        if self.BW2.x != 525 or self.BW2.y != 525:
            self.BK.roszada_krotka = False

    def Sprawdzenie_Hetmana(self,figura,x,y):
        poczatkowe_x = figura.x
        poczatkowe_y = figura.y
        if figura.rusz(x,y):
            figura.rusz(poczatkowe_x,poczatkowe_y)
            if figura.ruch_gonca:
                if self.Sprawdzenie_Goniec(figura,x,y):
                    return True
                else:
                    return False
            elif figura.ruch_wiezy:
                if self.Sprawdzenie_Wieza(figura,x,y):
                    figura.rusz(x,y)
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def Sprawdzenie_Piona(self,figura,x,y):
        odleglosc_x = figura.x - x
        odleglosc_y = figura.y - y
        laczna_lista = self.rozstawienie_Biale+self.rozstawienie_Czarne
        if figura in laczna_lista:
            laczna_lista.remove(figura)
        if odleglosc_x in [-75,75]:
            if figura.kolor and odleglosc_y == 75:
                for i in laczna_lista:
                    if i in self.Lista_Pionkow_Czarne:
                            if i.podwojny and i.x == x and i.y == 225:
                                figura.rusz(x,y)
                                self.wynik = i.zbij()
                                self.rozstawienie_Czarne.remove(i)
                                if i in self.Lista_Pionkow_Czarne:
                                    self.Lista_Pionkow_Czarne.remove(i)
                                return True
                    if i.x == x and i.y == y and i.kolor != figura.kolor:
                        figura.rusz(x,y)
                        self.wynik = i.zbij()
                        if i.kolor:
                             self.rozstawienie_Biale.remove(i)
                             if i in self.Lista_Pionkow_Biale:
                                 self.Lista_Pionkow_Biale.remove(i)
                        else:
                             self.rozstawienie_Czarne.remove(i)
                             if i in self.Lista_Pionkow_Czarne:
                                self.Lista_Pionkow_Czarne.remove(i)
                        if i in self.Lista_Wiez:
                             self.Lista_Wiez.remove(i)
                        if i in self.Lista_Skoczkow:
                             self.Lista_Skoczkow.remove(i)
                        if i in self.Lista_Kroli:
                             self.Lista_Kroli.remove(i)
                        if i in self.Lista_Goncow:
                             self.Lista_Goncow.remove(i)
                        if i in self.Lista_Hetmanow:
                             self.Lista_Hetmanow.remove(i)
                        return True
                self.tura = not self.tura
                return False
            elif not figura.kolor and odleglosc_y == -75:
                for i in laczna_lista:
                    if i in self.Lista_Pionkow_Biale:
                            if i.podwojny and i.x == x and i.y == 300:
                                figura.rusz(x,y)
                                self.wynik = i.zbij()
                                self.rozstawienie_Biale.remove(i)
                                if i in self.Lista_Pionkow_Biale:
                                    self.Lista_Pionkow_Biale.remove(i)
                                return True
                    if i.x == x and i.y == y:
                        figura.rusz(x,y)
                        self.wynik = i.zbij()
                        if i.kolor:
                             self.rozstawienie_Biale.remove(i)
                             if i in self.Lista_Pionkow_Biale:
                                 self.Lista_Pionkow_Biale.remove(i)
                        else:
                             self.rozstawienie_Czarne.remove(i)
                             if i in self.Lista_Pionkow_Czarne:
                                self.Lista_Pionkow_Czarne.remove(i)
                        if i in self.Lista_Wiez:
                             self.Lista_Wiez.remove(i)
                        if i in self.Lista_Skoczkow:
                             self.Lista_Skoczkow.remove(i)
                        if i in self.Lista_Kroli:
                             self.Lista_Kroli.remove(i)
                        if i in self.Lista_Goncow:
                             self.Lista_Goncow.remove(i)
                        if i in self.Lista_Hetmanow:
                             self.Lista_Hetmanow.remove(i)
                        return True
                self.tura = not self.tura
                return False
            else:
                self.tura = not self.tura
                return False
        else:
            self.tura = not self.tura
            return False   

    def Sprawdzenie_Krola(self,figura,x,y):
        lista_laczna = self.rozstawienie_Biale + self.rozstawienie_Czarne
        if figura in lista_laczna:
            lista_laczna.remove(figura)
        for i in lista_laczna:
                if i.kolor and i.x == x and i.y == y:
                    return False
        if figura.rusz(x,y):
            for i in lista_laczna:
                if i.x == figura.x and i.y == figura.y:
                    self.wynik = i.zbij()
                    if i.kolor:
                             self.rozstawienie_Biale.remove(i)
                             if i in self.Lista_Pionkow_Biale:
                                 self.Lista_Pionkow_Biale.remove(i)
                    else:
                             self.rozstawienie_Czarne.remove(i)
                    if i in self.Lista_Pionkow_Czarne:
                                self.Lista_Pionkow_Czarne.remove(i)
                    if i in self.Lista_Wiez:
                             self.Lista_Wiez.remove(i)
                    if i in self.Lista_Skoczkow:
                             self.Lista_Skoczkow.remove(i)
                    if i in self.Lista_Kroli:
                             self.Lista_Kroli.remove(i)
                    if i in self.Lista_Goncow:
                             self.Lista_Goncow.remove(i)
                    if i in self.Lista_Hetmanow:
                             self.Lista_Hetmanow.remove(i)
                    return True
            return True
        else:
            return False

    def reset_bicia(self,zmienna):
        if zmienna:
            for i in self.Lista_Pionkow_Biale:
                i.podwojny = False
        else:
            for i in self.Lista_Pionkow_Czarne:
                i.podwojny = False

    def sprawdzenie(self,figura,x,y):           # Sprawdza jaka figure chce ruszyc uzytkownik
        zrobione = 0
        if self.tura: # Sprawdza czyja tura
                if bool(re.search(figura,"abcdefgh")):
                    for i in self.Lista_Pionkow_Biale:
                        if self.zmienne_szachowe_x(figura) == i.x:
                            if self.Sprawdzenie_Piona(i,x,y):
                                return True
                    return False
                if figura == "K":
                    if self.Sprawdzenie_Krola(self.BK,x,y):
                        return True
                    else:
                        self.tura = not self.tura
                        return False
                if figura == "H" or figura == "Q":
                    if self.Sprawdzenie_Hetmana(self.BH,x,y):
                        self.BH.ruch_gonca = False
                        self.BH.ruch_wiezy = False
                        return True
                    else:
                        self.tura = not self.tura
                        self.BH.ruch_gonca = False
                        self.BH.ruch_wiezy = False
                        return False
                if figura == "G" or figura == "B": # Warunek na gonca
                    if self.Sprawdzenie_Goniec(self.BG1,x,y) or self.Sprawdzenie_Goniec(self.BG2,x,y):
                        return True
                    else:
                        self.tura = not self.tura
                        return False
                if figura == "W" or figura == "R": # Warunek na wieze
                    if self.Sprawdzenie_Wieza(self.BW1,x,y) or self.Sprawdzenie_Wieza(self.BW2,x,y):
                        if bool(re.search("[a-h][a-h]",self.aktualny_ruch)):# Sprawdza czy uzytkownik podal ktora wieza chce ruszyc jak obie sa na tej samej linii
                            for i in self.Lista_Wiez:
                                if i.x == self.zmienne_szachowe_x(self.aktualny_ruch[len(self.aktualny_ruch)-3]) and i.kolor:
                                    i.rusz(x,y)
                                    zrobione = 1
                            if not zrobione:
                                self.tura = not self.tura
                                return False
                        elif bool(re.search("[1-8][a-h]",self.aktualny_ruch)):
                            for i in self.Lista_Wiez:
                                if i.y == self.zmienne_szachowe_y(self.aktualny_ruch[len(self.aktualny_ruch)-3]) and i.kolor:
                                    i.rusz(x,y)
                                    zrobione = 1
                            if not zrobione:
                                self.tura = not self.tura
                                return False

                        else:
                            u1 = self.BW1.x
                            u2 = self.BW2.x
                            v1 = self.BW1.y
                            v2 = self.BW2.y

                            try:
                                ruszenie1 = self.BW1.rusz(x,y)
                                ruszenie2 = self.BW2.rusz(x,y)
                                if ruszenie1 == ruszenie2: # Sprawdza czy obie wieze chca wejsc na to samo pole
                                    raise Niejednoznaczne
                            except:
                                self.tura = not self.tura
                                self.BW1.rusz(u1,v1)
                                self.BW2.rusz(u2,v2)
                                return False 
                    else:
                        self.tura = not self.tura
                        return False
                elif figura == "N" or figura == "S":
                    if self.Sprawdzenie_Skoczek(self.BS1,x,y) or self.Sprawdzenie_Skoczek(self.BS2,x,y):
                        return True
                    else:
                        self.tura = not self.tura
                        return False
        else:
                if bool(re.search(figura,"abcdefgh")):
                    for i in self.Lista_Pionkow_Czarne:
                        if self.zmienne_szachowe_x(figura) == i.x:
                            if self.Sprawdzenie_Piona(i,x,y):
                                return True
                    return False
                if figura == "K":
                    if self.Sprawdzenie_Krola(self.CK,x,y):
                        return True
                    else:
                        self.tura = not self.tura
                        return False
                if figura == "H" or figura == "Q":
                    if self.Sprawdzenie_Hetmana(self.CH,x,y):
                        self.CH.ruch_gonca = False
                        self.CH.ruch_wiezy = False
                        return True
                    else:
                        self.tura = not self.tura
                        self.CH.ruch_gonca = False
                        self.CH.ruch_wiezy = False
                        return False
                if figura == "G" or figura == "B":
                    if self.Sprawdzenie_Goniec(self.CG1,x,y) or self.Sprawdzenie_Goniec(self.CG2,x,y):
                        return True
                    else:
                        self.tura = not self.tura
                        return False
                if figura == "W" or figura == "R":
                    if self.Sprawdzenie_Wieza(self.CW1,x,y) or self.Sprawdzenie_Wieza(self.CW2,x,y):
                        if bool(re.search("[a-h][a-h]",self.aktualny_ruch)):
                            for i in self.Lista_Wiez:
                                if i.x == self.zmienne_szachowe_x(self.aktualny_ruch[len(self.aktualny_ruch)-3]) and not i.kolor:
                                    i.rusz(x,y)
                                    zrobione = 1
                            if not zrobione:
                                self.tura = not self.tura
                                return False
                                
                        elif bool(re.search("[1-8][a-h]",self.aktualny_ruch)):
                            for i in self.Lista_Wiez:
                                if i.y == self.zmienne_szachowe_y(self.aktualny_ruch[len(self.aktualny_ruch)-3]) and not i.kolor:
                                    i.rusz(x,y)
                                    zrobione = 1
                            if not zrobione:
                                self.tura = not self.tura
                                return False
                                
                        else:
                            u1 = self.CW1.x
                            u2 = self.CW2.x
                            v1 = self.CW1.y
                            v2 = self.CW2.y

                            try:
                                ruszenie1 = self.CW1.rusz(x,y)
                                ruszenie2 = self.CW2.rusz(x,y)
                                if ruszenie1 == ruszenie2:
                                    raise Niejednoznaczne
                            except:
                                self.tura = not self.tura
                                self.CW1.rusz(u1,v1)
                                self.CW2.rusz(u2,v2)
                                return False
                    else:
                        self.tura = not self.tura
                        return False
                elif figura == "N" or figura == "S":
                    if self.Sprawdzenie_Skoczek(self.CS1,x,y) or self.Sprawdzenie_Skoczek(self.CS2,x,y):
                        return True
                    else:
                        self.tura = not self.tura
                        return False
        return True
    
    def ruch_figury(self): # Zczytuje od uzytkownika jaki ruch ma wykonac i go sprawdza
        if self.aktualny_ruch[len(self.aktualny_ruch) - 2] == "=" and self.aktualny_ruch[len(self.aktualny_ruch) - 3] == "8":
            figura = self.aktualny_ruch[0]
            y = self.aktualny_ruch[len(self.aktualny_ruch) - 1]
            x = self.aktualny_ruch[len(self.aktualny_ruch) - 2]
            x = self.zmienne_szachowe_x(x)
            y = self.zmienne_szachowe_y(y)
            if self.sprawdzenie(figura,x,y):
                self.promocja(figura)
                return True
            else:
                y = self.aktualny_ruch[1]
                x = self.aktualny_ruch[0]
                x = self.zmienne_szachowe_x(x)
                y = self.zmienne_szachowe_y(y)
                if not self.tura:
                    laczna_lista = self.rozstawienie_Biale + self.rozstawienie_Czarne
                    for i in self.Lista_Pionkow_Czarne:
                        if i.x == x:
                            ix = i.x
                            iy = i.y
                            if i in laczna_lista:
                                laczna_lista.remove(i)
                            if i.rusz(x,y):

                                for j in laczna_lista:
                                        if j.x == i.x and i.y == j.y:
                                            i.x = ix 
                                            i.y = iy
                                            self.tura = not self.tura
                                            return False
                                        self.promocja(i)
                            else:
                                i.x = ix 
                                i.y = iy
                                self.tura = not self.tura
                                return False
                    return True
                else:
                    laczna_lista = self.rozstawienie_Biale + self.rozstawienie_Czarne
                    for i in self.Lista_Pionkow_Biale:
                        if i.x == x:
                            ix = i.x
                            iy = i.y
                            if i in laczna_lista:
                                laczna_lista.remove(i)
                            if i.rusz(x,y):
                                for j in laczna_lista:
                                        if j.x == i.x and i.y == j.y:
                                            i.x = ix 
                                            i.y = iy
                                            self.tura = not self.tura
                                            return False
                                        else:
                                            self.promocja(i)
                            else:
                                i.x = ix 
                                i.y = iy
                                self.tura = not self.tura
                                return False
                    return True
        elif self.aktualny_ruch == "O-O":
            if self.roszada_krotka():
                return True
            else:
                return False
        elif self.aktualny_ruch == "O-O-O":
            if self.roszada_dluga():
                return True
            else:
                return False
        elif len(self.aktualny_ruch) > 2:
           figura = self.aktualny_ruch[0]
           y = self.aktualny_ruch[len(self.aktualny_ruch) - 1]
           x = self.aktualny_ruch[len(self.aktualny_ruch) - 2]
           x = self.zmienne_szachowe_x(x)
           y = self.zmienne_szachowe_y(y)
           if self.sprawdzenie(figura,x,y):
                return True
           else:
                return False
        elif len(self.aktualny_ruch) == 2:
            y = self.aktualny_ruch[1]
            x = self.aktualny_ruch[0]
            x = self.zmienne_szachowe_x(x)
            y = self.zmienne_szachowe_y(y)
            if not self.tura:
                laczna_lista = self.rozstawienie_Biale + self.rozstawienie_Czarne
                for i in self.Lista_Pionkow_Czarne:
                    if i.x == x:
                        ix = i.x
                        iy = i.y
                        if i in laczna_lista:
                            laczna_lista.remove(i)
                        if i.rusz(x,y):
                            for j in laczna_lista:
                                if i.podwojny:
                                        if (j.y == i.y or j.y == i.y-75) and i.x == j.x:
                                            i.x = ix 
                                            i.y = iy
                                            self.tura = not self.tura
                                            return False
                                else:
                                        if j.x == i.x and i.y == j.y:
                                            i.x = ix 
                                            i.y = iy
                                            self.tura = not self.tura
                                            return False
                        else:
                            i.x = ix 
                            i.y = iy
                            self.tura = not self.tura
                            return False
                return True
            else:
                laczna_lista = self.rozstawienie_Biale + self.rozstawienie_Czarne
                for i in self.Lista_Pionkow_Biale:
                    if i.x == x:
                        ix = i.x
                        iy = i.y
                        if i in laczna_lista:
                            laczna_lista.remove(i)
                        if i.rusz(x,y):
                            for j in laczna_lista:
                                if i.podwojny:
                                        if (j.y == i.y or j.y == i.y+75) and i.x == j.x:
                                            i.x = ix 
                                            i.y = iy
                                            self.tura = not self.tura
                                            return False
                                else:
                                        if j.x == i.x and i.y == j.y:
                                            i.x = ix 
                                            i.y = iy
                                            self.tura = not self.tura
                                            return False
                        else:
                            i.x = ix 
                            i.y = iy
                            self.tura = not self.tura
                            return False
                return True

    def koniec_gry(self):
        if self.wynik != "*":
            return True
        else:
            return False

    def on_event(self, event):                      # Funkcja moniturujaca dzialania uzytkownika
        if event.type == pygame.QUIT:               # Uzytkownik wychodzi z okna
            self._running = False                   # Zamykanie programu
        if event.type == pygame.MOUSEBUTTONDOWN:    # Sprawdza przycisk myszy
            if self._wejscie_box.collidepoint(event.pos):   # Jezli klikniecie bylo w pole to aktywuje pole
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive # Zmiana koloru pola 
        if event.type == pygame.KEYDOWN and not self.koniec_gry():            # Uzytkownik klika przycisk na klawiaturze
            if self.active:                         # Jezli pole jest klikniete
                if event.key == pygame.K_RETURN:    # Jezli przycisk to Enter
                    print(len(self.Lista_Pionkow_Biale))
                    print(len(self.Lista_Pionkow_Czarne))
                    print(self.text)                # Wyswietla wpisany tekst
                    self.aktualny_ruch = self.text  # Zapisuje tekst do weryfikacji ruchu
                    if self.ruch_figury():              # Wykonanie funkcji do ruszania figurami
                        self.zapis_ruchow += "{} ".format(self.text)    # Zapis do pliku partii
                        self.licznik += 1     
                    self.text = ''                  # Reset boxa z tekstem
                    if self.licznik == 2:           # Jesli licznik jest na 2 to jest kolejny ruch
                            self.licznik = 0        # bo jeden ruch dzieli sie na ruch bialych i czarnych w zapisie
                            self.ruch += 1          # inkrementacja ruchu
                            self.zapis_ruchow += str(self.ruch)+". "    # dodanie numeru ruchu do pliku
                    self.tura = not self.tura       # Zmiana tury
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]      # Cofa litery
                else:
                    self.text += event.unicode      # Odpowiedzialne za dopisywanie liter
           
    def on_loop(self):                              # funkcja w petli
        font = pygame.font.SysFont("arial", 22)     # Ustawienie czcionki
        self._display_surf.fill((30, 30, 30))       
        self._display_surf.blit(self.Deseczka,(0,0)) # Wyswietlanie obszaru dookola deski
        self.txt_surface = font.render(self.text, True, self.color) # Tworzenie powierzchni na tekst
        if self.tura:
            self._display_surf.blit(self.ruchB,(525,625)) # Znacznik ruchu
        else:
            self._display_surf.blit(self.ruchC,(525,625))
        self._display_surf.blit(self.Deska,(0,0)) # Rysowanie deski
        for i in self.Lista_Kroli:
            if i.szach:
                self._display_surf.blit(self.szachy,(i.x,i.y))
        for i in self.rozstawienie_Biale+self.rozstawienie_Czarne:
            if not i.zbite:
                self._display_surf.blit(i.rook,(i.x,i.y)) # Rysowanie niezbitych figur
        self._display_surf.blit(self.txt_surface, (self._wejscie_box.x+5, self._wejscie_box.y+5)) # Rysowanie tekstu
        pygame.draw.rect(self._display_surf, self.color, self._wejscie_box, 2) # Rysowanie pola na tekst

    def on_render(self):
        self.Sprawdzanie_roszady()
        self.reset_bicia(self.tura)
        pygame.display.update() # odswiezanie obrazu

    def on_cleanup(self): # czyszczenie
        self.plik.write("""[Event "Projekt Python"]
[Site "put.poznan.pl"] 
[Date \""""+ str(self.data.strftime("%d.%m.%Y %H:%M:%S"))+"""\"]
[White "Gracz1"]
[Black "Gracz2"]
[Result \"""" + str(self.wynik) +"""\"]
[Variant "Standard"]

""") # Ten zapis pozwala na wklejenie do stron typu chess.com lichess.org
        self.plik.write(self.zapis_ruchow) # Dodaje ruchy do pliku
        self.plik.close() # zamyka plik
        pygame.quit() # konczy okienko pygame
    
    def on_execute(self): # Glowny plik odpowiedzialny za dzialanie programu
        clock = pygame.time.Clock() # Tworzenie zegara
        if self.on_init() == False:
            self._running = False
        self.rozstawienie_figur()
 
        while( self._running ): # Glowna petla
            clock.tick(self.FPS) # Ustawianie predkosci odswiezania na 30 klatek na sekunde
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            
        self.on_cleanup()
 
if __name__ == "__main__" : # a tu mainik
    theApp = Deska()
    theApp.on_execute()
