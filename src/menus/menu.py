from abc import abstractmethod

import pygame

from ..gamesave import Partida
from ..scene import Scene
from .pantallaGUI import *

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
            if evento.type == pygame.QUIT:
                self.director.salir_programa()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.salirPrograma()
        # Se pasa la lista de eventos a la pantalla actual
        self.listaPantallas[self.pantallaActual].eventos(lista_eventos)

    def ejecutarJuego(self):
        pass

    def dibujar(self, pantalla):
        self.listaPantallas[self.pantallaActual].dibujar(pantalla)

    def salirPrograma(self):
        self.director.salir_programa()

    def mostrarPantallaInicial(self):
        self.pantallaActual=0


    def update(self, *args):
        self.listaPantallas[self.pantallaActual].update()

    def continuar(self):
        self.director.salir_de_escena()

    def cargar_partida(self):
        from ..worlds import world1, world2, world3
        partida = Partida.load("save.pkl")
        if partida:
            self.director.partida = partida
            fase = world1.World1(self.director.pantalla.get_height(), self.director.pantalla.get_width())
            match partida.current_stage:
                case 1:
                    fase = world1.World1(self.director.pantalla.get_height(), self.director.pantalla.get_width())
                case 2:
                    fase = world2.World2(self.director.pantalla.get_height(), self.director.pantalla.get_width())
                case 3:
                    fase = world3.World3(self.director.pantalla.get_height(), self.director.pantalla.get_width())
            partida.set_save_coords(fase)
            self.director.cambiar_escena(fase)

    def return_to_title(self):
        self.director.cambiar_escena(MainMenu(self.director))


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
        self.director.partida = Partida(4, 4, 3, 0, 0, 1)
        sub_fase = DialogoMenu(self.director, "selva", world1.World1(self.director.pantalla.get_height(), self.director.pantalla.get_width()))
        fase = DialogoMenu(self.director, "inicial", sub_fase, "intersection.wav")
        self.director.cambiar_escena(fase)
    
    def irAConfiguraciones(self):
        self.pantallaActual=1 #encontrar una manera mellor de manjar las pantallas que no sea con el numero directamente

class PauseMenu(Menu):

    def __init__(self, director):
        super().__init__(director)
        self.listaPantallas.append(PantallaPauseGUI(self))
        self.mostrarPantallaInicial()

    def guardar_partida(self):
        self.director.partida.save()

    def eventos(self, lista_eventos):
        for evento in lista_eventos:
        # Si se quiere salir, se le indica al director
            if evento.type == pygame.QUIT:
                self.director.salir_programa()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.continuar()
        # Se pasa la lista de eventos a la pantalla actual
        self.listaPantallas[self.pantallaActual].eventos(lista_eventos)

class GameOverMenu(Menu):

    def __init__(self, director):
        super().__init__(director)
        self.listaPantallas.append(PantallaGameOverGUI(self))
        self.mostrarPantallaInicial()
        ResourceManager.load_and_play_wav(f"game_over_theme.wav")

    def reintentar(self):
        ResourceManager.stop_and_unload_wav(f"game_over_theme.wav")
        self.director.salir_de_escena()
        self.director.reiniciar_escena()

class DialogoMenu(Menu):

    def __init__(self, director, dialogo, to, music = ""):
        super().__init__(director)
        self.listaPantallas.append(PantallaDialogo(self, dialogo, to))
        if music != "":
            ResourceManager.load_and_play_wav(music)

        self.mostrarPantallaInicial()

class FinalMenu(Menu):
    
    def __init__(self, director):
        super().__init__(director)
        self.listaPantallas.append(PantallaFin(self))
        self.mostrarPantallaInicial()

class CreditosMenu(Menu):
    
    def __init__(self, director):
        super().__init__(director)
        self.listaPantallas.append(PantallaCreditos(self))
        self.mostrarPantallaInicial()

