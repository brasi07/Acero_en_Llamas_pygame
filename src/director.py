import pygame

from . import SingletonMeta
from .extras.settings import ANCHO, ALTO, FPS
from .gamesave import Partida


class Director(metaclass=SingletonMeta):

    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN | pygame.SCALED | pygame.DOUBLEBUF)
        self.pila_escenas = []
        self.salir_escena = False
        self.escena_guardada = None
        self.escena_guardada_clase = None
        self.escena_parametros = None
        self.clock = pygame.time.Clock()
        self.partida = Partida(4, 0, 0, 1)

    def bucle(self, escena):
        self.salir_escena = False
        pygame.event.clear()

        while not self.salir_escena:
            time_past = self.clock.tick(FPS)
            escena.eventos(pygame.event.get())
            escena.update(time_past)
            escena.dibujar(self.pantalla)
            pygame.display.flip()

    def ejecutar(self):
        while len(self.pila_escenas) > 0:
            escena = self.pila_escenas[len(self.pila_escenas)-1]
            self.bucle(escena)

    def salir_programa(self):
        self.pila_escenas = []
        self.salir_escena = True

    def salir_de_escena(self):
        self.salir_escena = True
        if len(self.pila_escenas) > 0:
            self.pila_escenas.pop()

    def cambiar_escena(self, nueva_escena):
        if self.escena_guardada:
            self.salir_de_escena()

        self.escena_guardada = nueva_escena
        self.escena_guardada_clase = type(nueva_escena)
        self.escena_parametros = nueva_escena.get_parametros()

        self.pila_escenas.append(nueva_escena)

    def reiniciar_escena(self):
        if self.escena_guardada_clase and self.escena_parametros:
            nueva_escena = self.escena_guardada_clase(*self.escena_parametros)
            self.cambiar_escena(nueva_escena)

    def apilar_escena(self, nueva_escena):
        self.salir_escena = True
        self.pila_escenas.append(nueva_escena)