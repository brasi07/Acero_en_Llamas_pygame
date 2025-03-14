import pygame
from .interactable import Interactable
from ...extras.resourcesmanager import ResourceManager
from ...extras.settings import CollisionLayer, TIME_FRAME


class Mine(Interactable):

    def __init__(self, x, y):
        self.imagen = ResourceManager.load_and_scale_image("dynamite.png", 1, 1)
        self.tiempo_creacion = pygame.time.get_ticks()
        self.frame_actual = -1
        self.ultimo_cambio_frame = 0
        self.activo = False
        self.objeto_colisionando = True
        self.animacion = ResourceManager.load_animation("explosiones4A.png", 32, 32, 6, resizex=1, resizey=1)
        self.duracion = 5000 #tiempo en ms que la mina queda en el suelo
        super().__init__(x, y, self.imagen, CollisionLayer.BOTH)

    def update(self, jugador):
        if self.activo:
            tiempo_actual = pygame.time.get_ticks()  # Obtener el tiempo actual
            if tiempo_actual - self.ultimo_cambio_frame >= TIME_FRAME:
                    self.ultimo_cambio_frame = tiempo_actual  # Actualizar el tiempo del último cambio
                    if self.frame_actual < (len(self.animacion) - 1):
                        self.frame_actual += 1
                    else:
                        self.eliminar = True
                    self.imagen = self.animacion[self.frame_actual]

        if not self.check_collision(jugador):
            self.objeto_colisionando = False

    def interactuar(self, objeto):
        if not self.objeto_colisionando and self.check_collision(objeto) and not self.activo:
            objeto.recibir_dano(1)
            self.activo = True

    def deactivate(self):
        self.activo = True