import pygame

class Przycisk:
    def __init__(self, x, y, szerokosc, wysokosc, kolor, tekst, rola):
        self.rect = pygame.Rect(x, y, szerokosc, wysokosc)
        self.kolor = kolor
        self.tekst = tekst
        self.rola = rola
        self.kolor_aktywny = (min(kolor[0]+30, 255), min(kolor[1]+30, 255), min(kolor[2]+30, 255))
        self.click_flag = False
        
        # Flagi stanu połączenia
        self.polaczony = False
        self.kolor_polaczony = (50, 200, 50) # Zielony
        
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)

    def rysuj(self, ekran):
        poz_myszy = pygame.mouse.get_pos()
        
        # Priorytety kolorów
        if getattr(self, 'polaczony', False):
            aktualny_kolor = self.kolor_polaczony
        elif self.rect.collidepoint(poz_myszy):
            aktualny_kolor = self.kolor_aktywny
        else:
            aktualny_kolor = self.kolor
            
        pygame.draw.rect(ekran, aktualny_kolor, self.rect)
        
        if self.rola == "polacz_port":
            text_surf = self.font.render(self.tekst, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.rect.center)
            ekran.blit(text_surf, text_rect)
            
        if self.click_flag:
            match self.rola:
                case "polacz_port":
                    pass
                case _:
                    text_surf = self.font.render(self.tekst, True, (255, 255, 255))
                    text_rect = text_surf.get_rect(center=self.rect.center)
                    ekran.blit(text_surf, text_rect)

    def czy_klikniety(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.click_flag = not self.click_flag
                return True
        return False