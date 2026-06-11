import pygame

class Napis:
    def __init__(self, x, y, szerokosc, wysokosc, tekst,rozmiar=36):
        self.rect = pygame.Rect(x, y, szerokosc, wysokosc)
        self.tekst = tekst
        
        pygame.font.init()
        self.font = pygame.font.SysFont(None, rozmiar)

    def rysuj(self, ekran):
        
        text_surf = self.font.render(self.tekst, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        ekran.blit(text_surf, text_rect)
