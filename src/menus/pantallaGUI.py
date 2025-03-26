from ..extras import ResourceManager, ANCHO, ALTO
import pygame
from .elemento_gui import *
from .boton_gui import *

class PantallaGUI:
    def __init__(self, menu, nombreImagen):
        self.menu = menu
        # Se carga la imagen de fondo
        self.imagen = ResourceManager.load_image(nombreImagen)
        self.imagen = pygame.transform.scale(self.imagen, (ANCHO, ALTO))
        # Se tiene una lista de elementos GUI
        self.elementosGUI = []
        
    def eventos(self, lista_eventos):
        for event in lista_eventos:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.elementoClic = None
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(event.pos):
                        self.elementoClic = elemento
            if event.type == pygame.MOUSEBUTTONUP:
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(event.pos):
                        if (elemento == self.elementoClic):
                            elemento.accion()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.menu.continuar()


    def dibujar(self,pantalla):
        pantalla.blit(self.imagen, (0,0))
        for elemento in self.elementosGUI:
            elemento.dibujar(pantalla)

    def update(self):
        for elemento in self.elementosGUI:
            elemento.update()

class PantallaInicialGUI(PantallaGUI):
    def __init__(self, menu):
        super().__init__(menu, "menu_inicial.jpeg")
        self.elementosGUI = [BotonJugar(self, (ANCHO/2,(ALTO/3 * 2) - BUTTON_SIZEY)),
                             BotonCargar(self, (ANCHO/2,(ALTO/3 * 2))),
                             BotonConfiguraciones(self, (ANCHO/2, ((ALTO/3 * 2)  +  BUTTON_SIZEY))),
                             BotonSalir(self, (ANCHO/2, ((ALTO/3 * 2)  +  BUTTON_SIZEY*2)))]
        
class PantallaConfiguracionesGUI(PantallaGUI):
    def __init__(self, menu):
        super().__init__(menu, "menu_inicial.jpeg")
        self.elementosGUI = [BotonVolver(self, (ANCHO/2,ALTO/3))]

class PantallaPauseGUI(PantallaGUI):
    def __init__(self, menu):
        super().__init__(menu, "menu_inicial.jpeg")
        self.background = None
        self.elementosGUI = [BotonResume(self, (ANCHO/2, ALTO/3)),
                             BotonCargar(self, (ANCHO/2, ALTO/3 + BUTTON_SIZEY)),
                             BotonGuardar(self, (ANCHO/2, ALTO/3 + BUTTON_SIZEY*2)),
                             BotonConfiguraciones(self, (ANCHO/2, ALTO/3 + BUTTON_SIZEY*3)),
                             BotonSalir(self, (ANCHO/2, ALTO/3 + BUTTON_SIZEY * 4))]
        
    def dibujar(self,pantalla):
        if self.background == None:
            self.background = pantalla.copy()
        pantalla.blit(self.background, (0,0))
        for elemento in self.elementosGUI:
            elemento.dibujar(pantalla)

class PantallaGameOverGUI(PantallaGUI):
    def __init__(self, menu):
        super().__init__(menu, "blank_background.jpeg")
        self.elementosGUI = [BotonRetry(self, (ANCHO / 2, ALTO / 3 + BUTTON_SIZEY)),
                             BotonReturnToTitle(self, (ANCHO / 2, ALTO / 3 + BUTTON_SIZEY * 2)),
                             BotonSalir(self, (ANCHO / 2, ALTO / 3 + BUTTON_SIZEY * 3))]

