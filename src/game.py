import pygame

from .director import Director
from .worlds.world1 import World1

class Game:
    def __init__(self):
        pygame.init()
        self.tamaño_pantalla = 1

        self.director = Director()

        """if evento.key == pygame.K_F11:
                            self.pantalla = pygame.display.set_mode((ANCHO, ALTO))""" #para cambiar la pantalla

        self.mundo1 = World1(self.director.pantalla.get_height(), self.director.pantalla.get_width(),
                            self.director)

        self.director.cambiar_escena(self.mundo1)

    def run(self):
        self.director.ejecutar()

