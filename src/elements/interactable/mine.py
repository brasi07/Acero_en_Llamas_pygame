import pygame
from .interactable import Interactable
from ...extras import CollisionLayer, TIME_FRAME, ResourceManager, TILE_SIZE


class Mine(Interactable):

    def __init__(self, x, y):
        self.imagen = ResourceManager.load_and_scale_image("dynamite.png", 1, 1)
        super().__init__(x, y, self.imagen, CollisionLayer.BOTH)
        self.rect_element = self.imagen.get_rect(center=(x*TILE_SIZE, y*TILE_SIZE))
        self.tiempo_creacion = pygame.time.get_ticks()
        self.frame_actual = -1
        self.ultimo_cambio_frame = 0
        self.activo = False
        self.objeto_colisionando = True
        self.animacion = ResourceManager.load_animation("explosiones4A.png", 32, 32, 6, resizex=1, resizey=1)


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
            ResourceManager.play_sound("8bit_bomb_explosion.wav")
            self.activo = True