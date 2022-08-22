import pygame
import os
import random


# Odpalenie gry
pygame.init()




### PODSTAWOWA OBSLUGA GRY, DEKLARACJA ZMIENNYCH ###


# Potki
czas_potka = 0 #odliczanie czasu dla spawnowania potek
losuj_potke = False #czy jest czas na losowanie potki?
potka_spawn = 1000 #czas do zespawnowania pierwszej potki
potki = []

# Wrogowie (potwory)
typ_potwora = 0 #poczatkowy typ potwora
typy = 0 #ile typow losujemy
czas_potwory = 0 #aby liczyc czas od spawna
spawn_time = 500  # czas do zespawnowania potwora
czas_spawn0 = 100  # do kontroli czasu
czas_spawn1 = 200
jednorazowe = False # pomocnicza zmienna do spawnowania potworow
wrogowie = []
zabici = 0

# Dzialanie
dziala = True #definiuje, ze gra dziala (jest wlaczona)
intro = True #czy gra jest w trybie intro?
wyciszenie = False #czy gra jest wyciszona?
stop = False #czy gra jest w trybie stop (gameover)?
wiezaZycia = 10
level = 1
czasogolny=0 #do liczenia ogólnego czasu gry
ostczasogolny=0




### GRAFIKA I DZWIEK ###


# Szerokosc, wysokosc okna
okno_szer = 1300
okno_wys = 500
okno = pygame.display.set_mode((okno_szer,okno_wys))

# Wgranie obrazkow jako tla gry
obraztla = pygame.image.load(os.path.join("tla", 'tlo4.png')) # Tło podstaowe
tlo1 =  pygame.transform.scale(obraztla,(okno_szer,okno_wys)) # Przeskalowanie
tlo2 =  pygame.image.load(os.path.join("tla", 'intro3.png')) # Tlo do intro
gameover = pygame.image.load(os.path.join("tla", 'gameover.png')) # Tlo do gameovera

# Tytul na oknie gry
pygame.display.set_caption("Mage Tower Siege")

# Wieza magow
wieza = pygame.image.load(os.path.join("tla", "wieza2.png"))


# Dzwieki
muzyka = pygame.mixer.music.load(os.path.join("dzwieki", "obogowiewalka.mid"))
pygame.mixer.music.play(-1)  # robi petle muzyczna
kulaognia_dzwiek = pygame.mixer.Sound(os.path.join("dzwieki", "kula ognia.flac"))
#kulaognia_hit = pygame.mixer.Sound(os.path.join("dzwieki", "kula ognia hit.flac"))
piorun_dzwiek = pygame.mixer.Sound(os.path.join("dzwieki", "piorun.flac"))
smiercGoblina_dzwiek = pygame.mixer.Sound(os.path.join("dzwieki", "smierc goblina.flac"))
smiercGrzyba_dzwiek = pygame.mixer.Sound(os.path.join("dzwieki", "smierc grzyb.flac"))
smiercOka_dzwiek=pygame.mixer.Sound(os.path.join("dzwieki", "smierc oko.flac"))
wiezatraci_dzwiek = pygame.mixer.Sound(os.path.join("dzwieki", "strata wieza.flac"))


# Wgranie obrazkow - Pociski
kulaognia_img= pygame.image.load(os.path.join("kula ognia\prawa", "kulapr5.png")) #os.path.join laczy skad pobrac - folderglowny/folder_join/plik
kulaognia_imgrev= pygame.image.load(os.path.join("kula ognia\lewa", "kulale5.png"))#!!dalem najladniejsza na teraz, moze wiesz jak zrobic gif?
piorun_img=pygame.image.load(os.path.join("piorun", "piorunp.png"))
piorun_imgrev=pygame.image.load(os.path.join("piorun", "piorunl.png"))


# Wgranie obrazków - Bohater

stanie_p = [None]*7 # Animacja stania
for nranimacji in range(1, 7):
    stanie_p[nranimacji-1] = pygame.image.load(os.path.join("bohater", "S" + str(nranimacji) + ".png"))
    nranimacji+=1
# <- Z folderu "bohater" bierzemy po kolei obrazki o nazwie "S" i <nr obrazka> i ".png"; analogicznie dla pozostalych animacji

stanie_l = [None]*7
for nranimacji in range(1, 7):
    stanie_l[nranimacji-1] = pygame.image.load(os.path.join("bohater", "SL" + str(nranimacji) + ".png"))
    nranimacji+=1

prawo = [None]*9
for nranimacji in range(1, 9):
    prawo[nranimacji-1] = pygame.image.load(os.path.join("bohater", "R" + str(nranimacji) + ".png"))
    nranimacji+=1

lewo = [None]*9
for nranimacji in range(1, 9):
    lewo[nranimacji-1] = pygame.image.load(os.path.join("bohater", "L" + str(nranimacji) + ".png"))
    nranimacji+=1

skok_p = [None]*3
for nranimacji in range(1, 3):
    skok_p[nranimacji-1] = pygame.image.load(os.path.join("bohater", "JGP" + str(nranimacji) + ".png"))
    nranimacji+=1

skok_l = [None]*3
for nranimacji in range(1, 3):
    skok_l[nranimacji-1] = pygame.image.load(os.path.join("bohater", "JGL" + str(nranimacji) + ".png"))
    nranimacji+=1


# Wgranie obrazków - Wrogowie i potki

grzyb_ruch = [None]*17
for nranimacji in range(1, 17):
    grzyb_ruch[nranimacji-1] = pygame.image.load(os.path.join("grzyb", "R" + str(nranimacji) + ".png"))
    nranimacji+=1

oko_ruch = [None] * 17
for nranimacji in range(1, 17):
    oko_ruch[nranimacji - 1] = pygame.image.load(os.path.join("oko", "R" + str(nranimacji) + ".png"))
    nranimacji += 1

goblin_ruch = [None] * 9
for nranimacji in range(1, 9):
    goblin_ruch[nranimacji - 1] = pygame.image.load(os.path.join("goblin", "R" + str(nranimacji) + ".png"))
    nranimacji += 1

potka_animacja = [None]*9
for nranimacji in range(1, 9):
    potka_animacja[nranimacji - 1] = pygame.image.load(os.path.join("potka", "potka" + str(nranimacji) + ".png"))
    nranimacji += 1



### KLASA BOHATERA ###


class Bohater:

    def __init__(self, x, y): # Ustawienie poczatkowych metod klasy Bohater, ktore od razu sie wywolaja
        # Ruch prawo / lewo
        self.x = x  #poczatkowe koordynaty
        self.y = y
        self.velx = 10  #predkosci w odpowiednich osiach
        self.vely = 10
        self.patrzy_prawo = True  #w ktora strone patrzy
        self.patrzy_lewo = False
        # Animacja ruchu
        self.nrkroku = 0  #do zmieniania kroku
        self.nrlotu = 0  #do zmieniania "fazy lotu"
        self.nrstania = 0 #do zmieniania animacji stania
        self.ostruch = 0 #zmienna pomocniczna aby wiedziec, w ktora strone poprzednio byl zwrocony bohater
        # Skok
        self.skok = False
        # Kule
        self.kuleognia = []
        self.licznik_kula_ognia = 0
        # Pioruny
        self.pioruny = []
        self.licznik_piorun = 0
        # Zycie
        self.hitbox = pygame.Rect(self.x, self.y, 65, 90)
        self.health = 100
        self.lives = 1
        self.czyZyje = True


    def ruch_bohatera(self, wcisniecie): #Kontrola ruchu

        if wcisniecie[pygame.K_RIGHT] and self.x <= 1200:  #win_width - 62 <- jesli chcemy ustawic w zaleznosci od okna
            self.x += self.velx # poruszanie sie z predkoscia velx
            self.patrzy_prawo = True
            self.patrzy_lewo = False

        elif wcisniecie[pygame.K_LEFT] and self.x >= 50:
            self.x -= self.velx
            self.patrzy_prawo = False
            self.patrzy_lewo = True

        else: #reset
            self.patrzy_lewo = False
            self.patrzy_prawo = False
            self.nrkroku = 0

        # Skok
        if wcisniecie[pygame.K_UP] and self.skok is False:
            self.skok = True
        if self.skok:
            self.y -= self.vely * 4
            self.vely -= 1
        if self.vely < -10:
            self.skok = False
            self.vely = 10


    def draw(self, okno): #Wyswietlanie grafiki i animacja

        player.hitbox = pygame.Rect(self.x + 80, self.y + 55, 65, 90)
        #pygame.draw.rect(okno, (0, 0, 0), player.hitbox, 1) <-- do testowania
        pygame.draw.rect(okno, (255, 76, 76), (self.x + 60, self.y + 20, 100, 10)) # Zycie - x,y pozycja, 50,10 - szerokosc i wysokosc paska
        pygame.draw.rect(okno, (159, 173, 189), (self.x + 60, self.y + 5, 100, 10))  # Mana
        if self.health >= 0:
            pygame.draw.rect(okno, (52, 191, 73), (self.x + 60, self.y + 20, self.health, 10))
        if self.licznik_piorun > 0 and self.licznik_piorun <100:
            pygame.draw.rect(okno, (0, 153, 229), (self.x + 60, self.y + 5, self.licznik_piorun, 10))
        elif self.licznik_piorun == 0:
            pygame.draw.rect(okno, (0, 153, 229), (self.x + 60, self.y + 5, 100, 10))

        if self.nrkroku >= 8*2: #8 (klatek animacji) * 2 (klatki na odswiezenie) aby bylo bardziej plynnie
            self.nrkroku = 0 # po odwtowrzeniu wszystkich klatek resetujemy od poczatku, analogicznie dla pozostalych animacji
        if self.nrlotu >= 2 * 2:
            self.nrlotu = 0
        if self.nrstania >= 6*4:
            self.nrstania = 0
        if self.patrzy_lewo:
            if self.skok: #dodane aby sprawdzic ktory obrazek skoku (w lewo czy w prawo) uzyc
                okno.blit(skok_l[self.nrlotu // 2], (self.x, self.y)) #ktory nr obrazka pokazac w oknie z grafiki lewo, dzielimy przez 2 bo mamy te 2 klatki odscwiezania, w koodynatach self.x i self.y
                self.nrlotu += 1 #przewijamy nr obrazka z animacji (tutaj faza, pózniej np. krok) o 1
            else: #analogicznie dla pozostalych animacji
                okno.blit(lewo[self.nrkroku//2], (self.x, self.y))
                self.nrkroku += 1
            self.ostruch = 1
        if self.patrzy_prawo:
            if self.skok:
                okno.blit(skok_p[self.nrlotu // 2], (self.x, self.y))
                self.nrlotu += 1
            else:
                okno.blit(prawo[self.nrkroku//2], (self.x, self.y))
                self.nrkroku += 1
            self.ostruch = 0
        if (self.patrzy_lewo == False) and (self.patrzy_prawo == False) and (self.ostruch == 0): #warunek aby sprawdzic w ktora strone jest skierowany czarodziej
            okno.blit(stanie_p[self.nrstania // 4], (self.x, self.y))
            self.nrstania += 1
        if (self.patrzy_lewo == False) and (self.patrzy_prawo == False) and (self.ostruch == 1):
            okno.blit(stanie_l[self.nrstania // 4], (self.x, self.y))
            self.nrstania += 1


    def kierunek(self): #Robione po to, zeby strzelal w dobra strone. Domyslnie ma wartosc 1, bo postac jest zwrocona w prawo
        if self.patrzy_prawo:
            return 1
        if self.patrzy_lewo:
            return -1
        if (self.patrzy_lewo == False) and (self.patrzy_prawo == False) and (
                self.ostruch == 0):  # warunek aby sprawdzic w ktora strone jest skierowany czarodziej
            return 2
        if (self.patrzy_lewo == False) and (self.patrzy_prawo == False) and (self.ostruch == 1):
            return -2


    def kulaognia_uzycie(self):
        self.hit()
        self.cd_kulaognia()
        if wcisniecie[pygame.K_SPACE] and self.licznik_kula_ognia == 0:
            if wyciszenie == False:
                kulaognia_dzwiek.play()
            kulaognia = Kulaognia(self.x , self.y, self.kierunek())
            self.kuleognia.append(kulaognia)
            self.licznik_kula_ognia = 1 #dodajemy 1 do licznika
        for kulaognia in self.kuleognia:
            kulaognia.ruch() #tworzymy funkcje ruch w klasie kuli ognia, zeby kula sie ruszala
            if kulaognia.poza_oknem(): #dodany warunek, zeby nie przeciazac pamieci - usuwanie z listy kuli ognia
                self.kuleognia.remove(kulaognia)

    def cd_kulaognia(self): #robimy licznik zeby za czesto nie atakowac kulami ognistymi
        if self.licznik_kula_ognia >= 10:
            self.licznik_kula_ognia = 0
        elif self. licznik_kula_ognia > 0:
            self.licznik_kula_ognia +=1

    def hit(self):
        for wrog in wrogowie: #dla kazdego obecnego na ekrenia wroga
            for kulaognia in self.kuleognia: #dla kazdej kuli
                if kulaognia.hitbox.colliderect(wrog.hitbox):
                    wrog.health -= 5
                    self.kuleognia.remove(kulaognia)


    def piorun_uzycie(self):
        self.hit_piorun()
        self.cd_piorun()
        if wcisniecie[pygame.K_z] and self.licznik_piorun == 0:
            piorun = Piorun(self.x, self.y, self.kierunek())
            if wyciszenie == False:
                piorun_dzwiek.play()
            self.pioruny.append(piorun)
            self.licznik_piorun = 1  # dodajemy 1 do licznika
        for piorun in self.pioruny:
            piorun.ruch()  # tworzymy funkcje ruch w klasie kuli ognia, zeby kula sie ruszala
            if piorun.poza_oknem():  # dodany warunek, zeby nie przeciazac pamieci - usuwanie z listy kuli ognia
                self.pioruny.remove(piorun)

    def cd_piorun(self):  # robimy licznik zeby za czesto nie atakowac kulami ognistymi siarczystymi
        if self.licznik_piorun >= 100:
            self.licznik_piorun = 0
        elif self.licznik_piorun > 0:
            self.licznik_piorun += 0.5

    def hit_piorun(self):
        for wrog in wrogowie: #dla kazdego obecnego na ekrenia wroga
                for piorun in self.pioruny: #dla kazdego pioruna
                    if piorun.hitbox.colliderect(wrog.hitbox):
                    #if wrog.hitbox[0] < piorun.x < wrog.hitbox[0] + wrog.hitbox[2] and wrog.hitbox[1] < piorun.y < wrog.hitbox[1] + wrog.hitbox[3] or (wrog.hitbox[0] < piorun.x + 600 < wrog.hitbox[0] + wrog.hitbox[2] and wrog.hitbox[1] < piorun.y + 50 < wrog.hitbox[1] + wrog.hitbox[3]): #jezeli hitboxy wroga i pioruna sie pokryja
                        wrog.health -= 1.25




### KLASY ATAKOW ###


class Kulaognia:

    def __init__(self,x,y, kierunek): #pozycja pojawiania sie kuli ognia
        self.kierunek = kierunek
        self.x = x + 120
        self.y = y + 70
        self.hitbox = pygame.Rect(self.x, self.y, 54, 23)
        if self.kierunek == 1 or self.kierunek == 2: #gdy kierunek mamy o wartosci 1 lub 2 to kula ognia wychodzi bardziej z przodu "z reki"
            self.x= x + 120
            self.y= y + 70
        if self.kierunek ==-1 or self.kierunek ==-2: #gdy kierunek mamy o wartosci -1 lub -2 to kula ognia wychodzi lepiej z reki do tylu
            self.x = x + 60
            self.y = y + 70

    def draw_kulaognia(self): #jak odpowiednia wartosc kierunku jest spelniona, wtedy rysuje w jedna albo druga strone kule ognia
        self.hitbox = pygame.Rect(self.x, self.y, 54, 23)
        if  self.kierunek ==1 or self.kierunek == 2:
            okno.blit(kulaognia_img, (self.x, self.y))
        if self.kierunek ==-1 or self.kierunek ==-2:
            okno.blit(kulaognia_imgrev, (self.x, self.y)) #podaje kordy bohatera do metody __init__ i rysuje kule ognia

    def ruch(self): # Chcemy korzystajac z odczytania kierunku ruchu bohatera zeby albo pocisk sie "oddalal" albo lecial do przodu.
        if self.kierunek ==1:
            self.x += 20
        if self.kierunek ==-1:
            self.x -= 20
        if self.kierunek == 2:
            self.x += 20
        if self.kierunek == -2:
            self.x -= 20

    def poza_oknem(self): #potrzebne, zeby usuwac z pamieci niepotrzebne pociski gdy wyjda poza ekran
        return not(self.x>=-10 and self.x<=okno_szer+10)


class Piorun:

    def __init__(self,x,y, kierunek): #pozycja pojawiania pioruna
        self.kierunek = kierunek
        self.x = x + 120
        self.y = y + 75
        self.hitbox = pygame.Rect(self.x, self.y, 600, 50)
        if self.kierunek == 1 or self.kierunek == 2: #gdy kierunek mamy o wartosci 1 lub 2 to piorun wychodzi bardziej z przodu "z reki"
            self.x= x + 120
            self.y= y + 75
        if self.kierunek ==-1 or self.kierunek ==-2: #gdy kierunek mamy o wartosci -1 lub -2 to piorun wychodzi lepiej z reki do tylu
            self.x = x + 60
            self.y = y + 75

    def draw_piorun(self): #jak odpowiednia wartosc kierunku jest spelniona, wtedy rysuje w jedna albo druga strone piorun
        self.hitbox = pygame.Rect(self.x, self.y, 600, 50)
        if  self.kierunek ==1 or self.kierunek == 2:
            okno.blit(piorun_img, (self.x, self.y))
        if self.kierunek ==-1 or self.kierunek ==-2:
            okno.blit(piorun_imgrev, (self.x-450, self.y)) #podaje kordy bohatera do metody __init__ i rysuje piorun

    def ruch(self): # Chcemy korzystajac z odczytania kierunku ruchu bohatera zeby albo pocisk sie "oddalal" albo lecial do przodu.
        if self.kierunek ==1:
            self.x += 30
        if self.kierunek ==-1:
            self.x -= 30
        if self.kierunek == 2:
            self.x += 30
        if self.kierunek == -2:
            self.x -= 30

    def poza_oknem(self): #potrzebne, zeby usuwac z pamieci niepotrzebne pociski gdy wyjda poza ekran
        return not(self.x>=-500 and self.x<=okno_szer)



### KLASY POTEK I POTWOROW ###

class Potka:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.nranimacji = 0
        self.czyuzyta = False
        self.hitbox = pygame.Rect(self.x+10, self.y+10, 40, 40)

    def draw(self, okno):
        self.ruch()
        okno.blit(potka_animacja[self.nranimacji // 3], (self.x, self.y))
        self.nranimacji +=1
        self.hitbox = pygame.Rect(self.x + 10, self.y + 10, 40, 40)
        #pygame.draw.rect(okno, (0, 0, 0), self.hitbox, 1)

    def ruch(self):
        if self.nranimacji >= 8*3:
            self.nranimacji = 0
        self.uzycie()

    def uzycie(self):
        for potka in potki:
            if player.hitbox.colliderect(potka.hitbox):
                player.health = 100
                self.czyuzyta = True



class Grzyb:

    def __init__(self, x, y):
        self.x = x #gdzie sie pojawia na poczatku
        self.y = y
        self.nrkrokuataku = 0 #do animacji
        # Zycie
        self.hitbox = pygame.Rect(self.x+145, self.y+145, 60, 85) #wstawiamy tutaj aby hitbox za kazdym razem poruszal sie razem z psotacia
        self.health = 80
        self.czypokonany = False
        self.czypoza = False
        self.numer = 0

    def ruch(self): #animacja, analogicznie jak boahter
        if self.nrkrokuataku >= 16*2:
            self.nrkrokuataku = 0

    def draw(self, okno): #grafika - pomocniczy hitboxy i poruszanie sie
        self.hitbox = pygame.Rect(self.x + 145, self.y+145, 60, 85) #gdzie znajduje sie hitbox (a, b, x, y); a, b - od ktorego punktu obrazka c, d - wymiary
        pygame.draw.rect(okno,(255, 76, 76), (self.x+140, self.y+110, 80,10)) #x,y pozycja, 50,10 - szerokosc i wysokosc paska
        if self.health>= 0:
            pygame.draw.rect(okno, (52, 191, 73), (self.x + 140, self.y + 110, self.health, 10))
        #pygame.draw.rect(okno, (0,0,0), self.hitbox, 1) #rysowanie hitboxa
        self.ruch() #poruszanie sie
        okno.blit(grzyb_ruch[self.nrkrokuataku//2], (self.x, self.y))
        self.nrkrokuataku += 1
        if self.health <= 0 and wyciszenie == False:
            smiercGrzyba_dzwiek.play()

    def move(self):
        self.hit()
        self.x -= 1 # predkosc ruchu

    def hit(self): #Jezeli hitbox potwora znajduje sie w tym samym miejscu co hitbox playera
        if player.hitbox.colliderect(wrog.hitbox):
            if player.health > 0:
                player.health -= 1.5 #"zaliczamy "hit"
            if player.health <= 0 and player.lives > 0:
                player.lives -= 1
                player.health = 100
            elif player.health <= 0 and player.lives == 0:
                player.czyZyje = False

    def off_screen(self): #kiedy ma znikac
        return not (self.x >= -150 and self.x <= okno_szer + 50)


class Oko(Grzyb): #tworzę tę klasę przez dziedziczenie aby nie przpisywać wszystkiego

    def __init__(self, x, y):
        self.x = x  # gdzie sie pojawia na poczatku
        self.y = y
        self.czypokonany = False
        self.nrkrokuataku = 0  # do animacji
        # Zycie
        self.hitbox = pygame.Rect(self.x + 50, self.y + 50, 60, 50)  # wstawiamy tutaj aby hitbox za kazdym razem poruszal sie razem z psotacia
        self.health = 10
        self.czypoza = False
        self.numer = 0

    def draw(self, okno): #inne rysowanie
        self.hitbox = pygame.Rect(self.x + 50, self.y+50, 60, 50)
        #pygame.draw.rect(okno, (0,0,0), self.hitbox, 1)
        pygame.draw.rect(okno, (255, 76, 76),(self.x + 60, self.y+ 30, 20, 10))  # x,y pozycja, 50,10 - szerokosc i wysokosc paska
        if self.health >= 0:
            pygame.draw.rect(okno, (52, 191, 73), (self.x + 60, self.y + 30, self.health*2, 10))
        self.ruch()
        okno.blit(oko_ruch[self.nrkrokuataku//2], (self.x, self.y))
        self.nrkrokuataku += 1
        if self.health <= 0 and wyciszenie == False:
            smiercOka_dzwiek.play()

    def move(self): #inna szybkosc
        self.hit()
        self.x -= 3



class Goblin(Grzyb): #tworzę tę klasę przez dziedziczenie aby nie przpisywać wszystkiego

    def __init__(self, x, y):
        self.x = x # gdzie sie pojawia na poczatku
        self.y = y
        self.nrkrokuataku = 0  # do animacji
        self.czypoza = False
        self.czypokonany = False
        # Zycie
        self.hitbox = pygame.Rect(self.x + 50, self.y+50, 40, 80)  # wstawiamy tutaj aby hitbox za kazdym razem poruszal sie razem z psotacia
        self.health = 50
        self.numer = 0

    def ruch(self):
        if self.nrkrokuataku >= 8*3:
            self.nrkrokuataku = 0

    def draw(self, okno): #inne rysowanie
        self.hitbox = pygame.Rect(self.x + 50, self.y+50, 40, 80)
        #pygame.draw.rect(okno, (0,0,0), self.hitbox, 1)
        pygame.draw.rect(okno, (255, 76, 76),(self.x +45, self.y + 25 , 50, 10))  # x,y pozycja, 50,10 - szerokosc i wysokosc paska
        if self.health >= 0:
            pygame.draw.rect(okno, (52, 191, 73),(self.x +45, self.y+ 25 , self.health, 10)) #rysuje zielony kwadrat w dopasowanym
            #recznie miejscu ktory ma dlugosc odpowiadajaca zyciu
        self.ruch()
        okno.blit(goblin_ruch[self.nrkrokuataku//3], (self.x, self.y))
        self.nrkrokuataku += 1
        if self.health <= 0 and wyciszenie == False:
            smiercGoblina_dzwiek.play()

    def move(self): #inna szybkosc ataku
        self.hit()
        self.x -= 3




# GRAFIKA

def grafika():

    global wiezaZycia, zabici, stop, level, wrogowie, potki, intro

    if wcisniecie[pygame.K_RETURN]:
        intro = False

    if intro == True:
        okno.blit (tlo2,(0,0)) # wypelnia tlem aby postaci nie zostawialy sladow

    else:
        okno.blit (tlo1, (0,0))

        #Rysowanie postaci
        player.draw(okno)
        #Rysowanie kuli
        for kulaognia in player.kuleognia: #rysujemy wypuszczona kule ognia dla kul ognia z listy kuleognia
            kulaognia.draw_kulaognia()
        #Rysowanie pioruna
        for piorun in player.pioruny:
            piorun.draw_piorun()

        #Rysowanie wroga
        for wrog in wrogowie:
            wrog.draw(okno)

        for potka in potki:
            potka.draw(okno)

        #Rysowanie wiezy
        okno.blit(wieza, (10, 125))

        #Gameover/stop - co kiedy gracz ginie
        if player.czyZyje == False:
            stop = True
            okno.blit(gameover, (0, 0))
            czcionka = pygame.font.Font(os.path.join("czcionka", "czcionka.otf"), 60)
            tekst1 = czcionka.render('Game Over', True, (27, 35, 44))
            tekst2 = czcionka.render('Your Score: ' +str(zabici) , True, (27, 35, 44))
            tekst3 = czcionka.render('Press R to try again', True, (27, 35, 44))
            miejsceTekstu1 = tekst1.get_rect() #bierze tekst jako prostokat
            miejsceTekstu1.center = (okno_szer//2, okno_wys//2 - 100) #wyszukuje srodek dla kwadratu na tekst
            miejsceTekstu2 = tekst2.get_rect()
            miejsceTekstu2.center = (okno_szer//2, okno_wys//2) #
            miejsceTekstu3 = tekst3.get_rect()  #
            miejsceTekstu3.center = (okno_szer // 2, okno_wys // 2 + 100)
            okno.blit(tekst1, miejsceTekstu1)
            okno.blit(tekst2, miejsceTekstu2)
            okno.blit(tekst3, miejsceTekstu3)
            if wcisniecie[pygame.K_r]:
                player.czyZyje = True
                player.lives = 1
                player.health = 100
                wiezaZycia = 10
                wrogowie = []
                potki = []
                zabici = 0
                level  = 1
                stop = False
                player.x = 150
                player.y = 300

        if not stop:
            czcionka = pygame.font.Font(os.path.join("czcionka", "czcionka.otf"), 30)
            tekst =  czcionka.render("Tower health: " + str(wiezaZycia) + '     Lives: '+ str(player.lives) + "                                              Monsters killed: " +str(zabici) + "     Poziom: " + str(level), True, 	(0, 125, 81)) #wybieramy tekst ktory ma sie wyswietlic i jego pozycje
            okno.blit(tekst, (75,30))
            czcionka_mute = pygame.font.Font(os.path.join("czcionka", "czcionka.otf"), 15)  # ("freesansbold.ttf", 30) #wybieramy czcionke
            tekst_mute = czcionka_mute.render("Press M to mute", True, (0, 125, 81))  # wybieramy tekst ktory ma sie wyswietlic i jego pozycje
            okno.blit(tekst_mute, (1200, 10))

    #opoznianie i odswiezanie
    pygame.time.delay(20)
    pygame.display.update()





player = Bohater(150, 310)

while dziala:

    czasogolny+=1

    # Input uzytkownika
    wcisniecie = pygame.key.get_pressed()  # Definiuje czym jest wcisniecie i jaki efekt daje wcisniecie przycisku

    # Wyciszenie gry
    if wcisniecie[pygame.K_m]:
        if wyciszenie == True and czasogolny > ostczasogolny + 5: #dodatkowy warunek bo nie potrafimy tak szybko klikac aby bylo tylko 1 przewiniecie petli
            wyciszenie = False
            pygame.mixer.music.unpause()
            ostczasogolny = czasogolny
        if wyciszenie == False and czasogolny > ostczasogolny + 5:
            wyciszenie = True
            pygame.mixer.music.pause()
            ostczasogolny=czasogolny

    # Grafika - wywolanie funkcji odpowiedzialnej za animacje i grafike
    grafika()

    # Wyjscie z gry
    for wydarzenie in pygame.event.get(): # jezeli wydarzenie typu QUIT (zamnkniecie gry) nastapi...
        if wydarzenie.type == pygame.QUIT:
            dziala = False #zamykamy gre


    # "Podstawowy" tryb gry
    if intro == False:

        # Wrogowie
        # Spawnowanie losowego typu wrogow w losowych odstepach czasu
        if len(wrogowie) != 0 and jednorazowe == False: #jesli mamy juz jakiegos wrogama, ustalamy (jednorazowo) czas do zespawnowania kolejnego
            spawn_time = random.randint(czas_spawn0, czas_spawn1) # czas pomiedzy kolejnymi wrogami - losujemy od 150 do 300 "przewiniec"
            jednorazowe = True #aby tylko raz to robic

        if len(wrogowie) == 0 or czas_potwory == spawn_time:  #jesli nie mamy juz zadnego wroga lub nadszedl "czas" kolejnego wroga
            typ_potwora = random.randint(0, typy) # losujemy typ potwora
            if typ_potwora == 2:
                wrog = Grzyb(1200,215)
            if typ_potwora == 1:
                wysokosc = random.randint(100,300) #na jakiej wysokosci pojawi sie oko (na razie to sa granice strzalu bohatera)
                wrog = Oko(1200, wysokosc)
            if typ_potwora == 0:
                wrog = Goblin(1200, 335)
            wrogowie.append(wrog)
            jednorazowe = False
            czas_potwory = 0

        for wrog in wrogowie:
            wrog.move()
            if wrog.health <= 0:
                wrogowie.remove(wrog)
                if wrog.czypokonany == False:
                    zabici+=1
                wrog.czypokonany = True
            if wrog.x < 50:
                if wrog.czypoza == False:
                    wiezaZycia-=1
                    if wyciszenie == False and stop == False:
                        wiezatraci_dzwiek.play()
                wrogowie.remove(wrog)
                wrog.czypoza = True


        # Obsluga potek

        for potka in potki:
            if czas_potka > 500 and len(potki)==1: # potka po jakims czasie znika jesli jej sie nie zbierze
                potki.remove(potka)
                losuj_potke = True
            if potka.czyuzyta: #potka znika tez po uzyciu
                potki.remove(potka)
                losuj_potke = True

        if losuj_potke:
            potka_spawn = random.randint(1000,3000)
            losuj_potke = False

        # Spawnowanie potek
        if czas_potka == potka_spawn:
            potka_x = random.randint(200, 1200)
            potka_y = random.randint(120, 300)
            potka = Potka(potka_x, potka_y)
            potki.append(potka)
            czas_potka = 0

        # Kula ognia - podstawowy
        player.kulaognia_uzycie()

        #piorun - specjalny
        player.piorun_uzycie()

        # Ruch
        player.ruch_bohatera(wcisniecie)

        # Zycie wiezy
        if wiezaZycia <= 0:
            player.czyZyje = False

        # Levele
        if zabici < 5:
            level = 1
            typy = 0  # do kontroli typów potworów
            czas_spawn0 = 100  # do kontroli czasu
            czas_spawn1 = 200
        elif zabici < 15:
            level = 2
            typy = 1
            czas_spawn0 = 80
            czas_spawn1 = 180
        elif zabici < 35:
            level = 3
            typy = 2
            czas_spawn0 = 60
            czas_spawn1 = 160
        elif zabici < 60:
            level = 4
            typy = 2
            czas_spawn0 = 40
            czas_spawn1 = 140
        elif zabici < 100:
            level = 5
            typy = 2
            czas_spawn0 = 20
            czas_spawn1 = 120

        # Liczenie czasu
        czas_potwory += 1
        czas_potka += 1


