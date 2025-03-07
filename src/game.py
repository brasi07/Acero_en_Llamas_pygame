import pygame

from controller import KeyboardControl
from director import Director
from extras.settings import ANCHO, ALTO, FPS, SKY_WORLDS
from ui import Ui
from world import World
from tanks.player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.tamaño_pantalla = 1

        self.director = Director()

        """if evento.key == pygame.K_F11:
                            self.pantalla = pygame.display.set_mode((ANCHO, ALTO))""" #para cambiar la pantalla

        self.control = KeyboardControl()

        self.jugador = Player(0, 0, self.control)

        self.mundo1 = World(self.director.pantalla.get_height(), self.director.pantalla.get_width(),
                            self.director, Ui(), self.control, 1, self.jugador, SKY_WORLDS[1])

        self.director.apilar_escena(self.mundo1)

    def run(self):
        self.director.ejecutar()

