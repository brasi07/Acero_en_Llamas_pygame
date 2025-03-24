import pygame

from .director import Director
from .menus.menu import MainMenu


class Game:
    def __init__(self):
        pygame.init()

        self.director = Director()

        """if evento.key == pygame.K_F11:
                            self.pantalla = pygame.display.set_mode((ANCHO, ALTO))""" #para cambiar la pantalla

        escena = MainMenu(self.director)
        self.director.cambiar_escena(escena)


    def run(self):
        self.director.ejecutar()
