import pygame
from .elemento_gui import ElementoGUI
from ..extras import ResourceManager, Settings

class BotonGUI(ElementoGUI):

    def __init__(self, pantalla, texto, posicion):
        ElementoGUI.__init__(self, pantalla)
        self.imagen = ResourceManager.load_image("button_default.png")
        self.imagen = pygame.transform.scale(self.imagen, (Settings.BUTTON_SIZEX, Settings.BUTTON_SIZEY))
        self.rect = self.imagen.get_rect()
        self.idle = self.font.render(texto, True, Settings.NEGRO)
        self.hover = self.font.render(texto, True, Settings.VERDE)
        self.text = self.idle
        self.textrect = self.text.get_rect()
        # Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)
    
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)
        pantalla.blit(self.text, self.textrect)

    def establecerPosicion(self, posicion):
        super().establecerPosicion(posicion)
        self.textrect.center = self.rect.center

class BotonJugar(BotonGUI):
    def __init__(self, pantalla,posicion):
        BotonGUI.__init__(self, pantalla, "Jugar", posicion)
    
    def accion(self):
        self.pantalla.menu.ejecutarJuego()

class BotonSalir(BotonGUI):
    def __init__(self, pantalla, posicion):
        BotonGUI.__init__(self, pantalla, "Salir", posicion)

    def accion(self):
        self.pantalla.menu.salirPrograma()

class BotonConfiguraciones(BotonGUI):
    def __init__(self, pantalla, posicion):
        super().__init__(pantalla, "Configuraciones",posicion)

    def accion(self):
        self.pantalla.menu.irAConfiguraciones()

class BotonVolver(BotonGUI):
    def __init__(self, pantalla, posicion):
        super().__init__(pantalla, "Volver", posicion)

    def accion(self):
        self.pantalla.menu.mostrarPantallaInicial()

class BotonResume(BotonGUI):
    def __init__(self, pantalla, posicion):
        super().__init__(pantalla, "Continuar", posicion)

    def accion(self):
        self.pantalla.menu.continuar()

class BotonRetry(BotonGUI):
    def __init__(self, pantalla, posicion):
        super().__init__(pantalla, "Volver a intentar", posicion)

    def accion(self):
        self.pantalla.menu.reintentar()

class BotonGuardar(BotonGUI):
    def __init__(self, pantalla, posicion):
        super().__init__(pantalla, "Guardar Partida", posicion)

    def accion(self):
        self.pantalla.menu.guardar_partida()

class BotonCargar(BotonGUI):
    def __init__(self, pantalla, posicion):
        super().__init__(pantalla, "Cargar Partida", posicion)

    def accion(self):
        self.pantalla.menu.cargar_partida()

class BotonReturnToTitle(BotonGUI):
    def __init__(self, pantalla, posicion):
        super().__init__(pantalla, "Pantalla de titulo", posicion)

    def accion(self):
        self.pantalla.menu.return_to_title()