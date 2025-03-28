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
        self.hover = self.font.render(texto, True, Settings.ROJO)
        self.text = self.idle
        self.incial_text = texto
        self.textrect = self.text.get_rect()
        # Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)
        self.cambiado = False
    
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)
        pantalla.blit(self.text, self.textrect)

    def establecerPosicion(self, posicion):
        super().establecerPosicion(posicion)
        self.textrect.center = self.rect.center

    def cambiarTexto(self, texto):
        self.idle = self.font.render(texto, True, Settings.NEGRO)
        self.hover = self.font.render(texto, True, Settings.ROJO)
        self.text =self.hover
        self.textrect = self.text.get_rect()
        self.textrect.center = self.rect.center
        self.cambiado = True
        self.clickedWhen = pygame.time.get_ticks()

    def update(self):
        super().update()
        if self.cambiado:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.clickedWhen >= 500:
                self.volverTextoOriginal()

    def volverTextoOriginal(self):
        self.idle = self.font.render(self.incial_text, True, Settings.NEGRO)
        self.hover = self.font.render(self.incial_text, True, Settings.ROJO)
        self.text =self.hover
        self.textrect = self.text.get_rect()
        self.textrect.center = self.rect.center
        self.cambiado = False


class BotonJugar(BotonGUI):
    def __init__(self, pantalla,posicion):
        BotonGUI.__init__(self, pantalla, "JUGAR", posicion)
    
    def accion(self):
        self.pantalla.menu.ejecutarJuego()

class BotonSalir(BotonGUI):
    def __init__(self, pantalla, posicion):
        BotonGUI.__init__(self, pantalla, "SALIR", posicion)

    def accion(self):
        self.pantalla.menu.salirPrograma()

class BotonConfiguraciones(BotonGUI):
    def __init__(self, pantalla, posicion):
        super().__init__(pantalla, "AJUSTES",posicion)

    def accion(self):
        self.pantalla.menu.irAConfiguraciones()

class BotonVolver(BotonGUI):
    def __init__(self, pantalla, posicion):
        super().__init__(pantalla, "VOLVER", posicion)

    def accion(self):
        self.pantalla.menu.mostrarPantallaInicial()

class BotonResume(BotonGUI):
    def __init__(self, pantalla, posicion, to=None):
        super().__init__(pantalla, "CONTINUAR", posicion)
        self.to = to

    def accion(self):
        if self.to:
            self.pantalla.menu.director.cambiar_escena(self.to)
        else:
            self.pantalla.menu.continuar()

class BotonRetry(BotonGUI):
    def __init__(self, pantalla, posicion):
        super().__init__(pantalla, "VOLVER A INTENTAR", posicion)

    def accion(self):
        self.pantalla.menu.reintentar()

class BotonGuardar(BotonGUI):
    def __init__(self, pantalla, posicion):
        super().__init__(pantalla, "GUARDAR PARTIDA", posicion)

    def accion(self):
        self.pantalla.menu.guardar_partida()
        self.cambiarTexto("GUARDADO")

class BotonCargar(BotonGUI):
    def __init__(self, pantalla, posicion):
        super().__init__(pantalla, "CARGAR PARTIDA", posicion)

    def accion(self):
        self.pantalla.menu.cargar_partida(self)

class BotonReturnToTitle(BotonGUI):
    def __init__(self, pantalla, posicion):
        super().__init__(pantalla, "PANTALLA DE TITULO", posicion)

    def accion(self):
        self.pantalla.menu.return_to_title()

class BotonCreditos(BotonGUI):
    def __init__(self, pantalla, posicion):
        super().__init__(pantalla, "CREDITOS", posicion)

    def accion(self):
        from .menu import CreditosMenu
        self.pantalla.menu.director.cambiar_escena(CreditosMenu(self.pantalla.menu.director))