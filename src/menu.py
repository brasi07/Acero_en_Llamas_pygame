from abc import abstractmethod

import pygame

from .extras.settings import ANCHO, ALTO, VERDE
from .scene import Scene


class Menu(Scene):

    opciones = []

    primera_opcion = 0
    ultima_opcion = 0

    @abstractmethod
    def __init__(self, director):
        super().__init__(director)
        pygame.font.init()
        self.font = pygame.font.Font(None, 74)
        self.selected_item = 0

    def dibujar(self, pantalla):

        for index, item in enumerate(self.opciones):
            color = VERDE if index == self.selected_item else (150, 150, 150)
            text = self.font.render(item, True, color)
            rect = text.get_rect(center=(ANCHO / 2, (ALTO / 2 - 100 + index * 100)))
            pantalla.blit(text, rect)


    @abstractmethod
    def do_the_thing(self):
        pass


class PauseMenu(Menu):

    def __init__(self, controller, director):
        self.opciones = ["Back to Game", "Quit"]
        self.control = controller
        super().__init__(director)

    def do_the_thing(self):

        actions = {
            0: self.volver_al_juego,
            1: self.salir_juego
        }
        actions[self.selected_item]()



    def volver_al_juego(self):
        self.director.salir_de_escena()

    def salir_juego(self):
        self.director.salir_programa()

    def update(self, tiempo):
        pass

    def eventos(self, eventos):

        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.director.salir_programa()
            if self.control.aceptar(evento):
                self.do_the_thing()
            if self.control.rechazar(evento):
                self.volver_al_juego() #despausar
            if self.control.arriba_tap(evento):
                self.selected_item -= 1
                if self.selected_item < 0: self.selected_item = 1
            if self.control.abajo_tap(evento):
                self.selected_item = (self.selected_item + 1) % 2

