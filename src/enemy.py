import math
import pygame
import settings
from elements import Elemento

class Enemy(Elemento):
    def __init__(self, x, y, tamaño_tile):
        self.tamaño_tile = tamaño_tile
        self.sprites = {
            "abajo": self.escalar_y_cargar("../res/enemigos/tanque_rojo.png"),
        }
        super().__init__(x, y, True, self.sprites["abajo"])

    def escalar_y_cargar(self, ruta):
        imagen = pygame.image.load(ruta)
        return pygame.transform.scale(imagen, (self.tamaño_tile * settings.RESIZE_PLAYER, self.tamaño_tile * settings.RESIZE_PLAYER))

    def update(self):
        pass  # Aquí iría la IA de movimiento

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)
