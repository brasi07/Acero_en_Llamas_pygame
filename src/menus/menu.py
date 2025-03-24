from abc import abstractmethod

import pygame

from ..scene import Scene
from .pantallaGUI import *
from ..tanks import player

class Menu(Scene):
    def __init__(self, director):
        # Llamamos al constructor de la clase padre
        Scene.__init__(self, director)
        # Creamos la lista de pantallas
        self.listaPantallas = []
        # Creamos las pantallas que vamos a tener
        # y las metemos en la lista
        #self.listaPantallas.append(Pantallas del menu especifico)
        # En que pantalla estamos actualmente
        #self.mostrarPantallaInicial()
        
    def update(self, *args):
        return
    
    def eventos(self, lista_eventos):
        # Se mira si se quiere salir de esta escena
        for evento in lista_eventos:
        # Si se quiere salir, se le indica al director
            #if evento.type == pygame.KEYDOWN:
                #if evento.key == pygame.K_ESCAPE:
                    #self.salirPrograma()
            if evento.type == pygame.QUIT:
                self.director.salir_programa()
        # Se pasa la lista de eventos a la pantalla actual
        self.listaPantallas[self.pantallaActual].eventos(lista_eventos)

    def dibujar(self, pantalla):
        self.listaPantallas[self.pantallaActual].dibujar(pantalla)

    def salirPrograma(self):
        self.director.salir_programa()

    def mostrarPantallaInicial(self):
        self.pantallaActual=0

    #ir a configuraciones podría no ser un método de menu en general, pero todos los menus que tenemos pueden ir a configuraciones asi que es conveniente estar aqui en este caso
    def irAConfiguraciones(self):
        self.pantallaActual=1 #encontrar una manera mellor de manjar las pantallas que no sea con el numero directamente

    def update(self, *args):
        self.listaPantallas[self.pantallaActual].update()

    def continuar(self):
        self.director.salir_de_escena()


class MainMenu(Menu):

    def __init__(self, director):
        super().__init__(director)
        self.listaPantallas.append(PantallaInicialGUI(self))
        self.listaPantallas.append(PantallaConfiguracionesGUI(self))
        self.mostrarPantallaInicial()
        ResourceManager.load_and_play_wav(f"title_theme.wav", -1)

    def ejecutarJuego(self): 
        from ..worlds import world1

        ResourceManager.stop_and_unload_wav(f"title_theme.wav")
        fase = world1.World1(self.director.pantalla.get_height(), self.director.pantalla.get_width())
        self.director.cambiar_escena(fase)

class PauseMenu(Menu):

    def __init__(self, director):
        super().__init__(director)
        self.listaPantallas.append(PantallaPauseGUI(self))
        self.listaPantallas.append(PantallaConfiguracionesGUI(self))
        self.mostrarPantallaInicial()





