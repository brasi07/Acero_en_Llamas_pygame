from abc import abstractmethod
from ..extras import ResourceManager
import pygame

class ElementoGUI:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        # La fuente la debería cargar el estor de recursos
        if self.pantalla.ANCHO >= 1024:
            self.font = ResourceManager.load_font("Komi24", "Komi.ttf", 24)
        else:
            self.font = ResourceManager.load_font("Komi12", "Komi.ttf", 12)

    def establecerPosicion(self, posicion):
        (posicionx, posiciony) = posicion
        self.rect.centerx = posicionx
        self.rect.centery = posiciony

    def posicionEnElemento(self, posicion):
        (posicionx, posiciony) = posicion
        if (posicionx>=self.rect.left) and (posicionx<=self.rect.right) and (posiciony>=self.rect.top) and (posiciony<=self.rect.bottom):
            return True
        else:
            return False
        

    @abstractmethod
    def dibujar(self):
        pass

    @abstractmethod
    def accion(self):
        pass

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.posicionEnElemento(mouse_pos):
            self.text = self.hover
        else:
            self.text = self.idle

