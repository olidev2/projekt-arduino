import pygame

class Strzalka:
    def __init__(self, x, y, szerokosc, wysokosc, kolor, kierunek):
        self.rect = pygame.Rect(x, y, szerokosc, wysokosc)
        self.kolor = kolor  
        self.kolor_aktywny = (min(kolor[0]+30, 255), min(kolor[1]+30, 255), min(kolor[2]+30, 255))
        self.click_flag = False
        self.kierunek = kierunek

    def rysuj(self, ekran):
        poz_myszy = pygame.mouse.get_pos()
        aktualny_kolor = self.kolor_aktywny if self.rect.collidepoint(poz_myszy) else self.kolor
        pygame.draw.rect(ekran, aktualny_kolor, self.rect)
        
        match self.kierunek:
            case "gora":
                pygame.draw.line(ekran, (255, 255, 255), (self.rect.centerx, self.rect.top), (self.rect.centerx, self.rect.bottom), 3)
                pygame.draw.line(ekran, (255, 255, 255), (self.rect.centerx, self.rect.top), (self.rect.centerx - 10, self.rect.top + 10), 3)
                pygame.draw.line(ekran, (255, 255, 255), (self.rect.centerx, self.rect.top), (self.rect.centerx + 10, self.rect.top + 10), 3)
            case "dol":
                pygame.draw.line(ekran, (255, 255, 255), (self.rect.centerx, self.rect.top), (self.rect.centerx, self.rect.bottom), 3)  
                pygame.draw.line(ekran, (255, 255, 255), (self.rect.centerx, self.rect.bottom), (self.rect.centerx - 10, self.rect.bottom - 10), 3)
                pygame.draw.line(ekran, (255, 255, 255), (self.rect.centerx, self.rect.bottom), (self.rect.centerx + 10, self.rect.bottom - 10), 3)
            case "lewo":
                pygame.draw.line(ekran, (255, 255, 255), (self.rect.left, self.rect.centery), (self.rect.right, self.rect.centery), 3)
                pygame.draw.line(ekran, (255, 255, 255), (self.rect.left, self.rect.centery), (self.rect.left + 10, self.rect.centery - 10), 3)
                pygame.draw.line(ekran, (255, 255, 255), (self.rect.left, self.rect.centery), (self.rect.left + 10, self.rect.centery + 10), 3)
            case "prawo":
                pygame.draw.line(ekran, (255, 255, 255), (self.rect.left, self.rect.centery), (self.rect.right, self.rect.centery), 3)  
                pygame.draw.line(ekran, (255, 255, 255), (self.rect.right, self.rect.centery), (self.rect.right - 10, self.rect.centery - 10), 3)
                pygame.draw.line(ekran, (255, 255, 255), (self.rect.right, self.rect.centery), (self.rect.right - 10, self.rect.centery + 10), 3)

    def czy_klikniety(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.click_flag = not self.click_flag
                return True
        return False