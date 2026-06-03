import pygame

from przycisk import Przycisk
from strzalki import Strzalka
class Interfejs:
    def __init__(self, szerokosc, wysokosc):
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc
        self.ekran = pygame.display.set_mode((szerokosc, wysokosc))
        pygame.display.set_caption("Interfejs łazika")
    
        self.dziala = True
        self.przyciski = [
            Przycisk(100, 100, 200, 50, (100, 100, 100), "Wybierz port"),
            Przycisk(100, 200, 200, 50, (100, 100, 100), "Przycisk 2")
        ]
        self.strzalki = [
            Strzalka(680, 600, 50, 50, (100, 100, 100),"lewo"),
            Strzalka(820, 600, 50, 50, (100, 100, 100),"prawo"),
            Strzalka(750, 600, 50, 50, (100, 100, 100),"dol"),
            Strzalka(750, 530, 50, 50, (100, 100, 100),"gora"),
        ]
    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.dziala = False

            for przycisk in self.przyciski:
                if przycisk.czy_klikniety(event):
                    print(f"Kliknięto {przycisk.tekst}")
            for strzalka in self.strzalki:
                if strzalka.czy_klikniety(event):
                    print(f"Kliknięto strzałkę {strzalka.kierunek}")
    def coordinate_system(self):
        # metoda do odbierania danych i obliczen matematycznych
        pass
    def draw(self):
        self.ekran.fill((0,0,0))
        pygame.draw.circle(self.ekran, (200,200,200), (200, 630), 150)
        for przycisk in self.przyciski:
            przycisk.rysuj(self.ekran)
        for strzalka in self.strzalki:
            strzalka.rysuj(self.ekran)
        pygame.display.flip()
    def run(self):
        while self.dziala:
            self.event_handler()
            self.coordinate_system()
            self.draw()
        pygame.quit()
if __name__ == "__main__":
    interfejs = Interfejs(1200, 800)
    interfejs.run()