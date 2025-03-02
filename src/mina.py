import pygame
from interactuable import Interactuable
from resourcesmanager import ResourceManager
from settings import COLLISION_RULES, CollisionLayer
import settings

class Mina(Interactuable):

    def __init__(self, x, y):
        self.imagen = ResourceManager.load_and_scale_image("dynamite.png", 1, 1)
        self.tiempo_creacion = pygame.time.get_ticks()
        self.frame_actual = -1
        self.ultimo_cambio_frame = 0
        self.activo = False
        self.animacion = ResourceManager.load_animation("explosiones4A.png", 32, 32, 6, resizex=1, resizey=1)
        self.duracion = 5000 #tiempo en ms que la mina queda en el suelo
        super().__init__(x, y, self.imagen, CollisionLayer.BULLET_PLAYER)

    def update(self, jugador):
        if self.activo:
            tiempo_actual = pygame.time.get_ticks()  # Obtener el tiempo actual
            if tiempo_actual - self.ultimo_cambio_frame >= settings.TIME_FRAME:
                    self.ultimo_cambio_frame = tiempo_actual  # Actualizar el tiempo del último cambio
                    if self.frame_actual < (len(self.animacion) - 1):
                        self.frame_actual += 1
                    else:
                        self.eliminar = True
                    self.imagen = self.animacion[self.frame_actual]
    
    def interactuar(self, objeto):
         self.activo = True