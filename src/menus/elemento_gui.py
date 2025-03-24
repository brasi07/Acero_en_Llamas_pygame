from abc import abstractmethod
from ..extras import ResourceManager, VERDE, NEGRO
import pygame

class ElementoGUI:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        # La fuente la debería cargar el estor de recursos
        self.font = ResourceManager.load_font("Komi.ttf", 24)


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
        return 
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.posicionEnElemento(mouse_pos):
            self.text = self.hover
        else:
            self.text = self.idle


#
#
# TEXTO 
#
#


class TextoGUI(ElementoGUI):
    def __init__(self, pantalla, color, texto, posicion):
        # Se crea la imagen del texto
        ElementoGUI.__init__(self, pantalla)
        self.idle = self.font.render(texto, True, color)
        self.text = self.idle
        self.hover = self.font.render(texto, True, VERDE)
        self.rect = self.text.get_rect()
        # Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)

    def dibujar(self, pantalla):
        pantalla.blit(self.text, self.rect)

    


class TextoJugar(TextoGUI):
    def __init__(self, pantalla,posicion):
        TextoGUI.__init__(self, pantalla, NEGRO, 'Jugar', posicion)
        
    def accion(self):
        self.pantalla.menu.ejecutarJuego()

class TextoResume(TextoGUI):
    def __init__(self, pantalla, posicion):
        super().__init__(pantalla, NEGRO, "Continuar", posicion)

    def accion(self):
        self.pantalla.menu.continuar()

class TextoSalir(TextoGUI):
    def __init__(self, pantalla, posicion):
        super().__init__(pantalla, NEGRO, "Salir", posicion)
    
    def accion(self):
        self.pantalla.menu.salirPrograma()

class TextoConfiguraciones(TextoGUI):
    def __init__(self, pantalla, posicion):
        super().__init__(pantalla, NEGRO, "Configuraciones", posicion)

    def accion(self):
        self.pantalla.menu.irAConfiguraciones()

