import pygame


class Przycisk:
    def __init__(self,x,y,szerokosc,wysokosc,kolor,tekst):
        self.rect = pygame.Rect(x,y,szerokosc,wysokosc)
        self.kolor = kolor
        self.tekst = tekst
        self.kolor_aktywny = (kolor[0]+30, kolor[1]+30, kolor[2]+30)
        self.click_flag = False
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)

    def rysuj(self,ekran):
        poz_myszy = pygame.mouse.get_pos()
        aktualny_kolor = self.kolor_aktywny if self.rect.collidepoint(poz_myszy) else self.kolor
        pygame.draw.rect(ekran,aktualny_kolor,self.rect)
        if self.click_flag:
            text_surf = self.font.render(self.tekst, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.rect.center)
            ekran.blit(text_surf, text_rect)
    def czy_klikniety(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.click_flag = not self.click_flag
            return True
        
        return False