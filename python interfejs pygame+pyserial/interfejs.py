import pygame
import math  # <-- Nowy, niezbędny import do trygonometrii
from przycisk import Przycisk
from strzalki import Strzalka
from backend import Backend
from napis import Napis

class Interfejs:
    def __init__(self, szerokosc, wysokosc):
        pygame.init()
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc
        self.ekran = pygame.display.set_mode((szerokosc, wysokosc))
        pygame.display.set_caption("Interfejs łazika")
        
        self.port_draw = False
        self.dziala = True
        self.backend = Backend()
        self.przyciski_portow = []
        
        # słownik do przechowywania danych ze skanera (kąt: dystans)
        self.punkty_radaru = {}
        
        self.przyciski = [
            Przycisk(100, 100, 200, 50, (100, 100, 100), "Wybierz port", "port"),
            Przycisk(100, 200, 200, 50, (100, 100, 100), "Przycisk 2", "test"),
            Przycisk(950, 600, 200, 50, (100, 100, 100), "Radar", "radar")
        ]
        self.strzalki = [
            Strzalka(680, 600, 50, 50, (100, 100, 100), "lewo"),
            Strzalka(820, 600, 50, 50, (100, 100, 100), "prawo"),
            Strzalka(750, 600, 50, 50, (100, 100, 100), "dol"),
            Strzalka(750, 530, 50, 50, (100, 100, 100), "gora"),
        ]

        self.napis = [
            Napis(100, 300, 200, 50, "Interfejs Łazika", 40),
            Napis(580, 400, 400, 50, "Sterowanie", 24)
        ]

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.dziala = False

            # wyłapywanie puszczenia przycisku myszy (STOP)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.backend.wyslij_komende('S')

            for przycisk in self.przyciski:
                if przycisk.czy_klikniety(event):
                    match przycisk.rola:
                        case "port":
                            self.port_draw = not self.port_draw 
                            if self.port_draw:
                                self.backend.update_ports()
                                ports = self.backend.get_ports()
                                self.przyciski_portow.clear() 
                                for i, port_nazwa in enumerate(ports):
                                    nowy_przycisk = Przycisk(350, 100 + (i * 60), 200, 50, (80, 80, 150), port_nazwa, "polacz_port")
                                    self.przyciski_portow.append(nowy_przycisk)
                            else:
                                self.przyciski_portow.clear()
                        case "radar":
                            # wysłanie komendy startu skanowania
                            self.backend.wyslij_komende('r')
                            # zzyszczenie starych kropek z ekranu przed nowym skanem
                            self.punkty_radaru.clear() 
                        case _:
                            print("Inna rola")

            if self.port_draw:
                for port_przycisk in self.przyciski_portow:
                    if port_przycisk.czy_klikniety(event):
                        if not getattr(port_przycisk, 'polaczony', False):
                            print(f"Wybrano do połączenia: {port_przycisk.tekst}")
                            sukces = self.backend.connect(port_przycisk.tekst)
                            if sukces:
                                port_przycisk.polaczony = True
                        else:
                            print(f"Odłączono: {port_przycisk.tekst}")
                            self.backend.disconnect()
                            port_przycisk.polaczony = False

            for strzalka in self.strzalki:
                if strzalka.czy_klikniety(event):
                    match strzalka.kierunek:
                        case "gora": self.backend.wyslij_komende('F')
                        case "dol": self.backend.wyslij_komende('B')
                        case "lewo": self.backend.wyslij_komende('L')
                        case "prawo": self.backend.wyslij_komende('R')

    def coordinate_system(self):
        # odbieranie i rozpakowywanie danych z radaru
        odebrane_dane = self.backend.odbierz_dane()
        
        if odebrane_dane and odebrane_dane.startswith("R:"):
            wartosci = odebrane_dane[2:].split(",")
            
            if len(wartosci) == 2:
                try:
                    kat = int(wartosci[0])
                    dystans = int(wartosci[1])
                    
                    # ignorujemy błędy pomiarowe (np. -1, gdy radar nic nie złapie)
                    if dystans > 0:
                        self.punkty_radaru[kat] = dystans
                        print(f"Skan -> Kąt: {kat}°, Odległość: {dystans} cm")
                        
                except ValueError:
                    print("Błąd parsowania: Odebrane wartości nie są liczbami.")

    def draw(self):
        self.ekran.fill((0, 0, 0))
        
        
        srodek_x = 200
        srodek_y = 630
        promien_szarego_kola = 150
        
       
        pygame.draw.circle(self.ekran, (200, 200, 200), (srodek_x, srodek_y), promien_szarego_kola)
        
        # radar rysowanie kropek
        for kat, dystans in self.punkty_radaru.items():
            radiany = math.radians(kat)
            
            r = min(dystans, promien_szarego_kola)
            
            x = srodek_x + r * math.cos(radiany)
            y = srodek_y - r * math.sin(radiany)
            
            pygame.draw.circle(self.ekran, (255, 50, 50), (int(x), int(y)), 3)

        for przycisk in self.przyciski:
            przycisk.rysuj(self.ekran)
            
        for strzalka in self.strzalki:
            strzalka.rysuj(self.ekran)
            
        if self.port_draw:
            for port_przycisk in self.przyciski_portow:
                port_przycisk.rysuj(self.ekran)
                
        for napis in self.napis:
            napis.rysuj(self.ekran)
            
        pygame.display.flip()

    def run(self):
        while self.dziala:
            self.event_handler()
            self.coordinate_system()
            self.draw()
            
        print("Zamykanie interfejsu... Sprzątanie portów.")
        self.backend.disconnect()
        pygame.quit()

if __name__ == "__main__":
    interfejs = Interfejs(1200, 800)
    interfejs.run()