import math
import pygame
import settings
from settings import CollisionLayer, COLLISION_RULES
from elements import Elemento

class Enemy(Elemento):
    def __init__(self, x, y):
        self.sprites = {
            "abajo": self.escalar_y_cargar("../res/enemigos/tanque_rojo.png"),
        }
        super().__init__(x, y, self.sprites["abajo"], CollisionLayer.ENEMY)

    def escalar_y_cargar(self, ruta):
        imagen = pygame.image.load(ruta)
        return pygame.transform.scale(imagen, (settings.TILE_SIZE * settings.RESIZE_PLAYER, settings.TILE_SIZE * settings.RESIZE_PLAYER))

    def update(self):
        pass  # Aquí iría la IA de movimiento

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)
