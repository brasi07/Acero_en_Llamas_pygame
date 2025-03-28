from ..extras import ResourceManager, Settings
import pygame
from .elemento_gui import *
from .boton_gui import *
from .menu_texto import TextoMenu
from .texto_gui import TextoRes, TextoSonido

class PantallaGUI:
    def __init__(self, menu, nombreImagen):
        self.menu = menu
        self.elementoClic = None
        # Se carga la imagen de fondo
        self.imagen = ResourceManager.load_image(nombreImagen)
        self.ANCHO, self.ALTO = Settings.ANCHO, Settings.ALTO
        self.BUTTON_SIZEY = Settings.BUTTON_SIZEY
        self.imagen = pygame.transform.scale(self.imagen, (self.ANCHO, self.ALTO))
        # Se tiene una lista de elementos GUI
        self.elementosGUI = []
        
    def eventos(self, lista_eventos):
        for event in lista_eventos:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.elementoClic = None
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(event.pos):
                        ResourceManager.play_sound("Menu Selection Click.wav")
                        self.elementoClic = elemento
            if event.type == pygame.MOUSEBUTTONUP:
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(event.pos):
                        if self.elementoClic != None and (elemento == self.elementoClic):
                            elemento.accion()
            #if event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_ESCAPE:
                    #self.menu.continuar()


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
        self.elementosGUI = [BotonJugar(self, (self.ANCHO/2,(self.ALTO/3 * 2) - self.BUTTON_SIZEY)),
                             BotonCargar(self, (self.ANCHO/2,(self.ALTO/3 * 2))),
                             BotonConfiguraciones(self, (self.ANCHO/2, ((self.ALTO/3 * 2)  +  self.BUTTON_SIZEY))),
                             BotonSalir(self, (self.ANCHO/2, ((self.ALTO/3 * 2)  +  self.BUTTON_SIZEY*2)))]
        
class PantallaConfiguracionesGUI(PantallaGUI):
    def __init__(self, menu):
        super().__init__(menu, "menu_sin_logo.jpeg")
        if self.ANCHO >= 1024:
            optionFont = ResourceManager.load_font("VT32314","VT323.ttf", 24)
        else:
            optionFont = ResourceManager.load_font("VT32310", "VT323.ttf", 20)

        self.elementosGUI = [   TextoMenu(self, "Resolucion", optionFont, (self.ANCHO/6, self.ALTO/6)),
                                TextoRes(self, Settings.NEGRO, "768x432", (self.ANCHO/6 + self.ANCHO*0.15, self.ALTO/6), (768,432), self.menu.director),
                                TextoRes(self, Settings.NEGRO, "1024x576", (self.ANCHO/6 + self.ANCHO*0.15*2, self.ALTO/6), (1024,576), self.menu.director),
                                TextoRes(self, Settings.NEGRO, "1280x720", (self.ANCHO/6 + self.ANCHO*0.15*3, self.ALTO/6), (1280, 720), self.menu.director),
                                TextoRes(self, Settings.NEGRO, "Full Screen", (self.ANCHO/6 + self.ANCHO*0.15*4, self.ALTO/6), None, self.menu.director),
                                TextoMenu(self, "Volumen Música", optionFont, (self.ANCHO/6, self.ALTO/6 + Settings.BUTTON_SIZEY)),
                                TextoSonido(self, Settings.NEGRO, "0%", (self.ANCHO/6 + self.ANCHO*0.15,self.ALTO/6 + Settings.BUTTON_SIZEY), 0, True),
                                TextoSonido(self, Settings.NEGRO, "25%", (self.ANCHO/6 + self.ANCHO*0.15*2,self.ALTO/6 + Settings.BUTTON_SIZEY), 0.25, True),
                                TextoSonido(self, Settings.NEGRO, "50%", (self.ANCHO/6 + self.ANCHO*0.15*3,self.ALTO/6 + Settings.BUTTON_SIZEY), 0.50, True),
                                TextoSonido(self, Settings.NEGRO, "75%", (self.ANCHO/6 + self.ANCHO*0.15*4,self.ALTO/6 + Settings.BUTTON_SIZEY), 0.75, True),
                                TextoSonido(self, Settings.NEGRO, "100%", (self.ANCHO/6 + self.ANCHO*0.15*5,self.ALTO/6 + Settings.BUTTON_SIZEY), 1, True),
                                TextoMenu(self, "Volumen Efectos", optionFont, (self.ANCHO/6, self.ALTO/6 + Settings.BUTTON_SIZEY * 2)),
                                TextoSonido(self, Settings.NEGRO, "0%", (self.ANCHO/6 + self.ANCHO*0.15,self.ALTO/6 + Settings.BUTTON_SIZEY*2), 0, False),
                                TextoSonido(self, Settings.NEGRO, "25%", (self.ANCHO/6 + self.ANCHO*0.15*2,self.ALTO/6 + Settings.BUTTON_SIZEY*2), 0.25, False),
                                TextoSonido(self, Settings.NEGRO, "50%", (self.ANCHO/6 + self.ANCHO*0.15*3,self.ALTO/6 + Settings.BUTTON_SIZEY*2), 0.50, False),
                                TextoSonido(self, Settings.NEGRO, "75%", (self.ANCHO/6 + self.ANCHO*0.15*4,self.ALTO/6 + Settings.BUTTON_SIZEY*2), 0.75, False),
                                TextoSonido(self, Settings.NEGRO, "100%", (self.ANCHO/6 + self.ANCHO*0.15*5,self.ALTO/6 + Settings.BUTTON_SIZEY*2), 1, False),
                                BotonVolver(self, (self.ANCHO/2,self.ALTO - self.ALTO/6))]

class PantallaPauseGUI(PantallaGUI):
    def __init__(self, menu):
        super().__init__(menu, "menu_inicial.jpeg")
        self.background = None
        self.elementosGUI = [BotonResume(self, (self.ANCHO/2, self.ALTO/3)),
                             BotonCargar(self, (self.ANCHO/2, self.ALTO/3 + self.BUTTON_SIZEY)),
                             BotonGuardar(self, (self.ANCHO/2, self.ALTO/3 + self.BUTTON_SIZEY*2)),
                             BotonReturnToTitle(self, (self.ANCHO/2, self.ALTO/3 + self.BUTTON_SIZEY * 3)),
                             BotonControles(self, (self.ANCHO/2, self.ALTO/3 + self.BUTTON_SIZEY * 4)),
                             BotonSalir(self, (self.ANCHO/2, self.ALTO/3 + self.BUTTON_SIZEY * 5))]
        
    def dibujar(self,pantalla):
        if self.background == None:
            #no se pinta la imagen sino que se guarda una copia de la pantalla para que se vea el juego de fondo mientras esta pausado
            self.background = pantalla.copy()
        pantalla.blit(self.background, (0,0))
        for elemento in self.elementosGUI:
            elemento.dibujar(pantalla)

    def eventos(self, lista_eventos):
        super().eventos(lista_eventos)

class PantallaControles(PantallaGUI):
    def __init__(self, menu):
        super().__init__(menu, "menu_ controles.png")
        self.elementosGUI = [BotonResume(self, (self.ANCHO / 2, self.ALTO / 1.2))]

class PantallaGameOverGUI(PantallaGUI):
    def __init__(self, menu):
        super().__init__(menu, "blank_background.jpg")
        self.elementosGUI = [BotonRetry(self, (self.ANCHO / 2, self.ALTO / 3 + self.BUTTON_SIZEY*2)),
                             BotonReturnToTitle(self, (self.ANCHO / 2, self.ALTO / 3 + self.BUTTON_SIZEY * 3)),
                             BotonSalir(self, (self.ANCHO / 2, self.ALTO / 3 + self.BUTTON_SIZEY * 4))]

class PantallaDialogo(PantallaGUI):
    def __init__(self, menu, dialogo, to):
        super().__init__(menu, f"dialogo_{dialogo}.png")
        self.elementosGUI = [BotonResume(self, (self.ANCHO/2, self.ALTO/1.2), to=to)]


class PantallaFin(PantallaGUI):

    def __init__(self, menu, final):
        # Para el final alternativo
        nombre_archivo = f"pantalla_final_{final}.png" if final is not None else "pantalla_final.png"
        super().__init__(menu, nombre_archivo)
        self.elementosGUI = [BotonReturnToTitle(self, (self.ANCHO / 2, self.ALTO / 3 + self.BUTTON_SIZEY * 3)),
                             BotonCreditos(self, (self.ANCHO / 2, self.ALTO / 3 + self.BUTTON_SIZEY * 4)),]


class PantallaCreditos(PantallaGUI):
    def __init__(self, menu):
        super().__init__(menu, "creditos.png")
        self.elementosGUI = [BotonReturnToTitle(self, (self.ANCHO / 2, self.ALTO / 2 + self.BUTTON_SIZEY * 4))]



