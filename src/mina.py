import pygame
from interactuable import Interactuable
from settings import COLLISION_RULES, CollisionLayer
import settings

class Mina(Interactuable):

    def __init__(self, x, y):
        self.imagen = self.escalar_y_cargar("../res/entidades/jugador/armas/dynamite.png", 1, 1)
        self.tiempo_creacion = pygame.time.get_ticks()
        #self.animacion_explosion = settings.escalar_y_cargar_animacion()
        self.duracion = 5000 #tiempo en ms que la mina queda en el suelo
        super().__init__(x, y, self.imagen, CollisionLayer.BULLET_PLAYER)

    def update(self, jugador):
        return super().update(jugador)
    
    def activar(self, mundo):
        self.habilitado = False
        #animación de explotar
        pass

